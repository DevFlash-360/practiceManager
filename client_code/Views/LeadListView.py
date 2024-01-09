import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery
from ..app.models import Case, CaseStatus, User


class LeadListView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Lead',
            'columns': [
                {'name': 'case_name', 'label': 'Case Name'},
                {'name': 'retainer', 'label': 'Retainer'},
                {'name': 'lead_status', 'label': 'Lead Status'},
            ]
        }
        super().__init__(model='Lead', view_config=view_config, **kwargs)