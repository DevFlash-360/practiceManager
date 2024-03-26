import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid


class WarrantListView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Case',
            'columns': [
                {'name': 'next_case_search', 'label': 'Next Case Search'},
                {'name': 'case_name', 'label': 'Case Name'},
                {'name': 'incident_location', 'label': 'Incident Location'},
                {'name': 'contacts.full_name', 'label': 'Contacts'},
			]
        }
        super().__init__(model='Case', view_config=view_config, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
