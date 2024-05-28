import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid


class CaseUpdatesView(GridView):
    def __init__(self, case=None, case_uid=None, **kwargs):
        self.filter_case_uid = None
        is_dashboard = kwargs.pop('dashboard', None)
        if is_dashboard:
            self.filter_case_uid = get_cookie('case_uid')
        
        view_config = {
            'model': 'CaseUpdate',
            'columns': [
                {'name': 'next_date', 'label': 'Next Date', 'format': 'MMM dd, yyyy hh:mm a'},
                {'name': 'todays_update', 'label': 'Todays Update'},
                {'name': 'client_attendance_required', 'label': 'Client Attendance Required'},
                {'name': 'client_update', 'label': 'Client Update'},
                {'name': 'case.case_name', 'label': 'Case'},
                {'name': 'next_activity.name', 'label': 'Next Activity'},
            ],
            'filter': {'case': self.filter_case_uid},
        }
        if self.filter_case_uid:
            filters = {
                'case': {'uid': self.filter_case_uid}
            }
        else:
            filters = None
        
        super().__init__(model='CaseUpdate', view_config=view_config, filters=filters, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
