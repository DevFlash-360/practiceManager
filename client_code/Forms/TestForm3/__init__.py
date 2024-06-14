from ._anvil_designer import TestForm3Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TestForm3(TestForm3Template):
	def __init__(self, **properties):
		# Set Form properties and Data Bindings.
		self.init_components(**properties)
		self.drop_down_signs.items = [(row['name'], row) for row in app_tables.signature.search()]
		self.signature_name = None
		self.signature_url = None
		self.doc_uid = '778abb68-ec4d-4ae8-bcb1-1940ea45130c'

	# Any code you write here will run before the form opens.

	def Confirm_click(self, **event_args):
		"""This method is called when the button is clicked"""
		pos = self.call_js('get_sign_pos')
		page_info = self.call_js('get_pageInfo')
		pdf = anvil.server.call(
			'add_image_to_pdf', 
			self.doc_uid, 
			self.signature_name,
			page_info,
			pos['sign_x'],
			pos['sign_y'],
		)
		anvil.media.download(pdf)

	def get_sign_url(self):
		# Update to get signature from SF Signature
		return self.signature_url

	def drop_down_signs_change(self, **event_args):
		"""This method is called when an item is selected"""
		self.signature_name = self.drop_down_signs.selected_value['name']
		signature_url = anvil.server.call('load_signature', self.signature_name)
		print(signature_url)
		self.signature_url = signature_url

	def form_show(self, **event_args):
		pdf_url = anvil.server.call('load_doc', self.doc_uid)
		self.call_js('init', pdf_url)

