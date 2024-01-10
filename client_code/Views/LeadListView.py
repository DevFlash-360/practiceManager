import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery
from ..app.models import Lead


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
        
    def row_selected(self, args):
        jQuery(f"#details_content")[0].innerHTML = self.details_content(args)
        super().row_selected(args)

    def details_content(self, args):
        lead = args['data']
        item = Lead.get(lead['uid'])
        print(lead)
        return "lead-detail"
    
    