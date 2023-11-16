from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *
from datetime import datetime


class AssistantForm(FormBase):
    def __init__(self, **kwargs):
        print('AssistantForm')
        kwargs['model'] = 'Assistant'
        self.user_message = MultiLineInput(name='user_message', label='')
        self.thread = InlineMessage(name='thread')

        fields = [
            self.thread,
            self.user_message,
        ]


        super().__init__(fields=fields, width=POPUP_WIDTH_COL1, **kwargs)
