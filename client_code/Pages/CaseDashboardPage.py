from AnvilFusion.components.DashboardPage import DashboardPage


class CaseDashboardPage(DashboardPage):
    
    def __init__(self, container_id, **kwargs):
        
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
                    'sizeX': 1, 'sizeY': 2, 'row': 1, 'col': 0,
                    'id': 'incident_date', 'header': 'Incident Date'
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 3, 'col': 0,
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
                    'sizeX': 1, 'sizeY': 1, 'row': 4, 'col': 0,
                    'id': 'case_payments', 'header': 'Payment Status',
                },
                {
                    'sizeX': 1, 'sizeY': 1, 'row': 5, 'col': 0,
                    'id': 'case_balances', 'header': 'Balances',
                },
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 4, 'col': 1,
                    'id': 'time_entries', 'header': 'Time Entries',
                },
                {
                    'sizeX': 2, 'sizeY': 1, 'row': 5, 'col': 1,
                    'id': 'case_expenses', 'header': 'Expenses',
                },
            ],
        }
        
        super().__init__(
            layout=layout,
            container_id=container_id,
            container_style='margin-top: 10px; margin-right: 10px;',
            **kwargs
        )
    