import uuid
import anvil.js
from datetime import datetime, timedelta

from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py


class ProbationCalculatorView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.text_sentence = 0
        self.text_credits = 0

        self.datepicker_sentence_date_id = f"sentencing_{uuid.uuid4()}"
        self.textbox_sentence_id = f"sentence_{uuid.uuid4()}"
        self.textbox_credits_id = f"credits_{uuid.uuid4()}"
        self.probation_output_id = f"probation_output_{uuid.uuid4()}"

        self.datepicker_sentence_date = ej.calendars.DatePicker({})
        self.textbox_sentence = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        self.textbox_credits = ej.inputs.TextBox({'floatLabelType': 'Auto'})

        self.datepicker_sentence_date.addEventListener('change', self.datepicker_sentence_date_change)
        self.textbox_sentence.addEventListener('input', self.textbox_sentence_change)
        self.textbox_credits.addEventListener('input', self.textbox_credits_change)
    
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div style="display:flex; justify-content: center; margin-bottom: 15px;">\
                <div style="display: flex; align-items: center;">\
                    <label for="{self.datepicker_sentence_date_id}" style="white-space: nowrap; margin-right:10px;">Select Sentencing Date</label>\
                    <input id="{self.datepicker_sentence_date_id}"/>\
                </div>\
            </div>\
            <div style="display: flex; margin-bottom: 15px; justify-content: center;">\
                <div style="display:flex; align-items: center;">\
                    <label for="{self.textbox_sentence_id}" style="white-space: nowrap; margin-right:10px;">Probation Sentence (Months)</label>\
                    <input id="{self.textbox_sentence_id}" style="width: 50px;"/>\
                    <label for="{self.textbox_credits_id}" style="white-space: nowrap; margin: 0px 10px;">Good-Time Credits/Month (Days)</label>\
                    <input id="{self.textbox_credits_id}" style="width: 50px;"/>\
                </div>\
            </div>\
            <div style="display: flex; justify-content: center;">\
                <div class="e-card" style="width: 400px; align-items: center; padding:15px;">\
                    <label id={self.probation_output_id} style="font-size: 18px;"></label>\
                </div>\
            </div>'
        
        self.datepicker_sentence_date.appendTo(jQuery(f"#{self.datepicker_sentence_date_id}")[0])
        self.textbox_sentence.appendTo(jQuery(f"#{self.textbox_sentence_id}")[0])
        self.textbox_credits.appendTo(jQuery(f"#{self.textbox_credits_id}")[0])
    
    def destroy(self):
        self.datepicker_sentence_date.destroy()
        self.textbox_sentence.destroy()
        self.textbox_credits.destroy()

        if self.container_el:
            self.container_el.innerHTML = ''
    
    def probation_calc_func(self, sentencing_date, good_credits, sentence):
        if sentencing_date != '' and good_credits != '' and sentence != '':
            today = datetime.now()
            
            # Calculate difference in days without using .days
            years_diff = today.year - sentencing_date.year
            months_diff = today.month - sentencing_date.month
            time_served_in_days = (years_diff * 365.25) + (months_diff * 30.417)  # considering leap years
            
            # Calculate credits earned for the time served
            credits_earned = (time_served_in_days / 30.417) * int(good_credits)
            
            # Calculate total days required to complete half the sentence with credits
            total_days_required_with_credits = (int(sentence) * 30.417 / 2) + (int(sentence) * int(good_credits) / 2)
            
            # Calculate remaining days to serve with credits
            remaining_days_to_serve = total_days_required_with_credits - (time_served_in_days + credits_earned)
            
            # Calculate how many actual days they need to serve to accumulate the remaining days with credits
            actual_days_to_serve = remaining_days_to_serve * 30.417 / 50.417
            
            # Calculate projected termination with credits
            projected_termination_with_credits = today + timedelta(days=actual_days_to_serve)
            
            calc_output = (
                'Time Displayed in Months' + '\n\n' + 
                'Time Served: ' + str(round(time_served_in_days/30.417, 2)) + '   |   ' +
                'Credits Earned: ' + str(round(credits_earned/30.417, 2)) + '\n' + 
                'Total Served: ' + str(round((time_served_in_days + credits_earned)/30.417, 2)) + ' out of ' + str(sentence) + ' months' + '\n\n' +
                'Projected Termination (Credits Included):' + '\n' 
                + projected_termination_with_credits.strftime('%B %-d, %Y')
            )
            return calc_output

    def datepicker_sentence_date_change(self, args):
        self.update_output()

    def textbox_sentence_change(self, args):
        self.text_sentence = int(args['value'] if args['value'] else '0')
        self.update_output()

    def textbox_credits_change(self, args):
        self.text_credits = int(args['value'] if args['value'] else '0')
        self.update_output()
    
    def update_output(self):
        output_el = jQuery(f"#{self.probation_output_id}")[0]
        output_el.innerHTML = self.probation_calc_func(
            datetime_js_to_py(self.datepicker_sentence_date.value),
            self.text_credits,
            self.text_sentence
        )
        print("updated")
