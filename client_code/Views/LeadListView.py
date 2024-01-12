import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery
from ..app.models import Lead, User


class LeadListView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Lead',
            'columns': [
                {'name': 'case_name', 'label': 'Case Name'},
                {'name': 'retainer', 'label': 'Retainer'},
                {'name': 'lead_status', 'label': 'Lead Status'},
            ]
        }
        super().__init__(model='Lead', view_config=view_config, **kwargs)
        
    def row_selected(self, args):
        jQuery(f"#details_content")[0].innerHTML = self.details_content(args)
        super().row_selected(args)

    def details_content(self, args):
        lead = args['data']
        item = Lead.get(lead['uid'])
        intake_staffs = ', '.join([staff['full_name'] for staff in item['intake_staff']])
        lead_source = item['lead_source']['name'] if item['lead_source'] else None
        referred_by = item['referred_by']['full_name'] if item['referred_by'] else None
        practice_area = item['practice_area']['name'] if item['practice_area'] else None
        case_stage = item['case_stage']['name'] if item['case_stage'] else None
        cause_of_action = ', '.join([cause['cause_of_action'] for cause in item['cause_of_action']])
        contacts = ', '.join([contact['full_name'] for contact in item['contacts']])
        created_by = User.get(item['created_by']) if item['created_by'] else None
        if created_by:
            created_by = created_by['email']
        updated_by = User.get(item['updated_by']) if item['updated_by'] else None
        if updated_by:
            updated_by = updated_by['email']
            
        if item['lead_status'] is "Open":
            AppEnv.details.hide_reopen()
        else:
            AppEnv.details.show_reopen()

        content = "<div class='details_title'>Lead Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Lead Status</div>\
                <div class='details_record_data'>{item['lead_status']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Intake Staff</div>\
                <div class='details_record_data'>{intake_staffs}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Lead Source</div>\
                <div class='details_record_data'>{lead_source}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Referred By</div>\
                <div class='details_record_data'>{referred_by}</div>\
            </div>\
        </div>"

        content += "<div class='details_title'>Case Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Practice Area</div>\
                <div class='details_record_data'>{practice_area}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Name</div>\
                <div class='details_record_data'>{item['case_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Stage</div>\
                <div class='details_record_data'>{case_stage}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Cause of Action</div>\
                <div class='details_record_data'>{cause_of_action}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>SOL</div>\
                <div class='details_record_data'>{item['statute_of_limitations']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Number</div>\
                <div class='details_record_data'>{item['case_number']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Court</div>\
                <div class='details_record_data'>{item['court']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Department</div>\
                <div class='details_record_data'>{item['department']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Case Details</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Incident Date</div>\
                <div class='details_record_data'>{item['incident_date']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Incident Location</div>\
                <div class='details_record_data'>{item['incident_location']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Description</div>\
                <div class='details_record_data'>{item['case_description']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Billing Details</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Fee Type</div>\
                <div class='details_record_data'>{item['fee_type']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Retainer</div>\
                <div class='details_record_data'>{item['flat_fee_retainer']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Pre-Litigation Rate</div>\
                <div class='details_record_data'>{item['pre_litigation_rate']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Litigation Rate</div>\
                <div class='details_record_data'>{item['litigation_rate']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Trial Included</div>\
                <div class='details_record_data'>{item['trial_included']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Hours Limited on Retainer</div>\
                <div class='details_record_data'>{item['retainer_hours_limit']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Investigator Included</div>\
                <div class='details_record_data'>{item['investigator']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Investigator Budget</div>\
                <div class='details_record_data'>{item['investigator_budget']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Record Seal/Expungement Included</div>\
                <div class='details_record_data'>{item['record_seal_expungement']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Contacts</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Contacts</div>\
                <div class='details_record_data'>{contacts}</div>\
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
                <div class='details_record_data'>{item['created_time'].strftime('%m/%d/%Y %I:%M %p')}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Modified User</div>\
                <div class='details_record_data'>{updated_by}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Modified Time</div>\
                <div class='details_record_data'>{item['updated_time'].strftime('%m/%d/%Y %I:%M %p')}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>ID</div>\
                <div class='details_record_data'>{lead['uid']}</div>\
            </div>\
        <div>"

        return content
    
