from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid


class DocumentFolderForm(FormBase):

    def __init__(self, **kwargs):
        print('DocumentFolderForm')
        kwargs['model'] = 'DocumentFolder'
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.name = TextInput(name='name', label='Name')
        self.documents = SubformGrid(name='documents', label='Documents', model='Document', text_field='name')

        sections = [
            {'name': '_', 'rows': [
                [self.case, self.name],
                [self.documents],
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL1, **kwargs)
