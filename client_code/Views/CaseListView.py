import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv



class CaseListView(GridView2):
    def __init__(self, **kwargs):
        print('CaseListView')

        super().__init__(
            model='Case',
            # view_config=view_config,
            **kwargs)


    def open_dashboard(self, args):
        AppEnv.navigation.show_menu('case_menu', subcomponent='case_dashboard',
                                    props={'case_uid': args.rowInfo.rowData.uid})
