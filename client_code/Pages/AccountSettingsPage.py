import anvil.server
from AnvilFusion.components.SettingsPage import SettingsPage
from AnvilFusion.tools.utils import set_cookie, get_cookie
from ..app.models import Case


DASHBOARD_PANEL_CONTAINER_STYLE = "width:100%;height:100%;overflow:scroll;"


# won't work properly. need fix.
class AccountSettingsPage(SettingsPage):
    
    def __init__(self, container_id, **kwargs):
        self.case_uid = kwargs.get('case_uid', None)
        if self.case_uid:
            set_cookie('case_uid', self.case_uid)
            print(f"set_cookie {self.case_uid}")
        else:
            self.case_uid = get_cookie('case_uid')
            if not self.case_uid:
                self.case_uid = 'a31c356d-668c-4e62-b103-61869154adb1'
        print('CaseDashboardPage', self.case_uid)
        self.case = Case.get(self.case_uid) if self.case_uid else None
        self.panel_container_style = DASHBOARD_PANEL_CONTAINER_STYLE
        

    # won't work properly. need fix.
    def form_show(self):
        super().form_show()
        if self.case:
            # case details
            panel_content = f"<h5>{self.case['case_name']}</h5>"
            panel_content += f"<h6>Case Number</h6>{self.case['case_number']}"
            if self.case['practice_area']:
                panel_content += f"<h6>Practice Area</h6>{self.case['practice_area']['name']}"
            if self.case['case_stage']:
                panel_content += f"<h6>Case Stage</h6>{self.case['case_stage']['name']}"
            if self.case['court']:
                panel_content += f"<h6>Court</h6>{self.case['court']['name']}"
            # panel_content += f"<h6>Department</h6>{self.case['department']['department_desc']}"
            panel_content += f"<h6>SOL</h6>{self.case['statute_of_limitations']}"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'case_details',
                'content': panel_content,
            })