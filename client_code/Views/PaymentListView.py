import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid
from ..app.models import Staff, User


class PaymentListView(GridView):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Payment',
            'columns': [
                {'name': 'case.case_name', 'label': 'Case'},
                {'name': 'invoice.invoice_number', 'label': 'Activity'},
                {'name': 'bank_account.bank_name', 'label': 'Bank Account'},
                {'name': 'amount', 'label': 'Amount'},
                {'name': 'payment_method', 'label': 'Payment Method'},
                {'name': 'payment_time', 'label': 'Payment Time', 'format': 'MMM dd, yyyy'},
                {'name': 'status', 'label': 'Status'},
            ],
        }
        
        super().__init__(model='Payment', view_config=view_config, filters=None, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
