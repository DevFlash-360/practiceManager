import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from datetime import datetime


class PerformanceIncentiveForm(FormBase):
    def __init__(self, **kwargs):
        kwargs['model'] = 'PerformanceIncentive'

        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name')
        self.amount = NumberInput(name='amount', label='Amount', value=0)
        self.payment = LookupInput(name='payment', label='Payment', model='Payment')
        self.payment_date = DateTimeInput(name='payment_date', label='Date', value=datetime.now(), string_format='MMM dd, yyyy')
        self.payroll = LookupInput(name='payroll', label='Payroll', model='Payroll', text_field='staffs.full_name')

        sections = [
            {'name': '_', 'rows': [
                [self.staff, self.amount],
                [self.payment, self.payment_date],
                # hidden fields
                [self.payroll],
            ]}
        ]
        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        self.payroll.hide()
