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
        print(item['intake_staff'])
        intake_staffs = ', '.join([staff['full_name'] for staff in item['intake_staff']])
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
        </div>"

        content += "<div class='details_title'>Case Overview</div>"
        return content
    
    