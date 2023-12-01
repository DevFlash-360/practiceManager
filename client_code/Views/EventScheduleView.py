from anvil.tables import query as q
from anvil.js.window import ej, jQuery, Date, XMLHttpRequest, Object
from AnvilFusion.tools.utils import datetime_js_to_py
import anvil.js
from ..app.models import Event, Task, Case
from ..Forms.EventForm import EventForm
from ..Forms.TaskForm import TaskForm
from datetime import datetime, date, timedelta
import uuid
import json

PM_SCHEDULE_HEIGHT_OFFSET = 35
PM_SCHEDULE_DEFAULT_VIEWS = [
    'Agenda',
    'Day',
    'Week',
    'Month',
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
PM_SCHEDULE_CELL_TEMPLATE = '${if(type === "workCells")}<div>${pmRenderCell(resource)}</div>${/if}${if(type === ' \
                            '"monthCells")}${/if}'

PM_SCHEDULE_TYPE_EVENT = "event"
PM_SCHEDULE_TYPE_TASK = "task"
# PM_EVENT_VIEW_COLUMNS = [
#     {'name': 'start_time'},
#     {'name': 'end_time'},
#     {'name': 'activity.name'},
#     {'name': 'location.name'},
#     {'name': 'staff.full_name'},
#     {'name': 'case.case_name'},
#     {'name': 'no_case'},
#     {'name': 'department.full_name'},
#     {'name': ''},
# ]


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
        self.events = None # Contain events for Schedule data feed
        self.tasks = None # Contain tasks for Schedule data feed
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
            'actionComplete': self.action_complete,
            # 'hover': self.hover_event,
            'eventClick': self.event_click,
            'cssClass': 'pm-schedule-cell-width pm-schedule-cell-height e-hide-spinner',
            # 'cellTemplate': PM_SCHEDULE_CELL_TEMPLATE,
            # 'renderCell': self.render_cell,
        }

        self.schedule = ej.schedule.Schedule(schedule_config)
        # anvil.js.window.pmRenderCell = self.render_cell

        self.init_filters()

    def init_filters(self):
        cases_data = Case.search()
        cases_data_for_combobox = [{'Id': row['uid'], 'Text': row['case_name']} for row in cases_data]
        cases_data_for_combobox.insert(0, {'Id': 'all', 'Text': 'All cases'})
        self.filter_case = ej.dropdowns.ComboBox({
            'dataSource': cases_data_for_combobox,
            'fields': {'value': 'Id', 'text': 'Text'},
            'placeholder': 'Cases...',
        })
        self.filter_case.addEventListener('change', self.handler_filter_cases)

        self.filter_dropdown = ej.splitbuttons.DropDownButton({
            'iconCss': 'fa fa-filter',
            'items': cases_data_for_combobox
        }, '#iconbutton')

    # get events and bind them to the view
    def form_show(self, **event_args):
        self.schedule_el_id = uuid.uuid4()
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.schedule_height = self.container_el.offsetHeight - PM_SCHEDULE_HEIGHT_OFFSET
        self.container_el.innerHTML = f'\
       <div class="pm-scheduleview-container" style="height:{self.schedule_height}px;">\
         <div id="pm-filter-container" class="row"></div>\
         <div class="pm-gridview-title">Agenda</div>\
         <div id="{self.schedule_el_id}"></div>\
       </div>'
        self.schedule.appendTo(jQuery(f"#{self.schedule_el_id}")[0])

        self.add_filter_component("Case", self.filter_case)
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

    def handler_filter_cases(self, args):
        filterItem = args['itemData']['Id']
        self.schedules = []
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

    def action_complete(self, args):
        print('Complete', args.requestType)

    # def hover_event(self, args):
    #     if self.schedule.currentView not in PM_SCHEDULE_DETAIL_VIEWS:
    #         event = self.schedule.getEventDetails(args.element)
    #         if event:
    #             event['location'] = 'OVERRIDE'
    #             self.schedule.openQuickInfoPopup(event)
    #             # for k in event.keys():
    #             #  print(k, event[k])
    #         else:
    #             self.schedule.closeQuickInfoPopup()
                
    def event_click(self, args):
        event = self.schedule.getEventDetails(args.element)
        if event:
            self.schedule.openQuickInfoPopup(event)

    # def render_cell(self, args):
    #     # for k in args.keys():
    #     #   print(k, args[k])
    #     if args.elementType == 'workCells' or args.elementType == 'monthCells':
    #         # print('element', args.element)
    #         # for k in args.element.keys():
    #         #   print(k, args[k])
    #         event = self.schedule.getEventDetails(args.element)
    #         # if event:
    #         # print('event', event)


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
        ]

        self.events = Event.get_grid_view(view_config={'columns': event_cols}, filters=query)
        for event in self.events:
            event['event_type'] = PM_SCHEDULE_TYPE_EVENT
            event['subject'] = event['activity__name']
            event['description'] = event['notes']
            if event['case__case_name']:
                event['subject'] = f"{event['case__case_name']}: {event['subject']}"
        self.schedules = ej.base.extend(self.events, self.tasks, None, True)

    def get_tasks(self, start_time, end_time):
        filter_case = Case.get(self.filter_case.value)
        query = {
            'due_date': q.all_of(q.greater_than_or_equal_to(start_time.date()), q.less_than_or_equal_to(end_time.date())),
            'completed': q.not_(True),
        }
        if filter_case is not None:
            query['case'] = filter_case

        event_cols = [
            {'name':'uid'},
            {'name':'case.case_name'},
            {'name':'activity.name'},
            {'name':'due_date'},
            {'name':'priority'},
            {'name':'assigned_staff.full_name'},
            {'name':'notes'},
        ]

        self.tasks = []
        tasks = Task.get_grid_view(view_config={'columns':event_cols}, filters=query)
        for task in tasks:
            item = {}
            item['event_type'] = PM_SCHEDULE_TYPE_TASK
            item['uid'] = task['uid']
            item['start_time'] = task['due_date']
            item['end_time'] = (date.fromisoformat(task['due_date']) + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            item['isAllDay'] = True
            item['subject'] = task['activity__name']
            if task['case__case_name']:
                item['subject'] = f"{task['case__case_name']}: {item['subject']}"
            item['description'] = task.get('notes', '')
            self.tasks.append(item)
            
        self.schedules = ej.base.extend(self.events, self.tasks, None, True)

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
            <div id="{filter_el_id}"></div>'
        grid_toolbar.appendChild(filter_container)
        obj.appendTo(jQuery(f"#{filter_el_id}")[0])
