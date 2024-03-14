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
            'cssClass': 'e-primary',
            'iconCss': 'fa fa-plus',
            'isPrimary': True,
            'isToggle': True
        })
        self.btn_mode = ej.buttons.Button({
            'cssClass': 'e-primary',
            'iconCss': 'fa fa-calendar',
            'isPrimary': True,
            'isToggle': True
        })

        self.numbers = ej.inputs.TextBox({
            'floatLabelType': 'Auto'
        })
    
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div style="display:flex;">\
                <div style="width: 250px; margin-right: 10px;">\
                    <input id="{self.date_picker_id}" type="text"/>\
                </div>\
                <div style="display:flex; width: 250px; margin-right: 10px;">\
                    <label for="{self.date_picker_id}">Number of Days</label>\
                    <input id="{self.numbers_id}"/>\
                </div>\
                <button id="{self.btn_plus_minus_id}" style="margin-right: 10px;">ADD</button>\
                <button id="{self.btn_mode_id}">CALENDAR DAYS</button>\
            </div>\
            <label style="font-size: 16px;">Date: Thursday, March 21, 2024</label>'
        self.date_picker.appendTo(jQuery(f"#{self.date_picker_id}")[0])
        self.btn_plus_minus.appendTo(jQuery(f"#{self.btn_plus_minus_id}")[0])
        self.btn_mode.appendTo(jQuery(f"#{self.btn_mode_id}")[0])
        self.numbers.appendTo(jQuery(f"#{self.numbers_id}")[0])

    def destroy(self):
        self.date_picker.destroy()
        if self.container_el:
            self.container_el.innerHTML = ''
