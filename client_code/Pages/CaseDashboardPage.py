from AnvilFusion.components.DashboardPage import DashboardPage
from AnvilFusion.tools.utils import set_cookie, get_cookie
from ..app.models import Case


class CaseDashboardPage(DashboardPage):
    
    def __init__(self, container_id, **kwargs):
        self.case_uid = kwargs.get('case_uid', None)
        if self.case_uid:
            set_cookie('case_uid', self.case_uid)
        else:
            self.case_uid = get_cookie('case_uid')
        print('CaseDashboardPage', self.case_uid)
        self.case = Case.get(self.case_uid) if self.case_uid else None
        
        layout = {
            'cellSpacing': [10, 10],
            'columns': 3,
            'cellAspectRatio': 100/50,
            'panels': [
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 0, 'col': 0,
                    'id': 'case_details', 'header': 'Case Details',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 1, 'col': 0,
                    'id': 'incident_date', 'header': 'Incident Date'
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 2, 'col': 0,
                    'id': 'cause_of_action', 'header': 'Cause(s) of Action',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 1, 'col': 1,
                    'id': 'case_status', 'header': 'Case Status',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 2, 'col': 1,
                    'id': 'custody_status', 'header': 'Custody Status',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 2,
                    'id': 'assigned_attorney', 'header': 'Assigned Attorney(s)',
                },
                {
                    'sizeX': 1, 'sizeY': 2, 'row': 1, 'col': 2,
                    'id': 'contacts',   'header': 'Contacts',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 3, 'col': 0,
                    'id': 'case_payments', 'header': 'Payment Status',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 4, 'col': 0,
                    'id': 'case_balances', 'header': 'Balances',
                },
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 3, 'col': 1,
                    'id': 'time_entries', 'header': 'Time Entries',
                },
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 4, 'col': 1,
                    'id': 'case_expenses', 'header': 'Expenses',
                },
            ],
        }
        if not self.case_uid:
            layout = {
                'panels': [
                    {'content': '<div>Case not selected</div>'}
                ]
            }

        super().__init__(
            layout=layout,
            container_id=container_id,
            container_style='margin-top: 10px; margin-right: 10px;',
            **kwargs
        )


    def form_show(self):
        super().form_show()
        if self.case:
            # case details
            panel_content = f"<h5>{self.case['case_name']}</h5>"
            panel_content += f"<h6>Case Number</h6>{self.case['case_number']}"
            panel_content += f"<h6>Practice Area</h6>{self.case['practice_area']['name']}"
            panel_content += f"<h6>Case Stage</h6>{self.case['case_stage']['name']}"
            panel_content += f"<h6>Court</h6>{self.case['court']['name']}"
            panel_content += f"<h6>Department</h6>{self.case['department']['full_name']}"
            panel_content += f"<h6>SOL</h6>{self.case['statute_of_limitations']}"
            panel_content += f"<div style='width:100%;height:100%;overflow:auto;'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'case_details',
                'content': panel_content,
            })
    