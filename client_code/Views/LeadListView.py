import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery
from ..app.models import Lead


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
        cause_of_action = item['cause_of_action']['cause_of_action'] if item['cause_of_action'] else None
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
        </div>"
        return content
    
    