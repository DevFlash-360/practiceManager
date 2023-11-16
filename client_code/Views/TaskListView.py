from AnvilFusion.components.GridView import GridView
import anvil.js

GRID_TOOLBAR_COMMAND_ADD = {'id': 'add', 'text': '', 'prefixIcon': 'e-add', 'tooltipText': 'Add', 'align': 'Right'}
GRID_TOOLBAR_COMMAND_DELETE = {'id': 'delete', 'text': '', 'prefixIcon': 'e-delete', 'tooltipText': 'Delete',
                               'align': 'Right', 'style': 'color: #d6292c;'}
GRID_TOOLBAR_COMMAND_SEARCH = {'id': 'search', 'text': 'Search', 'prefixIcon': 'e-search', 'tooltipText': 'Search',
                               'align': 'Right'}
GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE = {'id': 'search-toggle', 'text': '', 'prefixIcon': 'e-search',
                                      'tooltipText': 'Search', 'align': 'Right'}

GRID_TOOLBAR_COMMAND_PRINT = {'id': 'print', 'text': '', 'prefixIcon': 'print',
                                      'tooltipText': 'Print', 'align': 'Right'}

TOOLBAR_ITEMS = [
    GRID_TOOLBAR_COMMAND_DELETE,
    GRID_TOOLBAR_COMMAND_SEARCH,
    GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
    GRID_TOOLBAR_COMMAND_ADD,
    GRID_TOOLBAR_COMMAND_PRINT
]
class TaskListView(GridView):
    def __init__(self, case=None, case_uid=None, **kwargs):
        print('TaskListView')
        view_config = {
            'model': 'Task',
            'columns': [
                {'name': 'completed', 'label': 'Completed'},
                {'name': 'due_date_days', 'label': 'Due Date'},
                {'name': 'due_date_view', 'label': 'Due Date', 'visible': False},
                {'name': 'due_date', 'label': 'Due Date', 'customAttributes': {'class':'bold'}},
                {'name': 'case.case_name', 'label': 'Case'},
                {'name': 'activity.name', 'label': 'Activity', 'customAttributes': {'class':'bold'}},
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

        super().__init__(model='Task', view_config=view_config, filters=filters, toolbar_items=TOOLBAR_ITEMS, **kwargs)
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


    def due_date_caption(self, args):
        # print('due_date_caption', args)
        caption_color = 'color:#a63333;' if args['key'] == -100 else ''
        return (f'<div class="template" style="font-size:14px;font-weight:bold;{caption_color}">'
                f'{args.items[0].due_date_view}</div>')
        # return args['due_date']


    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)


    def collapse_all(self, args):
        if self.first_load:
            self.grid.groupModule.collapseAll()
            self.first_load = False
