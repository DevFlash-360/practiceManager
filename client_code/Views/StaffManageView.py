import anvil.server
from anvil.js.window import ej, jQuery
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid
from ..app.models import Staff, User


class StaffManageView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Staff',
            'columns': [
                {'name': 'full_name', 'label': 'Name'},
                {'name': 'staff_group.name', 'label': 'Staff Group'},
                {'name': 'work_email', 'label': 'Work Email'},
                {'name': 'work_phone', 'label': 'Work Phone'},
                {'name': 'extension', 'label': 'Extension'},
                {'name': 'hire_date', 'label': 'Hire Date'},
                {'name': 'leave_date', 'label': 'Leave Date'},
            ]
        }
        super().__init__(model='Staff', view_config=view_config, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)

    def row_selected(self, args):
        if type(args['data']).__name__ == 'Proxy':
            jQuery(f"#details_content")[0].innerHTML = self.details_content(args['data'])
        elif type(args['data']).__name__ == 'ProxyList':
            jQuery(f"#details_content")[0].innerHTML = self.details_content(args['data'][0])
        super().row_selected(args)
        
    def details_content(self, staff):
        item = Staff.get(staff['uid'])
        created_by = User.get(item['created_by']) if item['created_by'] else None
        if created_by:
            created_by = created_by['email']
        
        updated_by = User.get(item['updated_by']) if item['updated_by'] else None
        if updated_by:
            updated_by = updated_by['email']
            
        str_dob = item['date_of_birth'].strftime('%b %d, %Y') if item['date_of_birth'] else ""
        
        content = "<div class='details_title'>Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Name</div>\
                <div class='details_record_data'>{item['full_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Work Email</div>\
                <div class='details_record_data'>{item['work_email']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Work Phone</div>\
                <div class='details_record_data'>{item['work_phone']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Extension</div>\
                <div class='details_record_data'>{item['extension']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Compensation</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Pay Type</div>\
                <div class='details_record_data'>{item['pay_type']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Pay Rate</div>\
                <div class='details_record_data'>{item['pay_rate']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Mileage Reimbursement</div>\
                <div class='details_record_data'>{item['mileage_reimbursement']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Enable Overtime</div>\
                <div class='details_record_data'>{item['enable_overtime']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Overtime Rate</div>\
                <div class='details_record_data'>{item['overtime_rate']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Weekly Base Hours</div>\
                <div class='details_record_data'>{item['weekly_base_hours']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Enable Automatic Break-Time Deduction</div>\
                <div class='details_record_data'>{item['enable_break_time_deduction']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Break-time Hour Base</div>\
                <div class='details_record_data'>{item['break_time_hour_base']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Break-time Rate</div>\
                <div class='details_record_data'>{item['break_time_rate']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Enable Performance Incentives</div>\
                <div class='details_record_data'>{item['enable_performance_incentives']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Intake Staff Performance Incentive</div>\
                <div class='details_record_data'>{item['intake_performance_incentive']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Staff Override Incentive</div>\
                <div class='details_record_data'>{item['override_incentive']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Manager Override Incentive</div>\
                <div class='details_record_data'>{item['manager_incentive']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Referral Incentive</div>\
                <div class='details_record_data'>{item['referral_incentive']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Employment Information</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Emergency Contact</div>\
                <div class='details_record_data'>{item['emergency_contact_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Emergency Contact Phone</div>\
                <div class='details_record_data'>{item['emergency_contact_phone']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Emergency Contact Email</div>\
                <div class='details_record_data'>{item['emergency_contact_email']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Emergency Contact</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Employment Status</div>\
                <div class='details_record_data'>{item['employment_status']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Staff Group</div>\
                <div class='details_record_data'>{item['staff_group__name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Manager</div>\
                <div class='details_record_data'>{item['manager__full_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Hire Date</div>\
                <div class='details_record_data'>{item['hire_date']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Leave Date</div>\
                <div class='details_record_data'>{item['leave_date']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Personal Information</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Phone</div>\
                <div class='details_record_data'>{item['personal_phone']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Email</div>\
                <div class='details_record_data'>{item['personal_email']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Address</div>\
                <div class='details_record_data'>{item['personal_address']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>SSN</div>\
                <div class='details_record_data'>{item['personal_ssn']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>DOB</div>\
                <div class='details_record_data'>{str_dob}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Gender</div>\
                <div class='details_record_data'>{item['personal_gender']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Race</div>\
                <div class='details_record_data'>{item['personal_race']}</div>\
            </div>\
        <div>"
        content += "<div class='details_title'>Direct Deposit Information</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Bank Name</div>\
                <div class='details_record_data'>{item['bank_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Bank Routing Number</div>\
                <div class='details_record_data'>{item['bank_routing_number']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Bank Account Number</div>\
                <div class='details_record_data'>{item['bank_account_number']}</div>\
            </div>\
        <div>"
        content += "<div class='details_title'>Emergency Contact</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Emergency Contact</div>\
                <div class='details_record_data'>{item['emergency_contact_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Emergency Contact Phone</div>\
                <div class='details_record_data'>{item['emergency_contact_phone']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Emergency Contact Email</div>\
                <div class='details_record_data'>{item['emergency_contact_email']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Emergency Contact Address</div>\
                <div class='details_record_data'>{item['emergency_contact_address']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Record Data</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Added User</div>\
                <div class='details_record_data'>{created_by}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Added Time</div>\
                <div class='details_record_data'>{item['created_time'].strftime('%b %d, %Y @ %I:%M %p')}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Modified User</div>\
                <div class='details_record_data'>{updated_by}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Modified Time</div>\
                <div class='details_record_data'>{item['updated_time'].strftime('%b %d, %Y @ %I:%M %p')}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>ID</div>\
                <div class='details_record_data'>{staff['uid']}</div>\
            </div>\
        <div>"

        return content
