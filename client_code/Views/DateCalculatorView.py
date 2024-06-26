import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from DevFusion.tools.utils import bizday_calc_func


class DateCalculatorView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]

        self.date_picker_id = f"date_picker_{uuid.uuid4()}"
        self.btn_plus_minus_id = f"plus_{uuid.uuid4()}"
        self.btn_mode_id = f"mode_{uuid.uuid4()}"
        self.numbers_id = f"numbers_{uuid.uuid4()}"
        self.output_id = f"output_{uuid.uuid4()}"

        self.number_days = 0

        self.date_picker = ej.calendars.DatePicker({
            'placeholder': 'Enter date',
            'format': 'MMM dd, yyyy'
        })
        
        self.radio_plus = ej.buttons.RadioButton({
            'label': '+ ADD',
            'name': 'plus_minus',
            'checked': True
        })
        
        self.radio_minus = ej.buttons.RadioButton({
            'label': '- SUBTRACT',
            'name': 'plus_minus',
            'checked': False
        })
        
        self.radio_calendar = ej.buttons.RadioButton({
            'label': 'CALENDAR DAYS',
            'name': 'day_mode',
            'checked': True
        })
        
        self.radio_business = ej.buttons.RadioButton({
            'label': 'BUSINESS DAYS',
            'name': 'day_mode',
            'checked': False
        })

        self.numbers = ej.inputs.TextBox({
            'floatLabelType': 'Auto'
        })

        self.date_picker.addEventListener('change', self.change_date)
        self.radio_plus.addEventListener('change', self.change_plus_minus)
        self.radio_minus.addEventListener('change', self.change_plus_minus)
        self.radio_calendar.addEventListener('change', self.change_day_mode)
        self.radio_business.addEventListener('change', self.change_day_mode)
        self.numbers.addEventListener('input', self.change_number_days)
        
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div style="display:flex; margin-bottom: 15px; justify-content: center;">\
                <div class="e-card" style="width: 250px; margin-right: 30px;">\
                    <input id="{self.date_picker_id}" type="text"/>\
                </div>\
                <div style="display:flex; align-items: center; ">\
                    <label for="{self.numbers_id}" style="white-space: nowrap; margin-right:10px;">Number of Days</label>\
                    <input id="{self.numbers_id}" style="width: 50px;"/>\
                </div>\
            </div>\
            <div style="display: flex; margin-bottom: 15px; justify-content: center;">\
                <ul>\
                    <input type="radio" id="radio_plus"/>\
                    <input type="radio" id="radio_minus"/>\
                </ul>\
                <ul>\
                    <input type="radio" id="radio_calendar"/>\
                    <input type="radio" id="radio_business"/>\
                </ul>\
            </div>\
            <div style="display: flex; justify-content: center;">\
                <div class="e-card" style="width: 400px; align-items: center; padding:15px;">\
                    <label id={self.output_id} style="font-size: 18px;">Date: </label>\
                </div>\
            </div>'
        self.date_picker.appendTo(jQuery(f"#{self.date_picker_id}")[0])
        self.radio_plus.appendTo(jQuery("#radio_plus")[0])
        self.radio_minus.appendTo(jQuery("#radio_minus")[0])
        self.radio_calendar.appendTo(jQuery("#radio_calendar")[0])
        self.radio_business.appendTo(jQuery("#radio_business")[0])
        self.numbers.appendTo(jQuery(f"#{self.numbers_id}")[0])

    def destroy(self):
        self.date_picker.destroy()
        self.radio_plus.destroy()
        self.radio_minus.destroy()
        self.radio_calendar.destroy()
        self.radio_business.destroy()
        self.numbers.destroy()
        if self.container_el:
            self.container_el.innerHTML = ''

    def change_date(self, args):
        self.update_date()

    def change_plus_minus(self, args):
        self.update_date()
    
    def change_day_mode(self, args):
        self.update_date()
    
    def change_number_days(self, args):
        self.number_days = int(args['value'] if args['value'] else '0')
        self.update_date()
    
    def update_date(self):
        date_check_blank = self.date_picker.value is not None
        button_state_addsub = self.radio_plus.checked
        button_state_calcbiz = self.radio_calendar.checked

        output_text = 'Date: '
        if date_check_blank:
            date_origin = datetime_js_to_py(self.date_picker.value)
            date_output = date_origin
            if button_state_addsub and button_state_calcbiz:
                date_output = date_origin + timedelta(days=self.number_days)
            elif button_state_addsub == False and button_state_calcbiz:
                date_output = date_origin - timedelta(days=self.number_days)
            elif button_state_addsub and button_state_calcbiz == False:
                date_output = bizday_calc_func(date_origin, self.number_days)
            elif button_state_addsub == False and button_state_calcbiz == False:
                date_output = bizday_calc_func(date_origin, self.number_days*-1)
            output_text = f'Date: {date_output.strftime("%A, %B %d, %Y")}'
        output_el = jQuery(f"#{self.output_id}")[0]
        output_el.innerHTML = output_text
