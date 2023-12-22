import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv



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
        
        AppEnv.navigation.show_menu('case_menu', subcomponent='case_dashboard',
                                    props={'case_uid': args.rowData.uid})
