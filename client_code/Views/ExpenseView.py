import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid


class ExpenseView(GridView):
    def __init__(self, case=None, case_uid=None, **kwargs):
        self.filter_case_uid = None
        is_dashboard = kwargs.pop('dashboard', None)
        if is_dashboard:
            self.filter_case_uid = get_cookie('case_uid')
        
        view_config = {
            'model': 'Expense',
            'columns': [
                {'name': 'date', 'label': 'Entry Date'},
                {'name': 'activity.name', 'label': 'Activity'},
                {'name': 'description', 'label': 'Description'},
                {'name': 'amount', 'label': 'Amount'},
                {'name': 'quantity', 'label': 'Quantity'},
                {'name': 'total', 'label': 'Total'},
                {'name': 'staff.full_name', 'label': 'Staff'},
                {'name': 'case.case_name', 'label': 'Case'},
            ],
        }
        if self.filter_case_uid:
            filters = {
                'case': {'uid': self.filter_case_uid}
            }
        else:
            filters = None
        
        super().__init__(model='Expense', view_config=view_config, filters=filters, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
