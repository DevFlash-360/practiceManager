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
        
        self.check_incomplete = ej.buttons.CheckBox({ 'label': 'Incomplete tasks only' })
        self.check_incomplete.addEventListener('change', self.unreadChange)

        self.grid.addEventListener('actionComplete', self.actionComplete)

    def due_date_caption(self, args):
        # print('due_date_caption', args)
        caption_color = 'color:#a63333;' if args['key'] == -100 else ''
        return (f'<div class="template" style="font-size:14px;font-weight:bold;{caption_color}">'
                f'{args.items[0].due_date_view}</div>')
        # return args['due_date']


    def form_show(self, get_data=True, **args):
        print("TaskListView/form_show")
        super().form_show(get_data=get_data, **args)
        self.check_incomplete.appendTo(jQuery(f"#{self.filters_el_id}")[0])

        self.invalidate()


    def collapse_all(self, args):
        if self.first_load:
            self.grid.groupModule.collapseAll()
            self.first_load = False

    def commandClick(args):
        print(f"Click {args}")

    def unreadChange(self, args):
        val = args['checked']
        if val:
            self.grid.filterByColumn('completed', 'equal', "<span class='fas fa-check fa-2x text-muted'></span>")
        else:
            self.grid.clearFiltering()

    def actionComplete(self, args):
        print("TaskListView/actionComplete")
        self.invalidate()

    def invalidate(self):
        data = self.grid['dataSource']
        for ind, item in enumerate(self.grid_data):
            data[ind]['completed'] = f"<span class='fas fa-check fa-2x {'text-green' if item['completed'] else 'text-muted'}'></span>"
            if item['priority'] == 'High':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-red'></span> High"
            elif item['priority'] == 'Normal':
                data[ind]['priority'] = f"<span class='fas fa-circle fa-sm me-1 text-green'></span> Normal"
        
