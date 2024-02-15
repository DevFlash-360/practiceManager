import anvil.server
from AnvilFusion.components.FormBase import FormBase, SubformBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.datamodel.types import FieldTypes
from ..Forms.PaymentForm import PAYMENT_METHOD_OPTIONS, PAYMENT_STATUS_OPTIONS


# expense status options
INVOICE_STATUS_DRAFT = 'draft'
INVOICE_STATUS_APPROVED = 'approved'
INVOICE_STATUS_DUE = 'due'
INVOICE_STATUS_PAID = 'paid'
INVOICE_STATUS_VOID = 'void'
INVOICE_STATUS_OPTIONS = [
    INVOICE_STATUS_DRAFT,
    INVOICE_STATUS_APPROVED,
    INVOICE_STATUS_DUE,
    INVOICE_STATUS_PAID,
    INVOICE_STATUS_VOID,
]


class InvoiceForm(FormBase):
    def __init__(self, **kwargs):
        print('InvoiceForm')
        kwargs['model'] = 'Invoice'
        self.invoice_number = NumberInput(name='invoice_number', label='Invoice Number')
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.bill_to = LookupInput(name='bill_to', label='Bill To', model='Contact', text_field='full_name')
        self.fee_type = LookupInput(model='FeeType', name='fee_type', label='Fee Type')
        self.total = NumberInput(name='total', label='Total')
        self.balance_due = NumberInput(name='balance_due', label='Balance Due')
        self.status = DropdownInput(name='status', label='Status', options=INVOICE_STATUS_OPTIONS)

        payment_fields = [
            DateTimeInput(name='payment_time', label='Payment Time'),
            NumberInput(name='amount', label='Amount', field_type=FieldTypes.CURRENCY),
            DropdownInput(name='payment_method', label='Payment Method', options=PAYMENT_METHOD_OPTIONS),
            DropdownInput(name='status', label='Status', options=PAYMENT_STATUS_OPTIONS),
        ]
        payments_view = {
            'model': 'Payment',
            'columns': [
                {'name': 'payment_time', 'label': 'Payment Time'},
                {'name': 'amount', 'label': 'Amount'},
                {'name': 'payment_method', 'label': 'Payment Method'},
                {'name': 'status', 'label': 'Status'},
            ],
            'inline_edit_fields': payment_fields,
        }
        self.payments = SubformGrid(
            name='payments', label='Payments', model='Payment',
            link_model='Invoice', link_field='invoice',
            view_config=payments_view, edit_mode='inline',
        )

        time_entries_view = {
            'model': 'TimeEntry',
            'columns': [
                {'name': 'date', 'label': 'Date'},
                {'name': 'staff.full_name', 'label': 'Staff'},
                {'name': 'activity.name', 'label': 'Activity'},
                {'name': 'description', 'label': 'Description'},
                {'name': 'billable', 'label': 'Billable'},
                {'name': 'rate_type', 'label': 'Rate Type'},
                {'name': 'rate', 'label': 'Rate'},
                {'name': 'duration', 'label': 'Duration'},
                {'name': 'total', 'label': 'Total'},
            ],
        }
        self.time_entries = SubformGrid(
            name='time_entries', label='Time Entry', model='TimeEntry',
            add_edit_form='TimeEntryForm', form_container_id=kwargs.get('target'),
            link_model='Invoice', link_field='invoice',
            view_config=time_entries_view,
        )

        expenses_view = {
            'model': 'Expense',
            'columns': [
                {'name': 'date', 'label': 'Date'},
                {'name': 'staff.full_name', 'label': 'Staff'},
                {'name': 'activity.name', 'label': 'Activity'},
                {'name': 'description', 'label': 'Description'},
                {'name': 'amount', 'label': 'Amount'},
                {'name': 'quantity', 'label': 'Quantity'},
                {'name': 'reduction', 'label': 'Reduction'},
                {'name': 'total', 'label': 'Total'},
                {'name': 'billable', 'label': 'Billable'},
                {'name': 'status', 'label': 'Status'},
            ],
        }
        self.expenses = SubformGrid(
            name='expenses', model='Expense',
            link_model='Invoice', link_field='invoice',
            add_edit_form='ExpenseForm', form_container_id=kwargs.get('target'),
            view_config=expenses_view,
        )

        adjustment_fields = [
            DropdownInput(name='type', label='Type', options=['Add', 'Discount']),
            DropdownInput(name='applied_to', label='Applied To',
                          options=['Flat Fees', 'Time Entries', 'Expenses', 'Sub-Total']),
            MultiLineInput(name='description', label='Description'),
            NumberInput(name='basis', label='Basis'),
            NumberInput(name='adjustment_amount', label='Adjustment $'),
            NumberInput(name='adjustment_percent', label='Adjustment %'),
        ]
        adjustments_view = {
            'inline_edit_fields': adjustment_fields,
        }
        self.adjustments = SubformGrid(
            name='adjustments', label='Adjustments',
            view_config=adjustments_view, edit_mode='inline',
        )

        sections = [
            {'name': '_', 'rows': [
                [self.case, self.fee_type],
                [self.invoice_number, self.total],
                [self.bill_to, self.balance_due],
                [None, self.status],
            ]},
            {'name': 'time_entries', 'label': 'Time Entries', 'rows': [[self.time_entries]]},
            {'name': 'expenses', 'label': 'Expenses', 'rows': [[self.expenses]]},
            {'name': 'adjustments', 'label': 'Adjustments', 'rows': [[self.adjustments]]},
            {'name': 'payments', 'label': 'Payments', 'rows': [[self.payments]]},
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
        self.fullscreen = True
