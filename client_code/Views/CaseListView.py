import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery
from ..app.models import Case, CaseStatus, User



class CaseListView(GridView2):
    def __init__(self, **kwargs):
        print('CaseListView')
        view_config = {
            'model': 'Case',
            'columns': [
                {'name': 'case_name', 'label': 'Case Name'},
                {'name': 'assigned_attorneys.full_name', 'label': 'Assigned Attorneys'},
                {'name': 'practice_area.name', 'label': 'Practice Area'},
                {'name': 'case_stage.name', 'label': 'Case Stage'},
                {'name': 'cause_of_action.cause_of_action', 'label': 'Causes) of Action'},
                {'name': 'close_date', 'label': 'Close Date'},

            ]
        }
        super().__init__(model='Case', view_config=view_config, **kwargs)


    def open_dashboard(self, args):
        print(f"CaseListview/open_dashboard args = {args}")
        AppEnv.navigation.show_menu('case_menu', subcomponent='case_dashboard',
                                    props={'case_uid': args.rowData.uid})
        # Expand AppSidebar Case Dashboard
        jQuery('#pm-sidebar-menu li.e-level-1').removeClass('e-active')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"]').addClass('e-active')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] div.e-icon-wrapper div.e-icons').removeClass('e-icon-expandable')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] div.e-icon-wrapper div.e-icons').addClass('e-icon-collapsible')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] ul')[0].style.display = "block"

    def row_selected(self, args):
        jQuery(f"#details_content")[0].innerHTML = self.details_content(args)
        super().row_selected(args)

    def details_content(self, args):
        case = args['data']
        item = Case.get(case['uid'])
        created_by = User.get(item['created_by']) if item['created_by'] else None
        if created_by:
            created_by = created_by['email']
        updated_by = User.get(item['updated_by']) if item['updated_by'] else None
        if updated_by:
            updated_by = updated_by['email']
        practice_area = case['practice_area__name'] if 'practice_area__name' in case else None
        case_stage = case['case_stage__name'] if 'case_stage__name' in case else None
        cause_of_action = case['cause_of_action__cause_of_action'] if 'cause_of_action__cause_of_action' in case else None
        assigned_attorneys = case['assigned_attorneys__full_name'] if 'assigned_attorneys__full_name' in case else None
        print(f"case_status = {item['case_status']}")
        case_status = item['case_status']['name'] if item['case_status'] else None
        content = "<div class='details_title'>Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Name</div>\
                <div class='details_record_data'>{case['case_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Practice Area</div>\
                <div class='details_record_data'>{practice_area}</div>\
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
                <div class='details_record_label'>Assigned Attorney</div>\
                <div class='details_record_data'>{assigned_attorneys}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Status</div>\
                <div class='details_record_data'>{case_status}</div>\
            </div>\
        </div>"

        content += "<div class='details_title'>Details</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Number</div>\
                <div class='details_record_data'>{item['case_number']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Close Date</div>\
                <div class='details_record_data'>{item['close_date']}</div>\
            </div>\
        <div>"

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
                <div class='details_record_data'>{case['uid']}</div>\
            </div>\
        <div>"
        return content
