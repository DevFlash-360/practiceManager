import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
import datetime


class ExpenseForm(FormBase):
    def __init__(self, **kwargs):
        print('ExpenseForm')
        kwargs['model'] = 'Expense'
        self.date = DateInput(name='date', label='Date', value=datetime.date.today(), string_format='MMM dd, yyyy')
        self.activity = LookupInput(model='Activity', name='activity', label='Activity')
        self.description = MultiLineInput(name='description', label='Description')
        self.amount = NumberInput(name='amount', label='Amount', value=0)
        self.quantity = NumberInput(name='quantity', label='Quantity', value=1)
        self.total = NumberInput(name='total', label='Total')
        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name')
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.billable = CheckboxInput(name='billable', label='Billable', value=True)
        self.reduction = NumberInput(name='reduction', label='Reduction')
        self.receipt_invoice = FileUploadInput(name='receipt_invoice', label='Receipt Invoice', save=False)

        sections = [
            {'name': '_', 'rows': [
                [self.case],
                [self.activity, self.staff],
                [self.description],
                [self.billable],
                [self.date, self.amount, self.quantity, self.reduction],
                [self.receipt_invoice],
                # hidden fields
                [self.total],
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        self.total.hide()

    def form_save(self, args):
        total = self.amount.value * self.quantity.value
        if self.reduction.value is not None:
            total -= self.reduction.value
        self.total.value = total

        super().form_save(args)
