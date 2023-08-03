from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *


class CaseWorkflowForm(FormBase):
    def __init__(self, **kwargs):
        print('CaseWorkflowForm')
        self.check_number = TextInput(name='check_number', label='Check Number')
        self.date = DateInput(name='date', label='Date')
        self.payee = LookupInput(name='payee', label='Payee', model='Contact', text_field='full_name')
        self.amount = NumberInput(name='amount', label='Amount')
        self.memo = MultiLineInput(name='memo', label='Memo')
        self.reference = TextInput(name='reference', label='Reference')
        self.bank_account = LookupInput(name='bank_account', label='Bank Account', model='BankAccount')

        fields = [
            self.check_number,
            self.date,
            self.payee,
            self.amount,
            self.memo,
            self.reference,
            self.bank_account,
        ]

        # validation = {
        #     'rules': {
        #         self.check_number.el_id: {'required': True},
        #         self.date.el_id: {'required': True, 'date': True},
        #         self.payee.el_id: {'required': True},
        #         self.amount.el_id: {'required': True, 'regex': r'^[1-9]\d*(\.\d{2})?$'},
        #         self.bank_account.el_id: {'required': True},
        #     }
        # }

        super().__init__(model='CaseWorkflow', fields=fields, width=POPUP_WIDTH_COL2, validation=validation, **kwargs)
