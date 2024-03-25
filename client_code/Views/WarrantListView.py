import anvil.server
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid


class WarrantListView(GridView):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Case',
            'columns': [
                
			]
        }
        super().__init__(model='Case', view_config=view_config, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
