import copy
import anvil.server
from anvil.tables import query as q
from anvil.js.window import ej, jQuery, Date, XMLHttpRequest, Object
from AnvilFusion.tools.utils import datetime_js_to_py
import anvil.js
from anvil.tables import app_tables
import anvil.server
from ..app.models import Event, Task, Case, Staff, Activity
from ..Forms.EventForm import EventForm
from ..Forms.TaskForm import TaskForm
from datetime import datetime, date, timedelta
import uuid
import json

PM_SCHEDULE_TYPE_EVENT = "event"
PM_SCHEDULE_TYPE_TASK = "task"

PM_SCHEDULE_HEIGHT_OFFSET = 35
PM_SCHEDULE_DEFAULT_VIEWS = [
    {
        'option': 'Agenda',
        'eventTemplate': '<div class="template-wrap">\
            ${if(event_type==="task" && isOverdue===true)}<span class="label label-danger">DUE</span>${/if}\
            <a class="e-subject">${subject}</a>\
            <div class="e-date-time">\
                <i class="fa-regular fa-clock pr-1"></i>\
                ${if(event_type==="event")}${start_time_time} - ${end_time_time}${/if}\
                ${if(event_type==="task")}All day${/if}\
            </div>\
            ${if(staff_name)}\
                <div><i class="fa-light fa-user pr-1"></i>${staff_name}</div>\
            ${/if}\
            ${if(location_name)}\
                <div><i class="fa-light fa-location-dot pr-1"></i>${location_name}</div>\
            ${/if}\
            ${if(department)}\
                <div><i class="fa-regular fa-building pr-1"></i>${department}</div>\
            ${/if}\
            ${if(client_attendance_required===true)}<i class="fa-solid fa-check pr-1"></i>Client attendance required${/if}\
        </div>'
    },
    # 'Day',
    'Week',
    'Month',
]
PM_SCHEDULE_POPUP = {
    'content': '<div style="font-size: 14px;">\
		<div>\
			<i class="fa-regular fa-clock pr-1"></i>\
			${if(event_type==="event")}${start_time_time} - ${end_time_time}${/if}\
			${if(event_type==="task")}All day${/if}\
		</div>\
		${if(staff_name)}\
			<div style="padding-top:12px;"><i class="fa-regular fa-user pr-1"></i>${staff_name}</div>\
		${/if}\
		${if(location_name)}\
			<div style="padding-top:12px;"><i class="fa-regular fa-location-dot pr-1"></i>${location_name}</div>\
		${/if}\
		${if(department)}\
			<div style="padding-top:12px;"><i class="fa-regular fa-building pr-1"></i>${department}</div>\
		${/if}\
		${if(client_attendance_required===true)}<i class="fa-solid fa-check pr-1"></i>Client attendance required${/if}'
}
PM_SCHEDULE_DETAIL_VIEWS = [
    # 'Agenda',
    'MonthAgenda',
    'TimelineDay',
    'TimelineWeek',
    'TimelineWorkWeek',
    'TimelineMonth',
    'TimelineYear',
]


