import anvil.server
import uuid
from anvil.js.window import ej, jQuery
from DevFusion.components.GridView2 import GridView2
from datetime import datetime, date
import anvil.js
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Staff, Case, Task, Activity
class TaskListView(GridView2):
    def __init__(self, case=None, case_uid=None, **kwargs):
        print('TaskListView')
        view_config = {
            'model': 'Task',
            'columns': [
                {'name': 'completed', 'label': 'Completed', 'visible': False, 'width': 100},
                {'name': 'due_date_days', 'label': 'Due Date'},
                {'name': 'due_date_view', 'label': 'Due Date', 'visible': False},
                {'name': 'due_date', 'label': 'Due Date'},
                {'name': 'case.case_name', 'label': 'Case'},
                {'name': 'activity.name', 'label': 'Activity'},
                {'name': 'priority', 'label': 'Priority'},
                {'name': 'assigned_staff.full_name', 'label': 'Assigned Staff'},
                {'name': 'notes', 'label': 'Notes'},
            ],
            'filter': {'case': kwargs.get('case_uid')} if kwargs.get('case_uid') else None,
        }
        case_uid = case['uid'] if case else case_uid
        if case_uid:
            filters = {
                'case': {'uid': case_uid}
            }
        else:
            filters = None

        super().__init__(model='Task', view_config=view_config, filters=filters, **kwargs)
        anvil.js.window['captionTemplateFormat'] = self.due_date_caption
        self.grid.allowGrouping = True
        self.grid.groupSettings = {
            'columns': ['due_date_days'],
            'showDropArea': False,
            # 'captionTemplate': '<div>${key} - ${data}</div>',
            'captionTemplate': '<div>${captionTemplateFormat(data)}</div>',
        }
        self.grid.allowSorting = True
        self.grid.sortSettings = {
            'columns': [
                {'field': 'due_date_days', 'direction': 'Ascending'},
            ]
        }
        # self.grid.filterSettings = {
        #     'columns': [
        #         {'field': 'completed', 'operator': 'notequal', 'value': True}
        #     ]
        # }

        # self.grid.editSettings = {
        #     'allowEditing': True,
        #     'allowAdding': False,
        #     'allowDeleting': True,
        #     'mode': 'Normal',
        # }
        # self.grid.dataBound = self.collapse_all
        self.first_load = True
        self.cases_filters = [] # Filter cards with this cases
        self.staffs_filters = [] # Filter cards with this staffs
        self.activity_filters = [] # Filter cards with this activities
        self.param_complete = [False, None]

        self.init_filters()
        self.init_events()
        self.get_tasks_filter()

    def init_filters(self):
        
        self.events  = [] # Events on filter
        self.tasks = [] # Staffs on filter

        cases_data = Case.search()
        cases_data_for_dropdown = [{'id': case['uid'], 'pid': 'cases', 'text': case['case_name']} for case in cases_data]

        staff_data = Staff.search()
        staff_data_for_dropdown = [{'id': row['uid'], 'pid': 'staffs', 'text': row['first_name'] + " " + row['last_name']} for row in staff_data]
       
        activity_data = Activity.search()
        activity_data_for_dropdown = [{'id': row['uid'], 'pid': 'activities', 'text': row['name']} for row in activity_data]


        dataSource = [
            {'id': 'statuses', 'text': 'Status', 'hasChild': True},
            {'id': 'complete', 'text': 'Complete', 'pid': 'statuses'},
            {'id': 'incomplete', 'text': 'Incomplete', 'pid': 'statuses', 'selected': True},
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
            'placeholder': ''
        })
        self.dropdown_tree.addEventListener('close', self.handler_filter_close)

        # Status filter
        # status_data = [
        #     {'Id': 'all', 'Text': 'All statuses', 'IconCss': 'e-icons e-badminton'},
        #     {'Id': 'complete', 'Text': 'Complete', 'IconCss': 'e-icons e-badminton'},
        #     {'Id': 'incomplete', 'Text': 'Incomplete', 'IconCss': 'e-icons e-cricket'},
        # ]
        # item_template = '<div><span class="${IconCss}"></span>${Text}</div>'

        # self.filter_complete = ej.dropdowns.ComboBox({
        #     'dataSource': status_data,
        #     'fields': { 'value': 'Id', 'text': 'Text'},
        #     'iconTemplate': item_template,
        #     'placeholder': 'Complete...',
        #     'cssClass': 'e-outline',
        #     'value': 'incomplete'
        # })
        # self.filter_complete.addEventListener('change', self.handler_filter_complete)

        # # Assigned filter
        # staff_data = Staff.search()
        # staff_data_for_combobox = [{'Id': row['uid'], 'Text': row['first_name'] + " " + row['last_name']} for row in staff_data]
        # staff_data_for_combobox.insert(0, {'Id': 'all', 'Text': 'All staffs'})
        
        # self.filter_staff = ej.dropdowns.ComboBox({
        #     'dataSource': staff_data_for_combobox,
        #     'fields': {'value': 'Id', 'text': 'Text'},
        #     'placeholder': 'Staff...',
        #     'value': 'all'
        # })
        # self.filter_staff.addEventListener('change', self.handler_filter_staff)
        
        # # Cases filter
        # cases_data = Case.search()
        # cases_data_for_combobox = [{'Id': row['uid'], 'Text': row['case_name']} for row in cases_data]
        # cases_data_for_combobox.insert(0, {'Id': 'all', 'Text': 'All cases'})
        # self.filter_case = ej.dropdowns.ComboBox({
        #     'dataSource': cases_data_for_combobox,
        #     'fields': {'value': 'Id', 'text': 'Text'},
        #     'placeholder': 'Cases...',
        # })
        # self.filter_case.addEventListener('change', self.handler_filter_cases)

    def init_events(self):
        self.grid.addEventListener('dataBound', self.handler_databound)
        # self.grid.addEventListener('actionCompltete', self.handle_actionComplete)

    def due_date_caption(self, args):
        caption_color = 'color:#a63333;' if args['key'] == -100 else ''
        return (f'<div class="template" style="font-size:14px;font-weight:bold;{caption_color}">'
                f'{args.items[0].due_date_view}</div>')

    def form_show(self, get_data=True, **args):
        print("TaskListView/form_show")
        super().form_show(get_data=get_data, **args)
        self.dropdown_tree.appendTo(jQuery(f"#{self.filter_el_id}")[0])
        jQuery("#pm-filter-container .e-icons.e-ddt-icon")[0].style.color = "rgb(0 147 255)"
        # self.add_filter_component('Completion Status', self.filter_complete)
        # self.add_filter_component('Assigned to', self.filter_staff)
        # self.add_filter_component('By Case', self.filter_case)

        self.invalidate()

    def collapse_all(self, args):
        if self.first_load:
            self.grid.groupModule.collapseAll()
            self.first_load = False

    # Handle complete filter
    # def handler_filter_complete(self, args):
    #     if args['itemData'] is None:
    #         self.grid.clearFiltering(['completed'])
    #     elif args['itemData']['Id'] == 'complete':
    #         self.grid.filterByColumn('completed', 'equal', "true")
    #     elif args['itemData']['Id'] == 'incomplete':
    #         self.grid.filterByColumn('completed', 'notequal', 'true')
    #     else:
    #         self.grid.clearFiltering(['completed'])

    # # Handle staff filter
    # def handler_filter_staff(self, args):
    #     if args['itemData']['Id'] == 'all':
    #         self.grid.clearFiltering(['assigned_staff__full_name'])
    #     else:
    #         self.grid.filterByColumn('assigned_staff__full_name', 'contains', args['itemData']['Text'])

    # # Handle cases filter
    # def handler_filter_cases(self, args):
    #     if args['itemData']['Id'] == 'all':
    #         self.grid.clearFiltering(['case__case_name'])
    #     else:
    #         self.grid.filterByColumn('case__case_name', 'equal', args['itemData']['Text'])

    def handler_filter_close(self, args):
        tree_data = self.dropdown_tree.getData()
        all_status = tree_data[0].get('selected', False)
        filter_complete = tree_data[1].get('selected', False)
        filter_incomplete = tree_data[2].get('selected', False)
        all_cases = tree_data[3].get('selected', False)
        all_staffs = tree_data[4].get('selected', False)
        all_activities = tree_data[5].get('selected', False)
        selected_items = [item for item in tree_data if item.get('selected')]

        self.cases_filters = []
        self.staffs_filters = []
        self.activity_filters = []

        for item in selected_items:
            if not all_cases and item.get('pid') == 'cases':
                self.cases_filters.append(item['id'])
            if not all_staffs and item.get('pid') == 'staffs':
                self.staffs_filters.append(item['id'])
            if not all_activities and item.get('pid') == 'activities':
                self.activity_filters.append(item['id'])

        if filter_complete:
            self.param_complete = [True]
        if filter_incomplete:
            self.param_complete = [False, None]
        if not filter_complete and not filter_incomplete or all_status:
            self.param_complete = [True, False, None]
        self.get_tasks_filter()
        if selected_items:
            jQuery("#pm-filter-container .e-icons.e-ddt-icon")[0].style.color = "rgb(0 147 255)"
            # self.grid.element.querySelector(f'#pm-filter-container .e-icons.e-input-group-icon.e-ddt-icon::before').content = "\e735"
        else:
            jQuery("#pm-filter-container .e-icons.e-ddt-icon")[0].style.color = "#6b7280"
            # self.grid.element.querySelector(f'#pm-filter-container .e-icons.e-input-group-icon.e-ddt-icon::before').content = "\e72c"
        self.grid.refresh()

    def handler_databound(self, args):
        self.invalidate()

    def handle_actionComplete(self, args):
        self.invalidate()

    def get_tasks_filter(self):
        tasks = anvil.server.call('get_tasks_filter', self.cases_filters, self.staffs_filters, self.activity_filters, None, None, self.param_complete)
        self.grid_data = []
        for task in tasks:
            item = {}
            item['due_date'] = task['due_date'].strftime("%Y-%m-%d") if task['due_date'] else None
            item['due_date_days'] = Task.get_due_date_days(task)
            item['uid'] = task['uid']
            item['completed'] = task['completed']
            item['assigned_staff__full_name'] = ' '.join([f"{staff['first_name']} {staff['last_name']}" for staff in task['assigned_staff']])
            item['activity__name']  = task['activity']['name'] if task['activity'] and task['activity']['name'] else ""
            item['priority'] = task['priority']
            item['case__case_name'] = task['case']['case_name'] if task['case'] and task['case']['case_name'] else ""
            item['due_date_view'] = Task.get_due_date_view(task)
            item['notes'] = task['notes']
            self.grid_data.append(item)
        self.grid['dataSource'] = self.grid_data

    def invalidate(self):
        rows = self.grid.element.querySelectorAll('.e-content .e-table .e-row')
        data = self.grid['dataSource']
        for ind, row in enumerate(rows):
            if row.querySelector('td:nth-child(5)').textContent == 'true':
                row.classList.add('task-complete')
                row.classList.remove('task-incomplete')
            else:
                row.classList.add('task-incomplete')
                row.classList.remove('task-complete')

        for ind, item in enumerate(data):
            if item['due_date'] is None:
                data[ind]['due_date'] = "No Due Date"
            if item['priority'] == 'High':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-red'></span> High"
            elif item['priority'] == 'Normal':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-green'></span> Normal"

    def update_grid(self, data_row, add_new, get_relationships=False):
        if data_row.uid is None:
            data_row.uid = f"grid_{uuid.uuid4()}"
        grid_row = self.get_style_row(data_row, get_relationships)
        self.update_grid_style(grid_row, add_new, get_relationships)

    # Get completed, priority components with style
    def get_style_row(self, data_row, get_relationships):
        grid_row = data_row.get_row_view(
            self.view_config['columns'],
            include_row=False,
            get_relationships=get_relationships,
        )
        if grid_row['priority'] == 'High':
            grid_row['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-red'></span> High"
        elif grid_row['priority'] == 'Normal':
            grid_row['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-green'></span> Normal"
        # grid_row['completed'] = f"<span class='fas fa-check fa-2x {'text-green' if grid_row['completed'] else 'text-muted'}'></span>"
        return grid_row
    
    def commandClick(self, args):
        obj = Task.get(args['rowData']['uid'])
        obj.update({'completed': not obj['completed']})
        obj.save()
        self.update_grid(obj, False)

    def row_selected(self, args):
        jQuery(f"#details_content")[0].innerHTML = self.details_content(args['data'])
        super().row_selected(args)
        
    def details_content(self, task):
        item = Task.get(task['uid'])
        content = "<div class='details_title'>Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Task Status</div>\
                <div class='details_record_data'>{'Complete' if task['completed'] else 'Incomplete'}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Due Date</div>\
                <div class='details_record_data'>{task['due_date_view']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Priority</div>\
                <div class='details_record_data'>{task['priority']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Details</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Case</div>\
                <div class='details_record_data'>{task['case__case_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Assigned Staff</div>\
                <div class='details_record_data'>{task['assigned_staff__full_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Notes</div>\
                <div class='details_record_data'>{task['notes']}</div>\
            </div>\
        <div>"
        return content
