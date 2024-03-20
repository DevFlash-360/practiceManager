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
        self.client_net_id = f"treatment_{uuid.uuid4()}"
        self.attorney_net_id = f"treatment_{uuid.uuid4()}"
        self.table_fees_id = f"Fee_table_{uuid.uuid4()}"
        self.table_treatment_id = f"Treatment_table_{uuid.uuid4()}"
    
        cases_data = Case.search()
        cases_data_for_dropdown = [{'id': case['uid'], 'text': case['case_name']} for case in cases_data]
        self.dropdown_cases = ej.dropdowns.DropDownList({
            'dataSource': cases_data_for_dropdown
        })
        self.contingency_fee = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        self.settlement_offer = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        percentage_list = [f"{i}%" for i in range(0, 101, 5)]
        self.treatment_reduction = ej.dropdowns.DropDownList({'dataSource': percentage_list})
        self.client_net = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        self.attorney_net = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div class="row">\
                <div class="col-md-3">\
                    <div class="form-group">\
                        <label for="{self.dropdown_cases_id}">Case</label>\
                        <input type="text" id="{self.dropdown_cases_id}" class="form-control"/>\
                    </div>\
                    <label>Contingency Fee</label>\
                    <div class="form-group input-group">\
                        <input id="{self.contingency_fee_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-percent"></i></span>\
                    </div>\
                    <label>Settlement Offer</label>\
                    <div class="form-group input-group">\
                        <input id="{self.settlement_offer_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                    <div class="form-group input-group">\
                        <label for="{self.treatment_reduction_id}">Treatment Reduction</label>\
                        <input id="{self.treatment_reduction_id}" type="text" class="form-control">\
                    </div>\
                </div>\
                <div class="col-md-3">\
                    <label>Client Net</label>\
                    <div class="form-group input-group">\
                        <input id="{self.client_net_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                    <label>Attorney/Firm Net</label>\
                    <div class="form-group input-group">\
                        <input id="{self.attorney_net_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                </div>\
            </div>\
            <table id="{self.table_fees_id}"></table>'
        
        self.dropdown_cases.appendTo(jQuery(f"#{self.dropdown_cases_id}")[0])
        self.contingency_fee.appendTo(jQuery(f"#{self.contingency_fee_id}")[0])
        self.settlement_offer.appendTo(jQuery(f"#{self.settlement_offer_id}")[0])
        self.treatment_reduction.appendTo(jQuery(f"#{self.treatment_reduction_id}")[0])
        self.client_net.appendTo(jQuery(f"#{self.client_net_id}")[0])
        self.attorney_net.appendTo(jQuery(f"#{self.attorney_net_id}")[0])
    
    def destroy(self):
        self.dropdown_cases.destroy()
        self.contingency_fee.destroy()
        self.settlement_offer.destroy()
        self.treatment_reduction.destroy()
        self.client_net.destroy()
        self.attorney_net.destroy()

        if self.container_el:
            self.container_el.innerHTML = ''
