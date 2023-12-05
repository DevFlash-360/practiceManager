from anvil.tables import query as q
from anvil.js.window import ej, jQuery, Date, XMLHttpRequest, Object
from AnvilFusion.tools.utils import datetime_js_to_py
import anvil.js
from ..app.models import Event, Task, Case, Staff
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
                ${if(event_type==="event")}${start_time_time} - ${end_time_time}${/if}\
                ${if(event_type==="task")}All day${/if}\
            </div>\
            <div>${staff_name}</div>\
            <div>${location_name}</div>\
            ${if(client_attendance_required===true)}<span>Client attendance required</span>${/if}\
        </div>'
    },
    # 'Day',
    # 'Week',
    # 'Month',
]
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
        self.events = [] # Contain events for Schedule data feed
        self.tasks = [] # Contain tasks for Schedule data feed
        self.schedules = None # Contain schedule elements = self.events + self.tasks

        event_fields = {
            'id': {'name': 'uid'},
            'subject': {'name': 'subject', 'title': 'Event'},
            'startTime': {'name': 'start_time', 'title': 'Start Time'},
            'endTime': {'name': 'end_time', 'title': 'End Time'},
            'description': {'name': 'description', 'title': 'Description'},
            'location': {'name': 'location', 'title': 'Location'},
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
            'eventSettings': {
                'dataSource': self.data_manager,
                'fields': event_fields,
            },
            'popupOpen': self.popup_open,
            'actionBegin': self.action_begin,
            # 'hover': self.hover_event,
            'eventClick': self.event_click,
            'cssClass': 'pm-schedule-cell-width pm-schedule-cell-height e-hide-spinner',
            # 'renderCell': self.render_cell,
        }

        self.schedule = ej.schedule.Schedule(schedule_config)

        self.init_filters()

    def init_filters(self):
        # ej.base.enableRipple(True)
        cases_data = Case.search()
        cases_data_for_dropdown = [{'Id': case['uid'], 'text': case['case_name']} for case in cases_data]
        cases_data_for_dropdown.insert(0, {'Id': 'cases_all', 'text': 'All cases'})

        staff_data = Staff.search()
        staff_data_for_dropdown = [{'Id': row['uid'], 'text': row['first_name'] + " " + row['last_name']} for row in staff_data]
        staff_data_for_dropdown.insert(0, {'Id': 'staffs_all', 'text': 'All staffs'})

        self.filter_dropdown = ej.splitbuttons.DropDownButton({
            'target': '#eventfilterlist',
            'iconCss': 'fa fa-filter',
            'cssClass': 'e-caret-hide'
        })

        dataSource = [
            {'Id': 'cases', 'text': 'Cases'},
            {'Id': 'staffs', 'text': 'Staffs'},
        ]

        dataSource[0]['items'] = cases_data_for_dropdown
        dataSource[1]['items'] = staff_data_for_dropdown

        self.query_filter_cases = []

        self.tree_filters = ej.navigations.TreeView({
            'fields': { 'dataSource': dataSource, id: "code", 'text': "name", 'child': "countries" },
            'nodeSelected': self.handler_nodeSelected,
            'cssClass': "accordiontree"
        })

        # self.filter_case = ej.dropdowns.ComboBox({
        #     'dataSource': cases_data_for_dropdown,
        #     'fields': {'value': 'Id', 'text': 'text', 'groupBy': 'category'},
        #     'placeholder': 'Cases...',
        # })
        # self.filter_case.addEventListener('change', self.handler_filter_cases)
       
    # get events and bind them to the view
    def form_show(self, **event_args):
        self.schedule_el_id = uuid.uuid4()
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.schedule_height = self.container_el.offsetHeight - PM_SCHEDULE_HEIGHT_OFFSET
        self.container_el.innerHTML = f'\
       <div class="pm-scheduleview-container" style="height:{self.schedule_height}px;">\
         <div id="pm-filter-container" class="row"></div>\
         <div id="eventfilterlist"></div>\
         <div class="pm-gridview-title">Agenda</div>\
         <div id="{self.schedule_el_id}"></div>\
       </div>'
        self.schedule.appendTo(jQuery(f"#{self.schedule_el_id}")[0])

        # self.add_filter_component("Case", self.filter_case)
        self.tree_filters.appendTo('#eventfilterlist')
        self.add_filter_component('', self.filter_dropdown)

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

    def handler_nodeSelected(self, args):
        print(f"===== handler_nodeSelected ===== \n {args.node}")
        if (args.node.classList.contains('e-level-1')):
            args.cancel = True
            self.tree_filters.collapseAll()
            self.tree_filters.expandAll([args.node])

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

    # def render_cell(self, args):
    #     if args.elementType == 'workCells' or args.elementType == 'monthCells':
    #         event = self.schedule.getEventDetails(args.element)

    def get_events(self, start_time, end_time):
        query = {'start_time': q.all_of(q.greater_than(start_time), q.less_than(end_time))}
        event_cols = [
            {'name': 'uid'},
            {'name': 'start_time'},
            {'name': 'end_time'},
            {'name': 'activity.name'},
            {'name': 'case.case_name'},
            {'name': 'location.name'},
            {'name': 'department.full_name'},
            {'name': 'staff.full_name'},
            {'name': 'notes'},
            {'name': 'client_attendance_required'}
        ]

        self.events = Event.get_grid_view(view_config={'columns': event_cols}, filters=query)
        for event in self.events:
            event['event_type'] = PM_SCHEDULE_TYPE_EVENT
            event['subject'] = event['activity__name']
            event['description'] = event['notes']
            if 'case__case_name' in event:
                event['subject'] = f"{event['case__case_name']}: {event['subject']}"
            event['start_time_time'] = datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
            event['end_time_time'] = datetime.strptime(event['end_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
            if 'staff__full_name' in event:
                event['staff_name'] = event['staff__full_name']
            event['location_name'] = event['location__name'] if 'location__name' in event and event['location__name'] else ''
            print(f"location_name = {event['location_name']}")
        self.schedules = self.events + self.tasks
        # self.schedules = ej.base.extend(self.events, self.tasks, None, True)

    def get_tasks(self, start_time, end_time):
        query = {
            'due_date': q.all_of(q.greater_than_or_equal_to(start_time.date()), q.less_than_or_equal_to(end_time.date())),
            'completed': q.not_(True),
        }
        if self.query_filter_cases:
            query['case'] = q.any_of(self.query_filter_cases)

        event_cols = [
            {'name':'uid'},
            {'name':'case.case_name'},
            {'name':'activity.name'},
            {'name':'due_date'},
            {'name':'priority'},
            {'name':'assigned_staff.full_name'},
            {'name':'notes'},
            {'name': 'due_date_view'}
        ]

        self.tasks = []
        tasks = Task.get_grid_view(view_config={'columns':event_cols}, filters=query)
        for task in tasks:
            item = {}
            item['event_type'] = PM_SCHEDULE_TYPE_TASK
            item['uid'] = task['uid']
            item['start_time'] = task['due_date']
            item['end_time'] = (date.fromisoformat(task['due_date']) + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            item['start_time_time'] = date.fromisoformat(task['due_date']).strftime('%H:%M')
            item['end_time_time'] = item['start_time_time']
            item['isAllDay'] = True
            item['subject'] = task['activity__name']
            if 'case__case_name' in task:
                item['subject'] = f"{task['case__case_name']}: {item['subject']}"
            item['description'] = task.get('notes', '')
            item['staff_name'] = task['assigned_staff__full_name']
            item['location_name'] = ''
            item['isOverdue'] = date.fromisoformat(task['due_date']) < date.today()
            self.tasks.append(item)
            
        # self.schedules = ej.base.extend(self.events, self.tasks, None, True)
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

    def add_filter_component(self, label, obj):
        filter_el_id = uuid.uuid4()
        grid_toolbar = jQuery("#pm-filter-container")[0]
        filter_container = anvil.js.window.document.createElement('div')
        filter_container.className = 'col-6 col-md-4 col-lg-2'
        filter_container.innerHTML = f'\
            <label for="{filter_el_id}">{label}</label>\
            <div id="{filter_el_id}" class="e-caret-hide"></div>'
        grid_toolbar.appendChild(filter_container)
        obj.appendTo(jQuery(f"#{filter_el_id}")[0])
