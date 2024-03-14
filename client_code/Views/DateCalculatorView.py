import uuid
import anvil.js

from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv


class DateCalculatorView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]

        self.date_picker_id = f"date_picker_{uuid.uuid4()}"
        self.btn_plus_minus_id = f"plus_{uuid.uuid4()}"
        self.btn_mode_id = f"mode_{uuid.uuid4()}"
        self.numbers_id = f"numbers_{uuid.uuid4()}"
        self.output_id = f"output_{uuid.uuid4()}"

        self.date_picker = ej.calendars.DatePicker({'placeholder': 'Enter date'})
        self.btn_plus_minus = ej.buttons.Button({
            'cssClass': 'e-flat',
            'iconCss': 'fa fa-plus',
            'isPrimary': True
        })
    
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div>\
                <input id="{self.date_picker_id}" type="text"/>\
                <button id="{self.btn_plus_minus_id}">ADD</button>\
            </div>'
        self.date_picker.appendTo(jQuery(f"#{self.date_picker_id}")[0])
        self.btn_plus_minus.appendTo(jQuery(f"#{self.btn_plus_minus_id}")[0])

    def destroy(self):
        self.date_picker.destroy()
        if self.container_el:
            self.container_el.innerHTML = ''
