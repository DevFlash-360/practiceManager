from DevFusion.tools.utils import is_last_week, is_this_week, is_two_weeks_ago
import anvil.server
from DevFusion.components.GridView2 import GridView2
from anvil.js.window import ej, jQuery
from AnvilFusion.tools.utils import AppEnv, get_cookie
import anvil.js
import uuid
from datetime import datetime, timedelta

from ..app.models import CaseStage, CaseStatus, Case

class WarrantListView(GridView2):
    def __init__(self, **kwargs):
        self.pre_charge_uids = []
        case_stage_pre_charge = CaseStage.search(name='Pre-Charge')
        if case_stage_pre_charge:
            for ele in case_stage_pre_charge:
                self.pre_charge_uids.append(ele['uid'])
        view_config = {
            'model': 'Case',
            'isWarrant': True,
            'columns': [
                {'name': 'next_case_search', 'label': 'Next Case Search', 'format': 'MMM dd, yyyy'},
                {'name': 'case_name', 'label': 'Case Name'},
                {'name': 'incident_location', 'label': 'Incident Location'},
                {'name': 'contacts.full_name', 'label': 'Contacts'},
                {'name': 'case_stage.name', 'label': 'Case Stage', 'visible': False},
                {'name': 'case_status.name', 'label': 'Case Status', 'visible': False},
            ]
        }
        super().__init__(model='Case', view_config=view_config, **kwargs)

        self.grid.addEventListener('dataBound', self.handler_databound)

    def form_show(self, get_data=True, **args):
        super().form_show(get_data=get_data, **args)
        self.grid.clearFiltering()
        self.grid.filterByColumn('case_stage__name', 'equal', 'Pre-Charge')
        self.grid.filterByColumn('case_status__name', 'equal', 'Open')

        self.invalidate()
    
    def search_complete(self, args):
        case_obj = Case.get(args.rowData.uid)
        current_datetime = datetime.now()
        next_case_search_date = current_datetime + timedelta(weeks=1)

        case_obj.update({'next_case_search': next_case_search_date.date()})
        case_obj.save()

        self.update_grid(case_obj)

    def handler_databound(self, args):
        self.invalidate()
    
    def update_grid(self, data_row):
        if data_row.uid is None:
            data_row.uid = f"grid_{uuid.uuid4()}"
        grid_row = data_row.get_row_view(
            self.view_config['columns'],
            include_row=False,
            get_relationships=False,
        )
        self.update_grid_style(grid_row, False, False)

    def invalidate(self):
        rows = self.grid.element.querySelectorAll('.e-content .e-table .e-row')
        for _, row in enumerate(rows):
            search_button = row.querySelector('button')
            if not search_button:
                continue
            is_enable_search = False
            str_next_search = row.querySelector('td:nth-child(4)').textContent
            if not str_next_search or len(str_next_search) < 1:
                is_enable_search = True
            else:
                date_format = "%b %d, %Y"
                next_case_search = datetime.strptime(str_next_search, date_format).date()
                if next_case_search < (datetime.now() - timedelta(weeks=2)).date():
                    is_enable_search = True
                elif is_this_week(next_case_search):
                    is_enable_search = True
                elif is_last_week(next_case_search):
                    is_enable_search = True
                elif is_two_weeks_ago(next_case_search):
                    is_enable_search = True
            if is_enable_search:
                search_button.disabled = False
            else:
                search_button.disabled = True
