from AnvilFusion.components.GridView import GridView


class CaseDocumentsView(GridView):
    def __init__(self, case=None, case_uid=None, **kwargs):
        print('CaseDocumentsView')
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
            'filter': {'document_folder.case': kwargs.get('case_uid')},
        }
        case_uid = case['uid'] if case else case_uid
        if case_uid:
            filters = {
                'case': {'uid': case_uid}
            }
        else:
            filters = None

        super().__init__(model='Document', view_config=view_config, filters=filters, **kwargs)
        # super().__init__(model='Document', **kwargs)
        self.grid.allowGrouping = True
        self.grid.groupSettings = {'columns': ['folder'], 'showDropArea': False}
