import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv



class CaseListView(GridView2):
    def __init__(self, **kwargs):
        print('CaseListView')

        context_menu_items = [
            {'id': 'select_tenant', 'label': 'Open Dashboard', 'action': self.open_dashboard},
        ]

        super().__init__(
            model='Case',
            # view_config=view_config,
            context_menu_items=context_menu_items,
            **kwargs)


    def open_dashboard(self, args):
        AppEnv.navigation.show_menu('case_menu', subcomponent='case_dashboard',
                                    props={'case_uid': args.rowInfo.rowData.uid})
