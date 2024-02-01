import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid


class CaseDocumentsView(GridView):
    def __init__(self, case=None, case_uid=None, **kwargs):
        print('CaseDocumentsView')
        self.filter_case_uid = None
        is_dashboard = kwargs.pop('dashboard', None)
        if is_dashboard:
            self.filter_case_uid = get_cookie('case_uid')

        view_config = {
            'model': 'Document',
            'columns': [
                {'name': 'folder.name', 'label': 'Folder'},
                {'name': 'title', 'label': 'Document Title'},
                {'name': 'file.name', 'label': 'File Name'},
                {'name': 'type', 'label': 'Type'},
                {'name': 'discovery', 'label': 'Discovery'},
                {'name': 'reviewed_by.full_name', 'label': 'Reviewed By'},
                {'name': 'notes', 'label': 'Notes'},
            ],
            'filter': {'document_folder.case': self.filter_case_uid},
        }
        if self.filter_case_uid:
            filters = {
                'case': {'uid': self.filter_case_uid}
            }
        else:
            filters = None

        super().__init__(model='Document', view_config=view_config, filters=filters, **kwargs)
        self.grid.allowGrouping = True
        self.grid.groupSettings = {
            'columns': ['folder__name'],
            'showDropArea': False,
            'captionTemplate': '<div>${key} - ${count} files</div>',
        }
        # self.grid.editSettings = {
        #     'allowEditing': True,
        #     'allowAdding': False,
        #     'allowDeleting': True,
        #     'mode': 'Normal',
        # }
        self.grid.dataBound = self.collapse_all
        self.first_load = True


    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)


    def collapse_all(self, args):
        if self.first_load:
            self.grid.groupModule.collapseAll()
            self.first_load = False
