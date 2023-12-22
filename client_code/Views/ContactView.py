import anvil.server
from DevFusion.components.GridView2 import GridView2


class ContactView(GridView2):
	def __init__(self, **kwargs):
		# print("ContactView")
		# view_config = {
		# 	'model': 'Contact',
		# 	'columns': [
		# 		{'name': 'first_name', 'label': 'Name'},
		# 		{'name': 'last_name', 'label': 'Name'}
		# 	]
		# }
		# super().__init__(model='Contact', view_config=view_config, *kwargs)
		super().__init__(**kwargs)
