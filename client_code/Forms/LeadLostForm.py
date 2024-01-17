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

        self.lost_reason = DropdownInput(name='lost_reason', label='Lost Reason', options=[
            'No Money', 'No Case', 'Calling for Information', 'Marketing', 'Wrong Number',
            'Out of State', 'Outside Practice Area', 'Hired Someone Else']
        )
        self.fields = [
            self.lost_reason
        ]


        self.form_content = f'<div id="{self.lost_reason.container_id}"></div>'
        self.form = ej.popups.Dialog({
            'header': 'Lost Lead',
            'content': self.form_content,
            'showCloseIcon': True,
            'target': self.target_el,
            'isModal': True,
            'width': '430px',
            'height': '200px',
            'open': self.form_open,
            'buttons': [
                {
                    'buttonModel':
                        {'isPrimary': True, 'content': 'Submit', 'cssClass': 'da-save-button'},
                    'click': self.form_save,
                },{
                    'buttonModel':
                        {'isPrimary': False, 'content': 'Cancel', 'cssClass': 'da-cancel-button'},
                    'click': self.form_cancel,
                },
            ]
        })
        self.form.appendTo(self.container_el)
    
    def form_show(self):
        self.form.show()

    def form_open(self, args):
        print("form_open")
        for field in self.fields:
            field.show()

    def form_save(self, args):
        print("form_save")

    
    def form_cancel(self, args):
        print("form_cancel")
        # for field in self.form_fields:
        #     field.value = None
        #     field.hide()
        self.form.hide()
