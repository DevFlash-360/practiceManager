import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import datetime, timedelta

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py


def bizday_calc_func(start_date, num_days):
    my_start_date = start_date
    my_num_days = abs(num_days)
    inc = 1 if num_days > 0 else -1
    while my_num_days > 0:
      my_start_date += timedelta(days=inc)
      weekday = my_start_date.weekday()
      if weekday >= 5:
        continue
      my_num_days -= 1
    return my_start_date

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

        self.date_picker = ej.calendars.DatePicker({'placeholder': 'Enter date'})
        
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
                <div style="width: 250px; margin-right: 30px;">\
                    <input id="{self.date_picker_id}" type="text"/>\
                </div>\
                <div style="display:flex; width: 120px;">\
                    <label for="{self.date_picker_id}" style="margin-right:10px;">Number of Days</label>\
                    <input id="{self.numbers_id}"/>\
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
                    <label style="font-size: 18px;">Date: Thursday, March 21, 2024</label>\
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
        if self.container_el:
            self.container_el.innerHTML = ''

    def change_date(self, args):
        print(datetime_js_to_py(self.date_picker.value).strftime("%A, %B %d, %Y"))
        self.update_date()

    def change_plus_minus(self, args):
        print(f"plus checked = {self.radio_plus.checked}")
        self.update_date()
    
    def change_day_mode(self, args):
        print(f"calendar checked = {self.radio_calendar.checked}")
        self.update_date()
    
    def change_number_days(self, args):
        self.number_days = int(args['value'])
        self.update_date()
    
    def update_date(self):
        print("update_date")
        print(self.date_picker.value)

        date_check_blank = self.date_picker.value is not None
        date_origin = datetime_js_to_py(self.date_picker.value)


        
