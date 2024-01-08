import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *


class DocumentFolderForm(FormBase):

    def __init__(self, **kwargs):
        print('DocumentFolderForm')
        kwargs['model'] = 'DocumentFolder'
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.name = TextInput(name='name', label='Folder Name')

        fields = [self.case, self.name]

        validation = {
            'rules': {
                self.name.el_id: {'required': True},
            }
        }

        super().__init__(fields=fields, header='New Folder', validation=validation, width=POPUP_WIDTH_COL1, **kwargs)


    def form_open(self, args):
        super().form_open(args)
        self.case.enabled = False
