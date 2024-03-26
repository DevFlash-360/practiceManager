import anvil.server
import uuid
from anvil.js.window import ej, jQuery
from DevFusion.components.GridView2 import GridView2
from datetime import datetime, date
import anvil.js
from AnvilFusion.tools.utils import AppEnv, get_cookie
from ..app.models import CaseStage, Staff, Case, Task, Activity, User


class StatuteListView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'CauseOfAction',
            'columns': [
                {'name': 'type_of_action.name', 'label': 'Type', 'width': 110},
                {'name': 'statute_id', 'label': 'Statute ID', 'width': 100},
                {'name': 'cause_of_action', 'label': 'Cause of Action'},
                {'name': 'penalty', 'label': 'Penalty'},
			]
		}
        super().__init__(model='Case', view_config=view_config, **kwargs)
