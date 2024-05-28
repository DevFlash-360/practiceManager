import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid


class TimeEntryView(GridView):
    def __init__(self, case=None, case_uid=None, **kwargs):
        self.filter_case_uid = None
        is_dashboard = kwargs.pop('dashboard', None)
        if is_dashboard:
            self.filter_case_uid = get_cookie('case_uid')
        
        view_config = {
            'model': 'TimeEntry',
            'columns': [
                {'name': 'date', 'label': 'Entry Date', 'format': 'MMM dd, yyyy'},
                {'name': 'activity.name', 'label': 'Activity'},
                {'name': 'duration', 'label': 'Duration'},
                {'name': 'description', 'label': 'Description'},
                {'name': 'rate', 'label': 'Rate'},
                {'name': 'total', 'label': 'Total'},
                {'name': 'staff.full_name', 'label': 'Staff'},
                {'name': 'case.case_name', 'label': 'Case'},
                {'name': 'status', 'label': 'Status'},
            ],
            'filter': {'case': self.filter_case_uid},
        }
        if self.filter_case_uid:
            filters = {
                'case': {'uid': self.filter_case_uid}
            }
        else:
            filters = None
        
        super().__init__(model='TimeEntry', view_config=view_config, filters=filters, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
