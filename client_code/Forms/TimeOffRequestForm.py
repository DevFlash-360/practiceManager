import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *
from .. import Forms
from datetime import datetime, timedelta


STATUS_INVOICED = 'Approved'
STATUS_OPEN = 'Open'
STATUS_OPTIONS = [
    STATUS_INVOICED,
    STATUS_OPEN,
]
class TimeOffRequestForm(FormBase):

    def __init__(self, **kwargs):

        kwargs['model'] = 'TimeOffRequest'
        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name')
        self.reason = TextInput(name='reason', label='Reason')
        self.date_of_return = DateInput(name='date_of_return', label='Date Of Return', string_format='MMM dd, yyyy')
        self.date_of_leave = DateInput(name='date_of_leave', label='Date Of Leave', string_format='MMM dd, yyyy')
        self.status = DropdownInput(name='status', label='Status', options=STATUS_OPTIONS)
        self.notes = MultiLineInput(name='notes', label="Notes", rows=4)
        
        sections = [
            {'name': '_', 'rows': [
                [self.staff],
                [self.reason],
                [self.date_of_return],
                [self.date_of_leave],
                [self.status],
                [self.notes]
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL1, **kwargs)
