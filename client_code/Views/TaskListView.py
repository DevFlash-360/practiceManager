import uuid
from anvil.js.window import ej, jQuery
from DevFusion.components.GridView2 import GridView2
import anvil.js
from ..app.models import Staff, Case, Task
class TaskListView(GridView2):
    def __init__(self, case=None, case_uid=None, **kwargs):
        print('TaskListView')
        view_config = {
            'model': 'Task',
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
        # staff_data = anvil.server.call('get_staff_data')
        staff_data = Staff.search()
        staff_data_for_combobox = [{'Id': row['uid'], 'Text': row['first_name'] + " " + row['last_name']} for row in staff_data]
        staff_data_for_combobox.insert(0, {'Id': 'all', 'Text': 'All staffs'})

        self.filter_staff = ej.dropdowns.ComboBox({
            'dataSource': staff_data_for_combobox,
            'fields': {'value': 'Id', 'text': 'Text'},
            'placeholder': 'Staff...',
        })
        self.filter_staff.addEventListener('change', self.handler_filter_staff)
        
        # Cases filter
        cases_data = Case.search()
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

    # Handle complete filter
    def handler_filter_complete(self, args):
        print(args)
        if args['itemData']['Id'] == 'complete':
            self.grid.filterByColumn('completed', 'equal', "<span class='fas fa-check fa-2x text-green'></span>")
        elif args['itemData']['Id'] == 'incomplete':
            self.grid.filterByColumn('completed', 'equal', "<span class='fas fa-check fa-2x text-muted'></span>")
        else:
            self.grid.clearFiltering(['completed'])

    # Handle staff filter
    def handler_filter_staff(self, args):
        if args['itemData']['Id'] == 'all':
            self.grid.clearFiltering(['assigned_staff__full_name'])
        else:
            self.grid.filterByColumn('assigned_staff__full_name', 'contains', args['itemData']['Text'])

    # Handle cases filter
    def handler_filter_cases(self, args):
        print(args)
        if args['itemData']['Id'] == 'all':
            self.grid.clearFiltering(['case__case_name'])
        else:
            self.grid.filterByColumn('case__case_name', 'equal', args['itemData']['Text'])

    def invalidate(self):
        print("invalidate")
        data = self.grid['dataSource']
        rows = self.grid.getRows()
        print(f"============== self.grid.element =============")
        print(rows)
        for ind, item in enumerate(self.grid_data):
            element = rows[ind]
            if item['completed']:
                data[ind]['completed'] = f"<span class='fas fa-check fa-2x 'task-complete text-green'></span>"
            else:
                data[ind]['completed'] = f"<span class='fas fa-check fa-2x 'task-incomplete text-muted'></span>"

            if item['priority'] == 'High':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-red'></span> High"
            elif item['priority'] == 'Normal':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-green'></span> Normal"

    def update_grid(self, data_row, add_new, get_relationships=False):
        print("TaskListView/update_grid")
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
        rows = self.grid.getRows()
        print(rows)

        # if grid_row['priority'] == 'High':
        #     grid_row['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-red'></span> High"
        # elif grid_row['priority'] == 'Normal':
        #     grid_row['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-green'></span> Normal"
        # grid_row['completed'] = f"<span class='fas fa-check fa-2x {'text-green' if grid_row['completed'] else 'text-muted'}'></span>"
        return grid_row
    
    def commandClick(self, args):
        obj = Task.get(args['rowData']['uid'])
        obj.update({'completed': not obj['completed']})
        obj.save()
        print(f"updated completed = {obj['completed']}")
        self.update_grid(obj, False)
