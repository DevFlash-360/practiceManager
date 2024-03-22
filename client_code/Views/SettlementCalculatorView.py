import uuid
import anvil.js
from datetime import datetime, timedelta

from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py

from ..app.models import Case, Expense

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
        self.total_fees_id = f"total_fees_{uuid.uuid4()}"
        self.table_fees_id = f"Fee_table_{uuid.uuid4()}"
        self.table_treatment_id = f"total_treatment_{uuid.uuid4()}"
        self.total_treatment_id = f"total_treatment_{uuid.uuid4()}"
        self.reduced_treatment_id = f"reduced_treatment_{uuid.uuid4()}"
        
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
        self.total_fees = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        self.total_treatment = ej.inputs.TextBox({'floatLabelType': 'Auto'})
        self.reduced_treatment = ej.inputs.TextBox({'floatLabelType': 'Auto'})

        self.dropdown_cases.addEventListener('change', self.dropdown_cases_change)
        self.treatment_reduction.addEventListener('change', self.dropdown_reduction_change)
        self.contingency_fee.addEventListener('input', self.textbox_congingency_change)
        self.settlement_offer.addEventListener('input', self.textbox_settlement_change)
        
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
                        <input disabled id="{self.client_net_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                    <label>Attorney/Firm Net</label>\
                    <div class="form-group input-group">\
                        <input disabled id="{self.attorney_net_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                </div>\
            </div>\
            <table id="{self.table_fees_id}" style="margin-bottom: 15px;"></table>\
            <div class="row">\
                <div class="col-md-3">\
                    <label>Total Fees & Costs</label>\
                    <div class="form-group input-group">\
                        <input disabled id="{self.total_fees_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                </div>\
            </div>\
            <table id="{self.table_treatment_id}" style="margin-bottom: 15px;"></table>\
            <div class="row">\
                <div class="col-md-3">\
                    <label>Total Medical Treatment</label>\
                    <div class="form-group input-group">\
                        <input disabled id="{self.total_treatment_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                </div>\
                <div class="col-md-3">\
                    <label>Reduced Medical Treatment</label>\
                    <div class="form-group input-group">\
                        <input disabled id="{self.reduced_treatment_id}" type="number" class="form-control">\
                        <span class="input-group-addon"><i class="fa-light fa-dollar-sign"></i></span>\
                    </div>\
                </div>\
            </div>\
            '
        
        self.dropdown_cases.appendTo(jQuery(f"#{self.dropdown_cases_id}")[0])
        self.contingency_fee.appendTo(jQuery(f"#{self.contingency_fee_id}")[0])
        self.settlement_offer.appendTo(jQuery(f"#{self.settlement_offer_id}")[0])
        self.treatment_reduction.appendTo(jQuery(f"#{self.treatment_reduction_id}")[0])
        self.total_fees.appendTo(jQuery(f"#{self.total_fees_id}")[0])
        self.client_net.appendTo(jQuery(f"#{self.client_net_id}")[0])
        self.attorney_net.appendTo(jQuery(f"#{self.attorney_net_id}")[0])
        self.total_treatment.appendTo(jQuery(f"#{self.total_treatment_id}")[0])
        self.reduced_treatment.appendTo(jQuery(f"#{self.reduced_treatment_id}")[0])
    
    def destroy(self):
        self.dropdown_cases.destroy()
        self.contingency_fee.destroy()
        self.settlement_offer.destroy()
        self.treatment_reduction.destroy()
        self.total_fees.destroy()
        self.client_net.destroy()
        self.attorney_net.destroy()
        self.total_treatment.destroy()
        self.reduced_treatment.destroy()

        if self.container_el:
            self.container_el.innerHTML = ''
    
    def dropdown_cases_change(self, args):
        tbl_fee_costs = jQuery(f"#{self.table_fees_id}")[0]
        tbl_treatments = jQuery(f"#{self.table_treatment_id}")[0]
        case_uid = args['value']
        case_sel = Case.get(case_uid)
        print(f"case_uid = {case_uid}")
        print(f"case_sel = {case_sel}")

        case_expenses = Expense.search(case=case_sel)
        expense_output = ""
        medical_output = ""
        fees = 0.00
        treatment = 0.00
        reduction_25_default = 0.00
        for expense in case_expenses:
            if expense.activity.name != 'Medical Treatment':
                fees = fees + expense.total
                print(expense['uid'])
                expense_output = expense_output + "<tr class='settlement-tr'><td class='settlement-td'>" + expense.date.strftime("%b %d, %Y") + "</td><td class='settlement-td'>" + expense.activity.name + "</td><td class='settlement-td'>" + str(expense.quantity) + "</td><td class='settlement-td'>" + str(expense.amount) + "</td><td class='settlement-td'>" + str(expense.reduction) + "</td><td class='settlement-td'>" + str(expense.total) + "</td></tr>"
            else:
                treatment = treatment + expense.total
                reduction_25_default = treatment - treatment * .25
                medical_output = medical_output + "<tr class='settlement-tr'><td class='settlement-td'>" + expense.date.strftime("%b %d, %Y") + "</td><td class='settlement-td'>" + expense.activity.name + "</td><td class='settlement-td'>" + str(expense.quantity) + "</td><td class='settlement-td'>" + str(expense.amount) + "</td><td class='settlement-td'>" + str(expense.reduction) + "</td><td class='settlement-td'>" + str(expense.total) + "</td></tr>"
        self.total_fees.value = fees
        self.treatment_reduction.value = round(reduction_25_default, 2)
        self.total_treatment.value = treatment
        tbl_fee_costs.innerHTML = "<html><head><style>.settlement-table{border-collapse: collapse;width: 100%;}.settlement-td, .settlement-th {border: 1px solid #272d83;text-align: left;padding: 5px;}.settlement-tr:nth-child(even) {color: white;background-color: #272d83;}.settlement-tr:nth-child(even):hover {color: white;background-color: #898FDC;}.settlement-tr:nth-child(odd):hover {background-color: #f2f4f5;}</style></head><body><table class='settlement-table'><tr class='settlement-tr'><th class='settlement-th'>Date</th><th class='settlement-th'>Fees & Costs</th><th class='settlement-th'>Quantity</th><th class='settlement-th'>Amount</th><th class='settlement-th'>% Reduction</th><th class='settlement-th'>Total</th></tr>" + expense_output + "</table></body></html>"
        tbl_treatments.innerHTML = "<html><head><style>.settlement-table{border-collapse: collapse;width: 100%;}.settlement-td, .settlement-th {border: 1px solid #272d83;text-align: left;padding: 5px;}.settlement-tr:nth-child(even) {color: white;background-color: #272d83;}.settlement-tr:nth-child(even):hover {color: white;background-color: #898FDC;}.settlement-tr:nth-child(odd):hover {background-color: #f2f4f5;}</style></head><body><table class='settlement-table'><tr class='settlement-tr'><th class='settlement-th'>Date</th><th class='settlement-th'>Medical Treatment</th><th class='settlement-th'>Quantity</th><th class='settlement-th'>Amount</th><th class='settlement-th'>% Reduction</th><th class='settlement-th'>Total</th></tr>" + medical_output + "</table></body></html>"

    def dropdown_reduction_change(self, args):
        contingency_fee = jQuery(f"#{self.contingency_fee_id}")[0].value
        settlement_offer = jQuery(f"#{self.settlement_offer_id}")[0].value
        total_fee_costs = jQuery(f"#{self.total_fees_id}")[0].value
        total_treatment = jQuery(f"#{self.total_treatment_id}")[0].value
        case_uid = self.dropdown_cases.value
        if len(contingency_fee) > 0 and len(settlement_offer) > 0 and case_uid:
            contingency_fee = float(contingency_fee)
            settlement_offer = float(settlement_offer)
            total_treatment = float(total_treatment)
            total_fee_costs = float(total_fee_costs)
            attorneys_fee = 0.00
            client_net = 0.00
            total_medical_treatment = total_treatment
            reduction_range_calc = int(self.treatment_reduction.value.replace("%", "")) / 100.0
            reduction_range = total_medical_treatment - total_medical_treatment * reduction_range_calc
            contingency_fee_percent = contingency_fee / 100.0
            attorneys_fee = contingency_fee_percent * settlement_offer
            client_net = settlement_offer - total_fee_costs - reduction_range - attorneys_fee
            self.attorney_net.value = attorneys_fee
            self.client_net.value = client_net
            self.reduced_treatment.value = reduction_range

    def textbox_congingency_change(self, args):
        self.update_attorney_client()
    
    def textbox_settlement_change(self, args):
        self.update_attorney_client()

    def update_attorney_client(self):
        contingency_fee = jQuery(f"#{self.contingency_fee_id}")[0].value
        settlement_offer = jQuery(f"#{self.settlement_offer_id}")[0].value
        total_fee_costs = jQuery(f"#{self.total_fees_id}")[0].value
        reduced_treatment = jQuery(f"#{self.reduced_treatment_id}")[0].value
        
        if len(contingency_fee) > 0 and len(settlement_offer) > 0 and len(total_fee_costs) > 0 and len(reduced_treatment) > 0:
            contingency_fee = float(contingency_fee)
            settlement_offer = float(settlement_offer)
            total_fee_costs = float(total_fee_costs)
            reduced_treatment = float(reduced_treatment)
            attorneys_fee = 0.00
            client_net = 0.00
            contingency_fee_percent = contingency_fee / 100
            attorneys_fee = contingency_fee_percent * settlement_offer
            client_net = settlement_offer - total_fee_costs - reduced_treatment - attorneys_fee
            self.attorney_net.value = attorneys_fee
            self.client_net.value = client_net
