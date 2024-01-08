import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery



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
        print(case)
        content = "<div class='details_title'>Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Name</div>\
                <div class='details_record_data'>{case['case_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Practice Area</div>\
                <div class='details_record_data'>{case['practice_area__name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Case Stage</div>\
                <div class='details_record_data'>{case['case_stage__name']}</div>\
            </div>\
        </div>"
        return content
