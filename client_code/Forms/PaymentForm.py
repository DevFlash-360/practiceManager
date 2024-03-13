import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *

from ..app.models import PerformanceIncentive, Staff

# payment method options
PAYMENT_METHOD_CARD = 'Card'
PAYMENT_METHOD_CASH = 'Cash'
PAYMENT_METHOD_CHECK = 'Check'
PAYMENT_METHOD_DIRECT_DEPOSIT = 'Direct Deposit'
PAYMENT_METHOD_WIRE_TRANSFER = 'Wire Transfer'
PAYMENT_METHOD_OPTIONS = [
    PAYMENT_METHOD_CARD,
    PAYMENT_METHOD_CASH,
    PAYMENT_METHOD_CHECK,
    PAYMENT_METHOD_DIRECT_DEPOSIT,
    PAYMENT_METHOD_WIRE_TRANSFER,
]

# payment status options
PAYMENT_STATUS_SUCCESS = 'Approved'
PAYMENT_STATUS_REFUND = 'Refunded'
PAYMENT_STATUS_CHARGEBACK = 'Dispute'
PAYMENT_STATUS_OPTIONS = [
    PAYMENT_STATUS_SUCCESS,
    PAYMENT_STATUS_REFUND,
    PAYMENT_STATUS_CHARGEBACK,
]


class PaymentForm(FormBase):
    def __init__(self, **kwargs):
        print('PaymentForm')
        kwargs['model'] = 'Payment'
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.invoice = LookupInput(name='invoice', label='Invoice', model='Invoice', text_field='invoice_number')
        self.bank_account = LookupInput(model='BankAccount', name='bank_account', label='Bank Account')
        self.amount = NumberInput(name='amount', label='Amount')
        self.payment_method = DropdownInput(name='payment_method', label='Payment Method', select='single',
                                            options=PAYMENT_METHOD_OPTIONS)
        self.payment_time = DateTimeInput(name='payment_time', label='Payment Time')
        self.status = DropdownInput(name='status', label='Status', select='single', options=PAYMENT_STATUS_OPTIONS)

        sections = [
            {'name': '_', 'rows': [
                [self.bank_account, self.case],
                [self.payment_method, self.invoice],
                [self.amount, None],
                [self.payment_time, self.status],
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
        
    def form_save(self, args):
        super().form_save(args)



        # Calculate performance incentives
        assigned_attorneys = self.data.case.assigned_attorneys
        assigned_attorney_ids = [member.uid for member in assigned_attorneys]
        assigned_staffs = self.data.case.staff
        assigned_staff_ids = [member.uid for member in assigned_staffs]
        all_staffs = Staff.search()
        
        eligible_cnt = len(assigned_staffs)
        for staff in assigned_staffs:
            if staff.staff_group.name == 'Attorney':
                eligible_cnt = eligible_cnt - 1
        
        if self.action == 'edit':
            incentives = PerformanceIncentive.search(payment=self.data.uid)
            for incentive in incentives:
                print(incentive)

        elif self.action == 'add':
            for staff in assigned_staffs:
                if staff['enable_performance_incentives'] and staff['intake_performance_incentive']:
                    div_cnt = 1 if staff.staff_group.name == 'Attorney' else eligible_cnt
                    incentive = PerformanceIncentive(
                        staff=staff,
                        amount=staff['intake_performance_incentive']*self.data.amount/div_cnt,
                        payment=self.data
                    )
                    incentive.save()
            
            for staff in assigned_attorneys:
                if staff['enable_performance_incentives'] and staff['intake_performance_incentive'] and staff.uid not in assigned_staff_ids:
                    incentive = PerformanceIncentive(
                        staff=staff,
                        amount=staff['intake_performance_incentive']*self.data.amount,
                        payment=self.data
                    )
                    incentive.save()
            
            for staff in all_staffs:
                if staff['override_incentive'] and staff.uid not in assigned_attorney_ids and staff.uid not in assigned_staff_ids:
                    incentive = PerformanceIncentive(
                        staff=staff,
                        amount=staff['override_incentive']*self.data.amount,
                        payment=self.data
                    )
                    incentive.save()
