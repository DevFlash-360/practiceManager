import uuid
import anvil.js
from datetime import datetime, timedelta

from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py

from ..app.models import Case

class SettlementCalculatorView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.dropdown_cases_id = f"dropdown_cases_{uuid.uuid4()}"
    
        cases_data = Case.search()
        cases_data_for_dropdown = [{'id': case['uid'], 'text': case['case_name']} for case in cases_data]
        self.dropdown_cases = ej.dropdowns.DropDownList({
            'dataSource': cases_data_for_dropdown,
            'placeholder': 'Select a Case'
        })
        
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div class="row">\
                <div class="col-md-3">\
                    <div class="form-group">\
                        <input type="text" id="{self.dropdown_cases_id}" />\
                    </div>\
                    <div class="form-group input-group">\
                        <input placeholder="Contingency Fee" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-percent"></i></span>\
                    </div>\
                </div>\
                <div class="col-md-3">\
                    <input type="currency" />\
                </div>\
            </div>'
        
        self.dropdown_cases.appendTo(jQuery(f"#{self.dropdown_cases_id}")[0])
    
    def destroy(self):
        if self.container_el:
            self.container_el.innerHTML = ''
