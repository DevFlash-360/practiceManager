import uuid
import anvil.server
from anvil.js.window import ej, jQuery
from DevFusion.components.GridView2 import GridView2
import anvil.js

class TaskListView(GridView2):
    def __init__(self, case=None, case_uid=None, **kwargs):
        print('TaskListView')
        view_config = {
            'model': 'Task',
            # 'commandClick': self.commandClick,
            'columns': [
                {'name': 'completed', 'label': 'Completed', 'custom_attributes': {}},
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
        # self.grid.editSettings = {
        #     'allowEditing': True,
        #     'allowAdding': False,
        #     'allowDeleting': True,
        #     'mode': 'Normal',
        # }
        # self.grid.dataBound = self.collapse_all
        self.first_load = True

        self.init_filters()

        self.grid_config['actionBegin'] = self.grid_action_handler
        self.grid_config['actionComplete'] = self.grid_action_handler

    def init_filters(self):
        # Status filter
        status_data = [
            {'Id': 'all', 'Text': 'All statuses', 'IconCss': 'e-icons e-badminton'},
            {'Id': 'complete', 'Text': 'Complete', 'IconCss': 'e-icons e-badminton'},
            {'Id': 'incomplete', 'Text': 'Incomplete', 'IconCss': 'e-icons e-cricket'},
        ]
        item_template = '<div><span class="${IconCss}"></span>${Text}</div>'

        self.filter_complete = ej.dropdowns.ComboBox({
            'dataSource': status_data,
            'fields': { 'value': 'Id', 'text': 'Text'},
            'iconTemplate': item_template,
            'placeholder': 'Complete...',
            'cssClass': 'e-outline'
        })
        self.filter_complete.addEventListener('change', self.handler_filter_complete)

        # Assigned filter
        staff_data = anvil.server.call('get_staff_data')
        staff_data_for_combobox = [{'Id': row['uid'], 'Text': row['first_name'] + " " + row['last_name']} for row in staff_data]
        staff_data_for_combobox.insert(0, {'Id': 'all', 'Text': 'All staffs'})

        self.filter_staff = ej.dropdowns.ComboBox({
            'dataSource': staff_data_for_combobox,
            'fields': {'value': 'Id', 'text': 'Text'},
            'placeholder': 'Staff...',
        })
        self.filter_staff.addEventListener('change', self.handler_filter_staff)
        
        # Cases filter
        cases_data = anvil.server.call('get_cases_data')
        cases_data_for_combobox = [{'Id': row['uid'], 'Text': row['case_name']} for row in cases_data]
        cases_data_for_combobox.insert(0, {'Id': 'all', 'Text': 'All cases'})
        self.filter_case = ej.dropdowns.ComboBox({
            'dataSource': cases_data_for_combobox,
            'fields': {'value': 'Id', 'text': 'Text'},
            'placeholder': 'Cases...',
        })
        self.filter_case.addEventListener('change', self.handler_filter_cases)
        

    def due_date_caption(self, args):
        caption_color = 'color:#a63333;' if args['key'] == -100 else ''
        return (f'<div class="template" style="font-size:14px;font-weight:bold;{caption_color}">'
                f'{args.items[0].due_date_view}</div>')
        # return args['due_date']


    def form_show(self, get_data=True, **args):
        print("TaskListView/form_show")
        super().form_show(get_data=get_data, **args)
        self.add_filter_component('Completion Status', self.filter_complete)
        self.add_filter_component('Assigned to', self.filter_staff)
        self.add_filter_component('By Case', self.filter_case)

        self.invalidate()

    def collapse_all(self, args):
        if self.first_load:
            self.grid.groupModule.collapseAll()
            self.first_load = False

    def commandClick(args):
        print(f"Click {args}")

    def handler_filter_complete(self, args):
        print(args)
        if args['itemData']['Id'] == 'complete':
            self.grid.filterByColumn('completed', 'equal', "<span class='fas fa-check fa-2x text-green'></span>")
        elif args['itemData']['Id'] == 'incomplete':
            self.grid.filterByColumn('completed', 'equal', "<span class='fas fa-check fa-2x text-muted'></span>")
        else:
            self.grid.clearFiltering(['completed'])

    def handler_filter_staff(self, args):
        if args['itemData']['Id'] == 'all':
            self.grid.clearFiltering(['assigned_staff__full_name'])
        else:
            self.grid.filterByColumn('assigned_staff__full_name', 'contains', args['itemData']['Text'])

    def handler_filter_cases(self, args):
        print(args)
        if args['itemData']['Id'] == 'all':
            self.grid.clearFiltering(['case__case_name'])
        else:
            self.grid.filterByColumn('case__case_name', 'equal', args['itemData']['Text'])

    def grid_action_handler(self, args):
        super().grid_action_handler(args)
        # self.invalidate()

    def invalidate(self):
        print("invalidate")
        data = self.grid['dataSource']
        for ind, item in enumerate(self.grid_data):
            data[ind]['completed'] = f"<span class='fas fa-check fa-2x {'text-green' if item['completed'] else 'text-muted'}'></span>"
            if item['priority'] == 'High':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-red'></span> High"
            elif item['priority'] == 'Normal':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-green'></span> Normal"

    def update_grid(self, data_row, add_new, get_relationships=False):
        print("GridView2/update_grid")
        if data_row.uid is None:
            data_row.uid = f"grid_{uuid.uuid4()}"
        grid_row = data_row.get_row_view(
            self.view_config['columns'],
            include_row=False,
            get_relationships=get_relationships,
        )
        self.update_grid_style(grid_row, add_new, get_relationships)