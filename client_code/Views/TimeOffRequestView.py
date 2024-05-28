import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid
from ..app.models import Staff, User


class TimeOffRequestView(GridView):
    def __init__(self, **kwargs):
        self.filter_staff_uid = None
        is_staff = kwargs.pop('only_staff', None)
        if is_staff:
            logged_user = User.get(AppEnv.logged_user.get('user_uid'))
            logged_staff = Staff.search(user=logged_user)
            for staff in logged_staff:
                self.filter_staff_uid = staff['uid']
        
        view_config = {
            'model': 'TimeOffRequest',
            'columns': [
                {'name': 'staff.full_name', 'label': 'Staff'},
                {'name': 'reason', 'label': 'Reason'},
                {'name': 'date_of_leave', 'label': 'Date of Leave', 'format': 'MMM dd, yyyy'},
                {'name': 'date_of_return', 'label': 'Date of Return', 'format': 'MMM dd, yyyy'},
                {'name': 'status', 'label': 'Approved'},
            ],
            'filter': {'staff': self.filter_staff_uid},
        }
        if self.filter_staff_uid:
            filters = {
                'staff': {'uid': self.filter_staff_uid}
            }
        else:
            filters = None
        
        super().__init__(model='TimeOffRequest', view_config=view_config, filters=filters, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
