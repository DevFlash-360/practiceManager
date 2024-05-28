import anvil.server
from DevFusion.components.GridView2 import GridView2
import anvil.js
from anvil.js.window import ej, jQuery
from ..app.models import Payroll, PayrollTotal


class PayrollView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Payroll',
            'columns': [
                {'name': 'start', 'label': 'Start', 'format': 'dd MMM, yyyy'},
                {'name': 'end', 'label': 'End', 'format': 'dd MMM, yyyy'},
                {'name': 'staffs.full_name', 'label': 'Staff'},
                {'name': 'total_payroll', 'label': 'Total Payroll'},
            ]
        }
        super().__init__(model='Payroll', view_config=view_config, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
    
    def row_selected(self, args):
        if type(args['data']).__name__ == 'Proxy':
            jQuery(f"#details_content")[0].innerHTML = self.details_content(args['data'])
        elif type(args['data']).__name__ == 'ProxyList':
            jQuery(f"#details_content")[0].innerHTML = self.details_content(args['data'][0])
        super().row_selected(args)

    def details_content(self, payroll):
        item = Payroll.get(payroll['uid'])
        payroll_totals = PayrollTotal.search(payroll=item)
        
        start_time = item['start'].strftime('%b %d, %Y') if item['start'] else ''
        end_time = item['end'].strftime('%b %d, %Y') if item['end'] else ''

        content = "<div class='details_title'>Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Start</div>\
                <div class='details_record_data'>{start_time}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>End</div>\
                <div class='details_record_data'>{end_time}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Total Payroll</div>\
                <div class='details_record_data'>{item['total_payroll']}</div>\
            </div>\
        </div>"
        
        content += "<div class='details_title'>Payroll Totals</div>"
        content += f"<div class='details-grid-6'>\
                <div class='details-grid-header'>Staff</div>\
                <div class='details-grid-header'>Total Base Pay</div>\
                <div class='details-grid-header'>Total Overtime Pay</div>\
                <div class='details-grid-header'>Total Incentive Pay</div>\
                <div class='details-grid-header'>Total Reimbursement Pay</div>\
                <div class='details-grid-header'>Total Pay</div>"
        for payroll_total in payroll_totals:
            content += f"<div class='details-grid-cell'>{payroll_total['staff']['full_name']}</div>\
                <div class='details-grid-cell'>{payroll_total['total_base_pay']}</div>\
                <div class='details-grid-cell'>{payroll_total['total_overtime_pay']}</div>\
                <div class='details-grid-cell'>{payroll_total['total_incentive_pay']}</div>\
                <div class='details-grid-cell'>{payroll_total['total_reimbursement_pay']}</div>\
                <div class='details-grid-cell'>{payroll_total['total_pay']}</div>"
        content += "</div>"
        return content
