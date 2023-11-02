from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv


class CaseListView(GridView):
    def __init__(self, **kwargs):
        print('CaseListView')

        context_menu_items = [
            {'id': 'select_tenant', 'label': 'Open Dashboard', 'action': AppEnv.navigation.show_menu('case_menu')},
        ]

        super().__init__(
            model='Case',
            # view_config=view_config,
            context_menu_items=context_menu_items,
            **kwargs)
