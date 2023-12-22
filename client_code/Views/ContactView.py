import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv


class ContactView(GridView2):
	def __init__(self, **kwargs):
		print("ContactView")
		view_config = {
			'model': 'Contact',
			'columns': [
				{'name': 'first_name', 'label': 'Name'},
			]
		}
		super().__init__(model='Contact', view_config=view_config, *kwargs)
