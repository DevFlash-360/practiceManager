import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Staff
from datetime import datetime, date

import uuid
import anvil.js
from anvil.js.window import ej, jQuery

class ESignSettingsForm(FormBase):

    def __init__(self, **kwargs):
        kwargs['model'] = 'TimeEntry'

        self.doc_name = TextInput(name='doc_name', label='Document', value='Agreement.pdf', enabled = False)
        # self.sign_label = InlineMessage(content='Who needs to sign?')
        self.sign_label = InlineMessage(content='''
          <hr class="mt-0"/>
          <p style='font-size: 20px'>Who needs to sign?</p>
        ''')
        self.sign_name = DropdownInput(name='sign_name', options=['Adam Plumer', 'Alex', 'Dmytro', 'Vlad'])
        self.sign_email = TextInput(name='sign_email')
        self.add_signer = Button(content='+ Add another signer')
        self.line_gap_1 = InlineMessage(content='''
          <div><div>
        ''')
        self.countersignature = CheckboxInput(name='countersignature', label='This document needs a countersignature', label_position='After', value=False)
        self.line_gap_2 = InlineMessage(content='''
          <div><div>
        ''')
        self.drawnsignature = CheckboxInput(name='drawnsignature', label='Require drawn signatures for all signers', label_position='After', value=False)
        self.line_gap_3 = InlineMessage(content='''
          <div><div>
        ''')
        self.btn_prepare = Button(content='Prepare document for signing', action=self.on_btn_prepare_click)
        self.message_label = InlineMessage(content='''
          <hr/>
          <p style='font-size: 20px'>Message for signers</p>
        ''')
        # InlineMessage can show any text or html
        self.subject = TextInput(name='subject', label='Subject', value='Signature requested from Wooldridge Law Ltd.')
        self.message = MultiLineInput(name='message', label='Message', value='Please review and sign this document at your earliest convenience.', rows=3)
        # InlineMessage() can store html
        self.msg_txt = InlineMessage(content='''
          <p style='font-size: 12px; opacity: 0.5'>Your email will include a button to access the document for signature</p>
        ''')
        
      
        sections = [
            {'name': '_', 'rows': [
                [self.doc_name],
                [self.sign_label],
                [self.sign_name, self.sign_email],
                [self.add_signer],
                [self.line_gap_1],
                [self.countersignature],
                [self.line_gap_2],
                [self.drawnsignature],
                [self.line_gap_3],
                [self.btn_prepare],
                [self.message_label],
                [self.subject],
                [self.message],
                [self.msg_txt],
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

    def form_open(self, args):
        super().form_open(args)

    # def form_show(self):
    #     self.container_el.innerHTML = '''
    #       <h1>Oh my god!</h1>
    #     '''
  
    def form_save(self, args):
        super().form_save(args)

    def total_calc(self, args):
        if args['name'] == 'rate_type':
            if self.rate_type.value == 'Flat':
                self.total.value = self.rate.value
                self.duration.value = None
                self.duration.enabled = False
            else:
                self.duration.enabled = True
                if self.rate.value is not None and self.duration.value is not None:
                    self.total.value = round((self.rate.value * self.duration.value), 2)
                else:
                    self.total.value = None
        if args['name'] == 'rate':
            if self.rate_type.value == 'Per hour':
                if self.rate.value is not None and self.duration.value is not None:
                    self.total.value = round((self.rate.value * self.duration.value), 2)
            else:
                self.total.value = self.rate.value
        if args['name'] == 'duration':
            if self.rate_type.value == 'Per hour':
                if self.rate.value is not None and self.duration.value is not None:
                    self.total.value = round((self.rate.value * self.duration.value), 2)
            else:
                self.total.value = self.rate.value

    def on_btn_prepare_click(self, args):
      print('the prepare button is clicked!')
    # def open_settings_dlg(self, args):
    #   print('Wow I handled this!!!!!!')

# need to change the "save" button as "Send" button -> change the FormBase ? I don't know..
# If i change the lable in FormBase, the buttons in all pop-ups will change. How to handle this?
## need to change the code in DevFusion in order to connect the step1 and step 2
# button click handle method in DevFusion
# make onClick handler to button_prepare
# in DevFusion, in the button adding part, there's a method calling line: open_dashboard
# called open_settings_dlg in DevFusion
# open_settings_dlg should be in the CaseDocumentView