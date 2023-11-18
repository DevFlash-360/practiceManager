# from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *
import anvil.js.window
from anvil.js.window import ej
import uuid


class AssistantForm:
    def __init__(self, target):
        print('AssistantForm', target)

        self.target_el = anvil.js.window.document.getElementById(target)
        self.container_id = str(f"assistant-{uuid.uuid4()}")
        self.container_el = anvil.js.window.document.createElement('div')
        self.container_el.setAttribute('id', self.container_id)
        # self.container_el.style.visibility = 'hidden'
        self.target_el.append(self.container_el)
        self.form_id = str(f"assistant-form-{uuid.uuid4()}")
        self.chat_id = str(f"assistant-chat-{uuid.uuid4()}")
        self.chat_el = None


        self.user_message = MultiLineInput(name='user_message', label='')
        self.thread = InlineMessage(name='thread')

        self.form_content = ''
        self.fields = [
            self.thread,
            self.user_message,
        ]
        self.form_content = f'<div id="{self.chat_id}" style="display: flex; flex-direction: column; height: 100vh;">'
        self.form_content += f'<div style="flex-grow: 1; overflow: auto;" ><div id="{self.thread.container_id}"></div></div>'
        self.form_content += f'<div><div id="{self.user_message.container_id}"></div></div>'
        self.form_content += '</div>'

        self.form_content = f'<form id="{self.form_id}" style="padding-top:1em;!important">' + self.form_content + '</form>'

        self.form = ej.popups.Dialog({
            'header': 'Assistant',
            'content': self.form_content,
            'showCloseIcon': True,
            'target': self.target_el,
            'isModal': False,
            'width': '500px',
            'height': '99%',
            'visible': True,
            'position': {'X': 'right', 'Y': '15'},
            'animationSettings': {'effect': 'Zoom'},
            'cssClass': 'e-fixed py-dialog',
            'open': self.form_open,
            # 'close': self.form_cancel,
            # 'beforeOpen': self.before_open,
            # 'created': self.form_created,
        })
        self.form.cssClass = 'e-fixed py-dialog'
        self.form.appendTo(self.container_el)
        print(self.target_el, self.container_el)


    def form_show(self):
        print('show assistant form')
        self.form.show()
        self.chat_el = anvil.js.window.document.getElementById(self.chat_id)
        print(self.chat_el, self.container_el, self.container_el.getBoundingClientRect().height)
        self.chat_el.style.height = f'{self.container_el.getBoundingClientRect().height}px'
        # if view_mode:
        #     container_el_height = int(self.container_el.style['max-height'][0:-2]) - DIALOG_FULLSCREEN_HEIGHT_OFFSET
        #     self.container_el.style.top = f"{DIALOG_FULLSCREEN_HEIGHT_OFFSET}px"
        #     self.container_el.style['max-height'] = f"{container_el_height}px"


    def form_open(self, args):
        print('form_open')
        for field in self.fields:
            field.show()
