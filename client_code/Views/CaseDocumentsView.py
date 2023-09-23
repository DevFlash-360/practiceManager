from AnvilFusion.components.GridView import GridView
import anvil.js
import uuid


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

        self.caption_el_id = uuid.uuid4()
        script_el = anvil.js.window.document.createElement('script')
        script_el.id = self.caption_el_id
        script_el.type = 'text/x-template'
        script_el.innerHTML = f'<div>${{folder_header(args)}}</div>'
        anvil.js.window.document.head.appendChild(script_el)

        super().__init__(model='Document', view_config=view_config, filters=filters, **kwargs)
        self.grid.allowGrouping = True
        self.grid.groupSettings = {
            'columns': ['folder'],
            'showDropArea': False,
            # 'captionTemplate': f'<div>${{{self.folder_header}}}</div>',
        }
        self.grid.dataBound = self.collapse_all
        self.first_load = True


    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
        # self.grid.groupModule.collapseAll()
        # print(self.grid.groupSettings.captionTemplate)


    def collapse_all(self, args):
        if self.first_load:
            self.grid.groupSettings.captionTemplate = '<div>${folder}</div>'
            self.grid.groupModule.collapseAll()
            self.first_load = False


    def folder_header(self, args):
        print('folder_header', args)
        return f'{args["key"]} ({len(args["items"])} files)'


