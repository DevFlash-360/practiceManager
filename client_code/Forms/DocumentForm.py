from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *


DOCUMENT_TYPES = [
    'Hardcopy',
    'Digital',
    'Disc',
    'USB Stick',
    'Hard Drive',
]


class DocumentForm(FormBase):

    def __init__(self, **kwargs):
        print('DocumentForm')
        kwargs['model'] = 'Document'
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name',
                                on_change=self.case_selected)
        self.folder = LookupInput(name='folder', label='Folder', model='DocumentFolder', text_field='name',
                                  add_item_label='Create Folder', add_item_form=FormBase,
                                  on_change=self.folder_selected)
        self.type = DropdownInput(name='type', label='Document Type', options=DOCUMENT_TYPES)
        self.discovery = CheckboxInput(name='discovery', label='Mark as Discovery')
        self.reviewed_by = LookupInput(name='reviewed_by', label='Reviewed By', model='Staff', text_field='full_name')
        self.notes = MultiLineInput(name='notes', label='Notes', rows=7)
        self.files = FileUploadInput(name='file', label='Upload File', on_change=self.file_selected)

        sections = [
            {'name': '_', 'cols': [
                [
                    self.case,
                    self.folder,
                    self.type,
                    self.reviewed_by,
                ],
                [
                    self.discovery,
                    self.notes,
                ]
            ]},
            {'name': 'File', 'rows': [
                [self.files]
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)


    def case_selected(self, args):
        if self.case.value is None or not args.get('value'):
            self.folder.enabled = False
        else:
            self.folder.enabled = True
            self.folder_selected({})


    def folder_selected(self, args):
        if self.folder.value is None or not args.get('value'):
            self.type.enabled = False
            self.discovery.enabled = False
            self.reviewed_by.enabled = False
            self.notes.enabled = False
            self.files.enabled = False
        else:
            self.type.enabled = True
            self.discovery.enabled = True
            self.reviewed_by.enabled = True
            self.notes.enabled = True
            self.files.enabled = True

    def file_selected(self, args):
        print('file_selected', args, self.files.value)
