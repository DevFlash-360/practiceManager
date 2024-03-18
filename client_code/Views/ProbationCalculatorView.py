import uuid
import anvil.js

from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv


class ProbationCalculatorView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]

        self.datepicker_sentence_date_id = f"sentencing_{uuid.uuid4()}"
        self.probation__id = f"sentencing_{uuid.uuid4()}"

        self.datepicker_sentence_date = ej.calendars.DatePicker({})
    
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div style="display:flex; justify-content: center;">\
                <label for="{self.datepicker_sentence_date_id}" style="margin-right:10px;">Select Sentencing Date</label>\
                <input id="{self.datepicker_sentence_date_id}"/>\
            </div>\
            <div style="display: flex; margin-bottom: 15px; justify-content: center;">\
            
            </div>'
        
        self.datepicker_sentence_date.appendTo(jQuery(f"#{self.datepicker_sentence_date_id}")[0])
    
    def destroy(self):
        self.datepicker_sentence_date.destroy()

        if self.container_el:
            self.container_el.innerHTML = ''
