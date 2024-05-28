import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid
from ..app.models import Staff, User, Timesheet


class TimeSheetView(GridView2):
    def __init__(self, **kwargs):
        self.filter_staff_uid = None
        is_staff = kwargs.pop('only_staff', None)
        if is_staff:
            logged_user = User.get(AppEnv.logged_user.get('user_uid'))
            logged_staff = Staff.search(user=logged_user)
            for staff in logged_staff:
                self.filter_staff_uid = staff['uid']
        
        view_config = {
            'model': 'Timesheet',
            'columns': [
                {'name': 'staff.full_name', 'label': 'Staff'},
                {'name': 'clock_in_time', 'label': 'Clock in Time', 'format': 'MMM dd, yyyy hh:mm a'},
                {'name': 'clock_out_time', 'label': 'Clock out Time', 'format': 'MMM dd, yyyy hh:mm a'},
                {'name': 'hours_worked', 'label': 'Hours Worked'},
                {'name': 'earned_pay', 'label': 'Earned Pay'},
                {'name': 'status', 'label': 'Status'},
            ],
            'filter': {'staff': self.filter_staff_uid},
        }
        if self.filter_staff_uid:
            filters = {
                'staff': {'uid': self.filter_staff_uid}
            }
        else:
            filters = None
        
        super().__init__(model='Timesheet', view_config=view_config, filters=filters, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