class EventScheduleView:
    def __init__(self,
                 container_id=None,
                 model=None,
                 title=None,
                 ):
        print('EventScheduleView')

        self.db_data = None
        self.schedule_el_id = None
        self.schedule_height = None
        self.container_id = container_id
        self.container_el = None
        self.cases_filters = [] # Filter cards with this cases
        self.staffs_filters = [] # Filter cards with this staffs
        self.activity_filters = [] # Filter cards with this activities
        self.events  = [] # Events on filter
        self.tasks = [] # Staffs on filter
        self.schedules = None # Contain schedule elements = self.events + self.tasks

        event_fields = {
            'id': {'name': 'uid'},
            'subject': {'name': 'subject', 'title': 'Event'},
            'startTime': {'name': 'start_time', 'title': 'Start Time'},
            'endTime': {'name': 'end_time', 'title': 'End Time'},
            'description': {'name': 'description', 'title': 'Description'},
            'location': {'name': 'location_name', 'title': 'Location'},
        }

        self.data_adaptor = ej.data.CustomDataAdaptor()
        self.data_adaptor.options.getData = self.data_adaptor_get_data
        self.data_adaptor.options.addRecord = self.data_adaptor_record
        self.data_adaptor.options.updateRecord = self.data_adaptor_record
        self.data_adaptor.options.deleteRecord = self.data_adaptor_record
        self.data_adaptor.options.butchUpdate = self.data_adaptor_record
        self.data_manager = ej.data.DataManager({
            'url': '_/theme/data-adaptor.json',
            'adaptor': self.data_adaptor,
        })

        schedule_config = {
            'height': '100%',
            'currentView': 'Agenda',
            'views': PM_SCHEDULE_DEFAULT_VIEWS,
            'selectedDate': Date.now(),
            'disableHtmlEncode': False, 
            # 'enableAdaptiveUI': True,
            'eventSettings': {
                'dataSource': self.data_manager,
                'fields': event_fields,
            },
            'popupOpen': self.popup_open,
            'actionBegin': self.action_begin,
            # 'hover': self.hover_event,
            'eventClick': self.event_click,
            'cssClass': 'pm-schedule-cell-width pm-schedule-cell-height e-hide-spinner',
            # 'quickInfoTemplates': PM_SCHEDULE_POPUP,
            # 'renderCell': self.render_cell,
        }

        self.schedule = ej.schedule.Schedule(schedule_config)

        self.init_filters()

    def init_filters(self):
        # ej.base.enableRipple(True)
        cases_data = Case.search()
        cases_data_for_dropdown = [{'id': case['uid'], 'pid': 'cases', 'text': case['case_name']} for case in cases_data]

        staff_data = Staff.search()
        staff_data_for_dropdown = [{'id': row['uid'], 'pid': 'staffs', 'text': row['first_name'] + " " + row['last_name']} for row in staff_data]

        activity_data = Activity.search()
        activity_data_for_dropdown = [{'id': row['uid'], 'pid': 'activities', 'text': row['name']} for row in activity_data]

        dataSource = [
            {'id': 'cases', 'text': 'Case', 'hasChild': True},
            {'id': 'staffs', 'text': 'Staff', 'hasChild': True},
            {'id': 'activities', 'text': 'Activity', 'hasChild': True},
        ]
        dataSource.extend(staff_data_for_dropdown)
        dataSource.extend(cases_data_for_dropdown)
        dataSource.extend(activity_data_for_dropdown)

        self.dropdown_tree = ej.dropdowns.DropDownTree({
            'fields': {'dataSource': dataSource, 'value':'id', 'parentValue': 'pid', 'text':'text', 'hasChildren': 'hasChild'},
            'showCheckBox': True,
            'treeSettings': {'autoCheck': True},
            # 'placeholder': 'Apply filter...'
        })
        
        # self.dropdown_tree.addEventListener('select', self.handler_filter_select)
        self.dropdown_tree.addEventListener('close', self.handler_filter_close)
       
    # get events and bind them to the view
    def form_show(self, **event_args):
        self.schedule_el_id = uuid.uuid4()
        self.filter_el_id = uuid.uuid4()
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.schedule_height = self.container_el.offsetHeight - PM_SCHEDULE_HEIGHT_OFFSET
        self.container_el.innerHTML = f'\
       <div class="pm-scheduleview-container" style="height:{self.schedule_height}px;">\
         <div id="eventfilterlist"></div>\
         <div class="pm-gridview-title">Agenda</div>\
         <div id="pm-filter-container">\
          <div id="{self.filter_el_id}" class="e-caret-hide" style="width: 250px;display:block;"></div>\
         </div>\
         <div id="{self.schedule_el_id}"></div>\
       </div>'
        self.schedule.appendTo(jQuery(f"#{self.schedule_el_id}")[0])
        self.dropdown_tree.appendTo(jQuery(f"#{self.filter_el_id}")[0])

    def destroy(self):
        self.schedule.destroy()
        if self.container_el is not None:
            self.container_el.innerHTML = ''

    def popup_open(self, args):
        if args.type == 'Editor':
            args.cancel = True
            event_type = args.data.get('event_type', PM_SCHEDULE_TYPE_EVENT)
            uid = args.data.get('uid', None)
            if event_type == PM_SCHEDULE_TYPE_EVENT:
                if uid:
                    action = 'edit'
                    event = Event.get(uid)
                else:
                    action = 'add'
                    start_time = datetime_js_to_py(args.data.start_time)
                    end_time = start_time + timedelta(hours=1)
                    event = Event(start_time=start_time, end_time=end_time)
                editor = EventForm(data=event, action=action, target=self.container_id, update_source=self.update_schedule)
            elif event_type == PM_SCHEDULE_TYPE_TASK:
                if uid:
                    action = 'edit'
                    task = Task.get(uid)
                else:
                    action = 'add'
                    due_date = datetime_js_to_py(args.data.start_time)
                    task = Task(due_date=due_date)
                editor = TaskForm(data=task, action=action, target=self.container_id, update_source=self.update_schedule)
            editor.form_show()
        elif args.type == 'QuickInfo':
            if 'subject' not in args.data.keys():
                args.cancel = True
            args.data['location'] = 'LOCATION'

    def update_schedule(self, data, add_new):
        self.schedule.refreshEvents()

    # def handler_filter_select(self, args):
    #     tree_data = self.dropdown_tree.getData()
    #     all_cases = tree_data[0].get('selected', False)
    #     all_staffs = tree_data[1].get('selected', False)
    #     selected_items = [item for item in tree_data if item.get('selected')]

    #     self.cases_filters = []
    #     self.staffs_filters = []

    #     for item in selected_items:
    #         if not all_cases and item.get('pid') == 'cases':
    #             self.cases_filters.append(item['id'])
    #         if not all_staffs and item.get('pid') == 'staffs':
    #             self.staffs_filters.append(item['id'])

    #     self.schedule.refreshEvents()

    def handler_filter_close(self, args):
        tree_data = self.dropdown_tree.getData()
        print(f"=======tree_data = \n{tree_data}=========")
        all_cases = tree_data[0].get('selected', False)
        all_staffs = tree_data[1].get('selected', False)
        all_activity = tree_data[2].get('selected', False)
        selected_items = [item for item in tree_data if item.get('selected')]

        self.cases_filters = []
        self.staffs_filters = []
        self.activity_filters = []

        for item in selected_items:
            if not all_cases and item.get('pid') == 'cases':
                self.cases_filters.append(item['id'])
            if not all_staffs and item.get('pid') == 'staffs':
                self.staffs_filters.append(item['id'])
            if not all_activity and item.get('pid') == 'activities':
                self.activity_filters.append(item['id'])

        self.schedule.refreshEvents()

    def action_begin(self, args):
        # change event
        if args.requestType == 'eventChange':
            print('Begin / eventChange', args.requestType)
            changed_event = args.data
            if changed_event['event_type'] == PM_SCHEDULE_TYPE_TASK:
                task = Task.get(changed_event.uid)
                task['due_date'] = datetime_js_to_py(changed_event.start_time).date()
                task.save()
            elif changed_event['event_type'] == PM_SCHEDULE_TYPE_EVENT:
                event = Event.get(changed_event.uid)
                event['start_time'] = datetime_js_to_py(changed_event.start_time)
                event['end_time'] = datetime_js_to_py(changed_event.end_time)
                event.save()
            self.schedule.refreshEvents()

        # delete event(s)
        if args.requestType == 'eventRemove':
            print(f"action_begin / eventRemove {args}")
            for removed in args.data:
                if removed['event_type'] == PM_SCHEDULE_TYPE_TASK:
                    task = Task.get(removed.uid)
                    task.delete()
                elif removed['event_type'] == PM_SCHEDULE_TYPE_EVENT:
                    event = Event.get(removed.uid)
                    event.delete()
            self.schedule.refreshEvents()

    def event_click(self, args):
        event = self.schedule.getEventDetails(args.element)
        if event:
            self.schedule.openQuickInfoPopup(event)

    def get_events(self, start_time, end_time):
        events = anvil.server.call('get_events_filter', start_time, end_time, self.cases_filters, self.staffs_filters, self.activity_filters)
        self.events = []
        for event in events:
            item = {}
            item['uid'] = event['uid']
            item['start_time'] = event['start_time'].strftime('%Y-%m-%d %H:%M:%S')
            item['end_time'] = event['end_time'].strftime('%Y-%m-%d %H:%M:%S')
            item['event_type'] = PM_SCHEDULE_TYPE_EVENT
            item['subject'] = event['activity']['name']
            item['description'] = event['notes']
            if event['case'] and event['case']['case_name']:
                item['subject'] = f"{item['subject']}: {event['case']['case_name']}"
            item['start_time_time'] = event['start_time'].strftime('%H:%M')
            item['end_time_time'] = event['end_time'].strftime('%H:%M')
            item['staff_name'] = ' '.join([f"{staff['first_name']} {staff['last_name']}" for staff in event['staff']])
            item['location_name'] = event['location']['name'] if event['location'] and event['location']['name'] else ''
            item['department'] = ""
            if event['department'] and event['department']['department'] and event['department']['courtroom']:
                item['department'] = f"{event['department']['department']}/{event['department']['courtroom']} - {event['department']['last_name']}"
            self.events.append(item)
        self.schedules = self.events + self.tasks

    def get_tasks(self, start_time, end_time):
        tasks = anvil.server.call('get_tasks_filter', self.cases_filters, self.staffs_filters, self.activity_filters, start_time, end_time)
        self.tasks = []
        for task in tasks:
            item = {}
            item['event_type'] = PM_SCHEDULE_TYPE_TASK
            item['uid'] = task['uid']
            item['start_time'] = task['due_date'].strftime('%Y-%m-%d %H:%M:%S')
            item['end_time'] = (task['due_date'] + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            item['start_time_time'] = task['due_date'].strftime('%H:%M')
            item['end_time_time'] = item['start_time_time']
            item['isAllDay'] = True
            item['subject'] = task['activity']['name']
            if task['case'] and task['case']['case_name']:
                item['subject'] = f"{item['subject']}: {task['case']['case_name']}"
            item['description'] = task.get('notes', '')
            item['staff_name'] = ' '.join([f"{staff['first_name']} {staff['last_name']}" for staff in task['assigned_staff']])
            item['isOverdue'] = task['due_date'] < date.today()
            self.tasks.append(item)
        self.schedules = self.events + self.tasks

    def data_adaptor_get_data(self, query):
        query_data = json.loads(query.data)
        start_time = datetime.fromisoformat(query_data['StartDate'][:10])
        end_time = datetime.fromisoformat(query_data['EndDate'][:10])
        self.get_events(start_time, end_time)
        self.get_tasks(start_time, end_time)

        # construct HTTP request for data adaptor
        request = XMLHttpRequest()
        request.open('GET', '_/theme/data-adaptor.json', False)
        request.setRequestHeader('Content-Type', 'application/json; charset=utf-8')
        request.send({})
        query['httpRequest'] = request

        # call back to pass data back to adaptor
        query.onSuccess(self.schedules, query)

    def data_adaptor_record(self, query):
        print('record', query)

    # def add_filter_component(self, label, obj):
    #     filter_el_id = uuid.uuid4()
    #     grid_toolbar = jQuery("#pm-filter-container")[0]
    #     filter_container = anvil.js.window.document.createElement('div')
    #     # filter_container.className = 'col-6 col-md-4 col-lg-2'
    #     filter_container.innerHTML = f'\
    #         <label for="{filter_el_id}">{label}</label>\
    #         <div id="{filter_el_id}" class="e-caret-hide"></div>'
    #     grid_toolbar.appendChild(filter_container)
    #     obj.appendTo(jQuery(f"#{filter_el_id}")[0])
