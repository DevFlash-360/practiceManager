import anvil.server
import json
import uuid
from anvil.js.window import ej, jQuery, XMLHttpRequest, Date
from AnvilFusion.tools.utils import datetime_js_to_py
from DevFusion.components.GridView2 import GridView2
from datetime import datetime, timedelta
import anvil.js
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Staff, Case, Activity, Event, CaseUpdate
from ..Forms.EventForm import EventForm

PM_SCHEDULE_HEIGHT_OFFSET = 35
PM_AGENDA_SCHEDULE_DEFAULT_VIEWS = [
    {
        'option': 'Agenda',
        'eventTemplate': '<div class="template-wrap">\
            $<a class="e-subject">${subject}</a>\
            <div class="e-date-time">\
                <i class="fa-regular fa-clock pr-1"></i>\
                ${if(event_type==="event")}${start_time_time} - ${end_time_time}${/if}\
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
]
PM_AGENDA_UPDATE_DEFAULT_VIEWS = [
    {
        'option': 'Agenda',
        'eventTemplate': '<div class="template-wrap">\
            <div style="color: white;background-color: rgb(39, 45, 131); padding: 5px;">${case_name}</div>\
            <div>${todays_update}</div>\
            <div style="background-color: rgb(247, 247, 247); padding:5px;">\
                <div>${activity}</div>\
                <div>${update_time}</div>\
                   ${if(client_attendance_required===true)}<i class="fa-solid fa-check pr-1"></i>Client attendance required${/if}\
            </div>\
        </div>'
    }
]
PM_AGENDA_SCHEDULE_POPUP = {
    'content': '<div style="font-size: 14px;">\
        <div>\
            <i class="fa-regular fa-clock pr-1"></i>\
            ${if(event_type==="event")}${start_time_time} - ${end_time_time}${/if}\
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


class CaseAgendaView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.events_element_id = f"cases_{uuid.uuid4()}"
        self.updates_element_id = f"updates_{uuid.uuid4()}"

        self.events_view = AgendaEventView(self.events_element_id)
        self.updates_view = AgendaCaseUpdatesView(self.updates_element_id)


    def form_show(self):
        self.container_el.innerHTML = f'\
            <div style="display:flex;">\
                <div id="{self.events_element_id}" style="display: inline-block;flex:0 0 60%;">\
                </div>\
                <div id="{self.updates_element_id}" style="display:inline-block;">\
                </div>\
            </div>'
        # self.case_list.appendTo(f"#{self.events_element_id}")
        self.events_view.form_show()
        self.updates_view.form_show()

    def destroy(self):
        self.events_view.destroy()
        if self.container_el is not None:
            self.container_el.innerHTML = ''

class AgendaEventView:
    def __init__(self, container_id=None):
        self.schedule_el_id = None
        self.container_id = container_id
        self.container_el = None
        self.cases_filters = [] # Filter cards with this cases
        self.staffs_filters = [] # Filter cards with this staffs
        self.activity_filters = [] # Filter cards with this activities
        self.schedules = None # Contain schedule elements = self.events
        
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
            'url': '_/theme/agenda-data-adaptor.json',
            'adaptor': self.data_adaptor,
        })
        
        schedule_config = {
            'height': '100%',
            'currentView': 'Agenda',
            'views': PM_AGENDA_SCHEDULE_DEFAULT_VIEWS,
            'agendaDaysCount': 28,
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
            'quickInfoTemplates': PM_AGENDA_SCHEDULE_POPUP,
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
        self.schedule_height = jQuery(f"#pm-content")[0].offsetHeight - PM_SCHEDULE_HEIGHT_OFFSET
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
            uid = args.data.get('uid', None)
            if uid:
                action = 'edit'
                event = Event.get(uid)
            else:
                action = 'add'
                start_time = datetime_js_to_py(args.data.start_time)
                end_time = start_time + timedelta(hours=1)
                event = Event(start_time=start_time, end_time=end_time)
            editor = EventForm(data=event, action=action, target=self.container_id, update_source=self.update_schedule)
            editor.form_show()
        elif args.type == 'QuickInfo':
            if 'subject' not in args.data.keys():
                args.cancel = True
            args.data['location'] = 'LOCATION'

    def update_schedule(self, data, add_new):
        self.schedule.refreshEvents()

    def handler_filter_close(self, args):
        tree_data = self.dropdown_tree.getData()
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
                
        if selected_items:
            jQuery("#pm-filter-container .e-icons.e-ddt-icon")[0].style.color = "rgb(0 147 255)"
            # self.grid.element.querySelector(f'#pm-filter-container .e-icons.e-input-group-icon.e-ddt-icon::before').content = "\e735"
        else:
            jQuery("#pm-filter-container .e-icons.e-ddt-icon")[0].style.color = "#6b7280"
            # self.grid.element.querySelector(f'#pm-filter-container .e-icons.e-input-group-icon.e-ddt-icon::before').content = "\e72c"
        self.schedule.refreshEvents()

    def action_begin(self, args):
        # change event
        if args.requestType == 'eventChange':
            print('Begin / eventChange', args.requestType)
            changed_event = args.data
            event = Event.get(changed_event.uid)
            event['start_time'] = datetime_js_to_py(changed_event.start_time)
            event['end_time'] = datetime_js_to_py(changed_event.end_time)
            event.save()
            self.schedule.refreshEvents()

        # delete event(s)
        if args.requestType == 'eventRemove':
            print(f"action_begin / eventRemove {args}")
            for removed in args.data:
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
            # item['event_type'] = PM_SCHEDULE_TYPE_EVENT
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
        self.schedules = self.events

    def data_adaptor_get_data(self, query):
        query_data = json.loads(query.data)
        start_time = datetime.fromisoformat(query_data['StartDate'][:10])
        end_time = datetime.fromisoformat(query_data['EndDate'][:10])
        self.get_events(start_time, end_time)

        # construct HTTP request for data adaptor
        request = XMLHttpRequest()
        request.open('GET', '_/theme/agenda-data-adaptor.json', False)
        request.setRequestHeader('Content-Type', 'application/json; charset=utf-8')
        request.send({})
        query['httpRequest'] = request

        # call back to pass data back to adaptor
        query.onSuccess(self.schedules, query)

    def data_adaptor_record(self, query):
        print('record', query)


class AgendaCaseUpdatesView:
    def __init__(self, container_id=None):
        self.schedule_el_id = None
        self.container_id = container_id
        self.container_el = None
        self.schedules = None # Contain schedule elements = self.case_updates

        update_fields = {
            'id': {'name': 'uid'},
            'startTime': {'name': 'start_time', 'title': 'Start Time'},
            'endTime': {'name': 'end_time', 'title': 'End Time'},
            'next_date': {'name': 'next_date'}
        }

        self.data_adaptor = ej.data.CustomDataAdaptor()
        self.data_adaptor.options.getData = self.data_adaptor_get_data
        self.data_adaptor.options.addRecord = self.data_adaptor_record
        self.data_adaptor.options.updateRecord = self.data_adaptor_record
        self.data_adaptor.options.deleteRecord = self.data_adaptor_record
        self.data_adaptor.options.butchUpdate = self.data_adaptor_record
        self.data_manager = ej.data.DataManager({
            'url': '_/theme/case-data-adaptor.json',
            'adaptor': self.data_adaptor,
        })
        schedule_config = {
            'height': '100%',
            'currentView': 'Agenda',
            'views': PM_AGENDA_UPDATE_DEFAULT_VIEWS,
            'agendaDaysCount': 28,
            'selectedDate': Date.now(),
            'disableHtmlEncode': False, 
            # 'enableAdaptiveUI': True,
            'eventSettings': {
                'dataSource': self.data_manager,
                'fields': update_fields,
            },
            'popupOpen': self.popup_open,
            'actionBegin': self.action_begin,
            # 'hover': self.hover_event,
            'cssClass': 'pm-schedule-cell-width pm-schedule-cell-height e-hide-spinner',
            # 'renderCell': self.render_cell,
        }
        self.schedule = ej.schedule.Schedule(schedule_config)

    def form_show(self):
        self.schedule_el_id = uuid.uuid4()
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.schedule_height = jQuery(f"#pm-content")[0].offsetHeight - PM_SCHEDULE_HEIGHT_OFFSET
        self.container_el.innerHTML = f'\
        <div class="pm-scheduleview-container" style="height:{self.schedule_height}px;">\
            <div class="pm-gridview-title">Case Updates</div>\
            <div id="{self.schedule_el_id}"></div>\
        </div>'
        self.schedule.appendTo(jQuery(f"#{self.schedule_el_id}")[0])
    
    def destroy(self):
        self.schedule.destroy()
        if self.container_el is not None:
            self.container_el.innerHTML = ''

    def popup_open(self, args):
        print("Case Updates popup_open")
    
    def update_schedule(self, data, add_new):
        self.schedule.refreshEvents()

    def action_begin(self, args):
        print("Case Updates action_begin")

    def get_case_updates(self):
        # case_updates = anvil.server.call('get_case_updates', start_time)
        case_updates = anvil.server.call('get_case_updates')
        self.schedules = []
        for update in case_updates:
            item = {}
            item['uid'] = update['uid']
            item['update_time'] = update['next_date'].strftime("%m/%d/%Y @ %I:%M %p")
            item['start_time'] = update['next_date'].strftime("%m/%d/%Y @ %I:%M %p")
            print(item['start_time'])
            item['end_time'] = (update['next_date'] + timedelta(minutes=1)).strftime("%m/%d/%Y @ %I:%M %p")
            item['isAllDay'] = True
            item['todays_update'] = update['todays_update']
            item['activity'] = update['next_activity']['name']
            item['case_name'] = update['case']['case_name']
            item['client_attendance_required'] = update['client_attendance_required']

            self.schedules.append(item)
    
    def data_adaptor_get_data(self, query):
        self.get_case_updates()

        # construct HTTP request for data adaptor
        request = XMLHttpRequest()
        request.open('GET', '_/theme/case-data-adaptor.json', False)
        request.setRequestHeader('Content-Type', 'application/json; charset=utf-8')
        request.send({})
        query['httpRequest'] = request

        # call back to pass data back to adaptor
        query.onSuccess(self.schedules, query)

    def data_adaptor_record(self, query):
        print('record', query)
