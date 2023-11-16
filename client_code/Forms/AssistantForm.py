# from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *
import anvil.js.window
from anvil.js.window import ej
import uuid


class AssistantForm:
    def __init__(self, target):
        print('AssistantForm')

        self.target_el = anvil.js.window.document.getElementById(target)
        self.container_id = str(f"assistant-{uuid.uuid4()}")
        self.container_el = anvil.js.window.document.createElement('div')
        self.container_el.setAttribute('id', self.container_id)
        self.container_el.style.visibility = 'hidden'
        self.target_el.append(self.container_el)
        self.form_id = str(f"assistant-form-{uuid.uuid4()}")
        self.form_el = None


        self.user_message = MultiLineInput(name='user_message', label='')
        self.thread = InlineMessage(name='thread')

        self.form_content = ''
        self.fields = [
            self.thread,
            self.user_message,
        ]
        for field in self.fields:
            self.form_content += f'<div class="row"><div class="col-xs-12" id="{field.container_id}"></div></div>'

        self.form_content = f'<form id="{self.form_id}" style="padding-top:1em;!important">' + self.form_content + '</form>'

        self.form = ej.popups.Dialog({
            'header': 'Assistant',
            'content': self.form_content,
            'showCloseIcon': True,
            'target': self.target_el,
            'isModal': False,
            'width': '500px',
            'height': '100%',
            'visible': False,
            'position': {'X': 'center', 'Y': '100'},
            'animationSettings': {'effect': 'Zoom'},
            'cssClass': 'e-fixed py-dialog',
            'open': self.form_open,
            # 'close': self.form_cancel,
            # 'beforeOpen': self.before_open,
            # 'created': self.form_created,
        })
        self.form.cssClass = 'e-fixed py-dialog'
        self.form.appendTo(self.container_el)


    def form_show(self):
        print('show assistant form')
        self.form.show()
        # if view_mode:
        #     container_el_height = int(self.container_el.style['max-height'][0:-2]) - DIALOG_FULLSCREEN_HEIGHT_OFFSET
        #     self.container_el.style.top = f"{DIALOG_FULLSCREEN_HEIGHT_OFFSET}px"
        #     self.container_el.style['max-height'] = f"{container_el_height}px"


    def form_open(self):
        for field in self.fields:
            field.show()
        self.container_el.style.visibility = 'visible'
