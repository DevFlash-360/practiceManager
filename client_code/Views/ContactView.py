import anvil.server
from DevFusion.components.GridView2 import GridView2


class ContactView(GridView2):
	def __init__(self, **kwargs):
		print("ContactView")
		view_config = {
			'model': 'Contact',
			'columns': [
				{'name': 'first_name', 'label': 'First Name'},
				{'name': 'last_name', 'label': 'Last Name'},
			]
		}
		super().__init__(model='Contact', view_config=view_config, *kwargs)
