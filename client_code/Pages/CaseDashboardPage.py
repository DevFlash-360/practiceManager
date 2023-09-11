from AnvilFusion.components.DashboardPage import DashboardPage


class CaseDashboardPage(DashboardPage):
    
    def __init__(self, container_id, **kwargs):
        
        layout = {
            'showGridLines': True,
            'cellSpacing': [10, 10],
            'columns': 3,
            'cellAspectRatio': 100/50,
            'panels': [
                {'sizeX': 2, 'sizeY': 1, 'row': 0, 'col': 0, 'id': 'case_details',
                 'content': '<div class="content" style="line-height:60px">Case</div>'},
                {'sizeX': 1, 'sizeY': 2, 'row': 1, 'col': 0, 'id': 'incident_date',
                 'content': '<div class="content" style="line-height:60px">Incident Date</div>'},
                {'sizeX': 1, 'sizeY': 1, 'row': 3, 'col': 0, 'id': 'contacts',
                 'content': '<div class="content" style="line-height:60px">Contacts</div>'},
                {'sizeX': 1, 'sizeY': 1, 'row': 1, 'col': 1, 'id': 'cuase_of_action',
                 'content': '<div class="content" style="line-height:60px">Cause(s) of Action</div>'},
                {'sizeX': 1, 'sizeY': 1, 'row': 1, 'col': 1, 'id': 'custody_status',
                 'content': '<div class="content" style="line-height:60px">Custody Status</div>'},
                {'sizeX': 1, 'sizeY': 1, 'row': 0, 'col': 2, 'id': 'assigned_attorney',
                 'content': '<div class="content" style="line-height:60px">Assigned Attorney(s)</div>'},
                {'sizeX': 1, 'sizeY': 1, 'row': 1, 'col': 2, 'id': 'case_status',
                 'content': '<div class="content" style="line-height:60px">Case Status</div>'},
                {'sizeX': 1, 'sizeY': 2, 'row': 2, 'col': 2, 'id': 'case_payments',
                 'content': '<div class="content" style="line-height:60px">Payment Status</div>'},
                {'sizeX': 1, 'sizeY': 2, 'row': 4, 'col': 2, 'id': 'time_entries',
                 'content': '<div class="content" style="line-height:60px">Time Entries</div>'},
                {'sizeX': 1, 'sizeY': 1, 'row': 6, 'col': 2, 'id': 'case_expenses',
                 'content': '<div class="content" style="line-height:60px">Expenses</div>'},
                {'sizeX': 1, 'sizeY': 1, 'row': 7, 'col': 2, 'id': 'case_balances',
                 'content': '<div class="content" style="line-height:60px">Balances</div>'},
            ],
        }
        
        super().__init__(
            layout=layout,
            container_id=container_id,
            container_style='margin-top: 10px; margin-right: 10px;',
            **kwargs
        )
    