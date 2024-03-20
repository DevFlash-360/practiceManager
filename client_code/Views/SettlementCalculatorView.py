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
        self.contingency_fee_id = f"contingency_{uuid.uuid4()}"
        self.settlement_offer_id = f"settlement_{uuid.uuid4()}"
        self.treatment_reduction_id = f"treatment_{uuid.uuid4()}"
    
        cases_data = Case.search()
        cases_data_for_dropdown = [{'id': case['uid'], 'text': case['case_name']} for case in cases_data]
        self.dropdown_cases = ej.dropdowns.DropDownList({
            'dataSource': cases_data_for_dropdown,
            'placeholder': 'Select a Case'
        })
        self.contingency_fee = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        self.settlement_offer = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        percentage_list = [f"{i}%" for i in range(0, 101, 5)]
        self.treatment_reduction = ej.dropdowns.DropDownList({'dataSource': percentage_list})
        
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div class="row">\
                <div class="col-md-3">\
                    <div class="form-group">\
                        <label for="{self.dropdown_cases_id}">Case</label>\
                        <input type="text" id="{self.dropdown_cases_id}" class="form-control"/>\
                    </div>\
                    <div class="form-group input-group">\
                        <label for="{self.contingency_fee_id}">Contingency Fee</label>
                        <input id="{self.contingency_fee_id}" placeholder="Contingency Fee" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-percent"></i></span>\
                    </div>\
                    <div class="form-group input-group">\
                        <label for="{self.settlement_offer_id}">Settlement Offer</label>
                        <input id="{self.settlement_offer_id}" placeholder="Settlement Offer" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                    <div class="form-group input-group">\
                        <label for="{self.treatment_reduction_id}">Treatment Reduction</label>
                        <input id="{self.treatment_reduction_id}" placeholder="Treatment Reduction" type="text" class="form-control">\
                    </div>\
                </div>\
                <div class="col-md-3">\
                    <input type="currency" />\
                </div>\
            </div>'
        
        self.dropdown_cases.appendTo(jQuery(f"#{self.dropdown_cases_id}")[0])
        self.contingency_fee.appendTo(jQuery(f"#{self.contingency_fee_id}")[0])
        self.settlement_offer.appendTo(jQuery(f"#{self.settlement_offer_id}")[0])
        self.treatment_reduction.appendTo(jQuery(f"#{self.treatment_reduction_id}")[0])
    
    def destroy(self):
        self.dropdown_cases.destroy()
        self.contingency_fee.destroy()
        self.settlement_offer.destroy()
        self.treatment_reduction.destroy()

        if self.container_el:
            self.container_el.innerHTML = ''
