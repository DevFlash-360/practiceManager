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
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.folder = LookupInput(name='folder', label='Folder', model='DocumentFolder', text_field='name',
                                  add_item_label='Create Folder', add_item_form=FormBase)
        self.type = DropdownInput(name='type', label='Document Type', options=DOCUMENT_TYPES)
        self.discovery = CheckboxInput(name='discovery', label='Mark as Discovery')
        self.reviewed_by = LookupInput(name='reviewed_by', label='Reviewed By', model='Staff', text_field='full_name')
        self.notes = MultiLineInput(name='notes', label='Notes', rows=6)
        self.file = FileUploadInput(name='file', label='Upload File')

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
                [self.file]
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
