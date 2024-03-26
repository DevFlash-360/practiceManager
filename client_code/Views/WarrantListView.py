import anvil.server
from DevFusion.components.GridView2 import GridView2
from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid

from ..app.models import CaseStage, CaseStatus

class WarrantListView(GridView2):
    def __init__(self, **kwargs):
        pre_charge_uids = []
        case_stage_pre_charge = CaseStage.search(name='Pre-Charge')
        if case_stage_pre_charge:
            for ele in case_stage_pre_charge:
                pre_charge_uids.append(ele['uid'])
        view_config = {
            'model': 'Case',
            'columns': [
                {'name': 'uid', 'label': 'uid', 'visible': False},
                {'name': 'next_case_search', 'label': 'Next Case Search'},
                {'name': 'case_name', 'label': 'Case Name'},
                {'name': 'incident_location', 'label': 'Incident Location'},
                {'name': 'contacts.full_name', 'label': 'Contacts'},
            ]
        }
        filters = {'case_stage': {'uid': pre_charge_uids[0]}} if len(pre_charge_uids)>0 else None
        print(filters)
        # filters = {'case_stage': {'name': 'Pre-Charge'}, 'case_status': {'name': 'Open'}}
        super().__init__(model='Case', view_config=view_config, filters=filters, **kwargs)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
    
    def open_dashboard(self, args):
        AppEnv.navigation.show_menu('case_menu', subcomponent='case_dashboard',
                                    props={'case_uid': args.rowData.uid})
        # Expand AppSidebar Case Dashboard
        jQuery('#pm-sidebar-menu li.e-level-1').removeClass('e-active')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"]').addClass('e-active')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] div.e-icon-wrapper div.e-icons').removeClass('e-icon-expandable')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] div.e-icon-wrapper div.e-icons').addClass('e-icon-collapsible')
        jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] ul')[0].style.display = "block"
