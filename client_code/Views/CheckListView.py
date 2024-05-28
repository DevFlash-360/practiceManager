import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid
from ..app.models import Staff, User


class CheckListView(GridView):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Check',
            'columns': [
                {'name': 'check_number', 'label': 'Check number'},
                {'name': 'date', 'label': 'Date', 'format': 'MMM dd, yyyy'},
                {'name': 'payee.full_name', 'label': 'Payee'},
                {'name': 'amount', 'label': 'Amount'},
                {'name': 'memo', 'label': 'Memo'},
                {'name': 'reference', 'label': 'Reference'},
                # {'name': 'bank_account.bank_name', 'label': 'Bank Account'},
            ],
        }
        
        super().__init__(model='Check', view_config=view_config, filters=None, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
