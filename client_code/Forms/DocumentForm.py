from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from ..app.models import Document


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
        self.upload_files = FileUploadInput(
            name='upload_files', label='Upload File(s)', multiple=True, required=True, save=False,
            storage_config={'type': 'aws_s3', 'key_prefix': f"documents"},
        )
        self.file = HiddenInput(name='file')

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
                [self.upload_files]
            ]}
        ]

        validation = {
            'rules': {
                self.case.el_id: {'required': True},
                self.folder.el_id: {'required': True},
                self.type.el_id: {'required': True},
            }
        }

        super().__init__(sections=sections, validation=validation, width=POPUP_WIDTH_COL3, **kwargs)
        # self.form_fields.append(self.file)


    def form_open(self, args):
        super().form_open(args)
        self.file.hide()


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
            self.upload_files.enabled = False
        else:
            self.type.enabled = True
            self.discovery.enabled = True
            self.reviewed_by.enabled = True
            self.notes.enabled = True
            self.upload_files.enabled = True

    # def form_validate(self):
    #     if not self.upload_files.value:
    #         self.upload_files.show_required()
    #         return False
    #     else:
    #         return super().form_validate()

    def form_save(self, args):
        if not self.upload_files.value:
            self.upload_files.show_required()
        else:
            document_data = {
                'case': self.case.value,
                'folder': self.folder.value,
                'type': self.type.value,
                'discovery': self.discovery.value,
                'reviewed_by': self.reviewed_by.value,
                'notes': self.notes.value,
            }
            for file in self.upload_files.value:
                document_data['file'] = file
                Document(**document_data).save()
            self.form_cancel(args)
