import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.tools.utils import AppEnv
import anvil.js.window
from anvil.js.window import ej
import uuid


class LeadLostForm:
    def __init__(self, target):
        self.target_el = anvil.js.window.document.getElementById(target)
        self.container_id = str(f"assistant-{uuid.uuid4()}")
        self.container_el = anvil.js.window.document.createElement('div')
        self.container_el.setAttribute('id', self.container_id)
        self.target_el.append(self.container_el)

        self.form_content = '<div>Form Content</div>'
        self.form = ej.popups.Dialog({
            'header': 'Lost Lead',
            'content': self.form_content,
            'showCloseIcon': True,
            'target': self.target_el,
            'isModal': True,
            'width': '430px',
            'height': '200px',
        })
        self.form.appendTo(self.container_el)
    
    def form_show(self):
        self.form.show()

