import uuid
import anvil.js

from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv


class ProbationCalculatorView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]

        self.datepicker_sentence_date_id = f"sentencing_{uuid.uuid4()}"
        self.textbox_sentence_id = f"sentence_{uuid.uuid4()}"
        self.textbox_credits_id = f"credits_{uuid.uuid4()}"

        self.datepicker_sentence_date = ej.calendars.DatePicker({})
        self.textbox_sentence = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        self.textbox_credits = ej.inputs.TextBox({'floatLabelType': 'Auto'})
    
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
