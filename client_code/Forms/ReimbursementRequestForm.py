import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
import datetime
from ..app.models import Staff


class ReimbursementRequestForm(FormBase):
    def __init__(self, **kwargs):
        kwargs['model'] = 'ReimbursementRequest'
        
        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name')
        self.activity = LookupInput(model='Activity', name='activity', label='Event Type')
        self.description = MultiLineInput(name='description', label='Description')
        self.date = DateInput(name='date', label='Date', value=datetime.date.today(), string_format='MMM dd, yyyy')
        self.amount = NumberInput(name='amount', label='Amount', value=0)
        self.quantity = NumberInput(name='quantity', label='Quantity', value=1)
        self.total = NumberInput(name='total', label='Total')
        self.receipt_invoice = FileUploadInput(name='receipt_invoice', label='Receipt Invoice', save=False)
        self.add_to_case = CheckboxInput(name='add_to_case', label='Add matching case expense', value=False, on_change=self.on_change_matching_case)
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.payroll = LookupInput(name='payroll', label='Payroll', model='Payroll', text_field='staffs.full_name')
        sections = [
            {'name': '_', 'rows': [
                [self.staff, self.add_to_case],
                [self.activity, self.case],
                [self.description],
                [self.date],
                [self.quantity],
                [self.amount],
                [self.receipt_invoice],
                # hidden fields
                [self.total],
                [self.payroll],
            ]}
        ]
        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
    
    def form_open(self, args):
        super().form_open(args)
        self.total.hide()
        self.payroll.hide()

    def form_save(self, args):
        total = self.amount.value * self.quantity.value
        self.total.value = total

        super().form_save(args)
    
    def on_change_matching_case(self, args):
        if self.add_to_case.value:
            self.case.show()
        else:
            self.case.hide()
