import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.tools.utils import AppEnv
import anvil.js.window
from anvil.js.window import ej
import uuid
from ..app.models import Lead


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
        for field in self.fields:
            field.show()

    def form_save(self, args):
        if self.lost_reason.value is not None:
            lead = Lead.get(AppEnv.details_lead_uid)
            lead.update({'lead_status': 'Lost'})
            lead.save()
            for field in self.fields:
                field.hide()
                field.value = None
            self.form.hide()
            AppEnv.navigation.content_control.refresh()
        else:
            args.cancel = True
    
    def form_cancel(self, args):
        for field in self.fields:
            field.value = None
            field.hide()
        self.form.hide()
