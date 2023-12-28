import anvil.server
from AnvilFusion.components.DashboardPage import DashboardPage
from AnvilFusion.tools.utils import set_cookie, get_cookie
from ..app.models import Case


DASHBOARD_PANEL_CONTAINER_STYLE = "width:100%;height:100%;overflow:scroll;"


class CaseDashboardPage(DashboardPage):
    
    def __init__(self, container_id, **kwargs):
        self.case_uid = kwargs.get('case_uid', None)
        if self.case_uid:
            set_cookie('case_uid', self.case_uid)
        else:
            self.case_uid = get_cookie('case_uid')
        print('CaseDashboardPage', self.case_uid)
        self.case = Case.get(self.case_uid) if self.case_uid else None
        self.panel_container_style = DASHBOARD_PANEL_CONTAINER_STYLE
        
        layout = {
            'cellSpacing': [10, 10],
            'columns': 3,
            'cellAspectRatio': 100/50,
            'allowResizing': True,
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
            # panel_content += f"<h6>Department</h6>{self.case['department']['department_desc']}"
            panel_content += f"<h6>SOL</h6>{self.case['statute_of_limitations']}"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'case_details',
                'content': panel_content,
            })
            # incident date
            panel_content = f"<h5>{self.case['incident_date']}</h5>"
            panel_content += f"<h6>Incident Location</h6>{self.case['incident_location']}"
            panel_content += f"<h6>Case Description</h6>{self.case['case_description']}"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'incident_date',
                'content': panel_content,
            })
            # cause of action
            panel_content = f"<ul>"
            for cause in self.case['cause_of_action']:
                panel_content += f"<li>{cause['cause_of_action']}</li>"
            panel_content += f"</ul>"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'cause_of_action',
                'content': panel_content,
            })
            # case status
            # if 'case_status' in self.case and 'name' in self.case['case_status']:
            panel_content = f"<h5>{self.case['case_status']['name']}</h5>"
            panel_content += f"<h6>Last Update</h6>TBD"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'case_status',
                'content': panel_content,
            })
            # custody status
            panel_content = f"<h6>Custody Status</h6>TBD"
            panel_content += f"<h6>Jail/Prison</h6>TBD"
            panel_content += f"<h6>Inmate ID</h6>TBD"
            panel_content += f"<h6>Bail Status</h6>TBD"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'custody_status',
                'content': panel_content,
            })
            # assigned attorney
            panel_content = f"<ul>"
            for attorney in self.case['assigned_attorneys']:
                panel_content += f"<li>{attorney['full_name']}</li>"
            panel_content += f"</ul>"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'assigned_attorney',
                'content': panel_content,
            })
            # contacts
            panel_content = f"<ul>"
            for contact in self.case['contacts']:
                panel_content += f"<li>{contact['full_name']} - {contact['contact_group']['name']}</li>"
            panel_content += f"</ul>"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'contacts',
                'content': panel_content,
            })
            # case payments
            panel_content = f"<h5>TBD</h5>"
            panel_content += f"<h6>Fee Type</h6>{self.case['fee_type']['name']}"
            panel_content += f"<h6>Retainer</h6>${(self.case['flat_fee_retainer'] or self.case['hourly_retainer']) or 0:,.2f}"
            panel_content += f"<h6>Trial</h6>" + ("Not " if not self.case['trial_included'] else "") + "Included"
            panel_content += f"<h6>Retainer Hour Limit</h6>{self.case['retainer_hours_limit'] or 'Unlimited'}"
            panel_content += f"<h6>Investigator</h6>" + ("Not " if not self.case['investigator'] else "") + "Included"
            panel_content += f"<h6>Investigator Budget</h6>" + f"${self.case['investigator_budget']:,.2f}" if self.case['investigator'] else ""
            panel_content += f"<h6>Seal/Expungement</h6>" + ("Not " if not self.case['record_seal_expungement'] else "") + "Included"
            panel_content = f"<div style='{self.panel_container_style}'>{panel_content}</div>"
            self.dashboard.updatePanel({
                'id': 'case_payments',
                'content': panel_content,
            })
