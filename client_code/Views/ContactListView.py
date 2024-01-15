import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery
from ..app.models import Contact


class ContactListView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Contacts',
            'columns': [
                # {'name': 'full_name', 'label': 'Name'},
                # {'name': 'contact_group', 'label': 'Group'},
                # {'name': 'email', 'label': 'Email'},
                # {'name': 'mobile_phone', 'label': 'Mobile Phone'},
                {'name': 'work_phone', 'label': 'Work Phone'},
            ]
        }
        super().__init__(model='Contacts', view_config=view_config, **kwargs)
