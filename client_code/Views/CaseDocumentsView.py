from AnvilFusion.components.GridView import GridView
import anvil.js
import uuid


def folder_header(args):
    print('folder_header', args)
    return f'{args["key"]} ({len(args["items"])} files)'


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

        caption_id = uuid.uuid4()
        self.caption_template = (f'<script id="{caption_id}" type="text/x-template"><div>'
                                 f'${{folder_header(args)}}</div></script>')

        super().__init__(model='Document', view_config=view_config, filters=filters, **kwargs)
        self.grid.allowGrouping = True
        self.grid.groupSettings = {
            'columns': ['folder'],
            'showDropArea': False,
            'captionTemplate': f'#{caption_id}',
        }


    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
        folder_header_el = anvil.js.window.createElement(self.caption_template)
        self.grid.element.appendChild(folder_header_el)
