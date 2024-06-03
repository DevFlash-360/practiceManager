import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv, get_cookie
from anvil.js.window import ej, jQuery
import anvil.js
import uuid


class CaseDocumentsView(GridView2):
    def __init__(self, case=None, case_uid=None, **kwargs):
        print('CaseDocumentsView')
        # self.filter_case_uid = None
        # is_dashboard = kwargs.pop('dashboard', None)
        # if is_dashboard:
        #     self.filter_case_uid = get_cookie('case_uid')

        view_config = {
            'model': 'Document',
            'columns': [
                {'name': 'folder.name', 'label': 'Folder'},
                {'name': 'title', 'label': 'Document Title'},
                {'name': 'file.name', 'label': 'File Name'},
                {'name': 'type', 'label': 'Type'},
                {'name': 'discovery', 'label': 'Discovery'},
                {'name': 'reviewed_by.full_name', 'label': 'Reviewed By'},
                {'name': 'notes', 'label': 'Notes'},
                # {'name': 'button', 'label': 'Button'},
            ],
            # 'filter': {'document_folder.case': self.filter_case_uid},
        }
        # if self.filter_case_uid:
        #     filters = {
        #         'case': {'uid': self.filter_case_uid}
        #     }
        # else:
        #     filters = None

        super().__init__(model='Document', view_config=view_config, **kwargs)
        # super().__init__(model='Document', view_config=view_config, filters=filters, **kwargs)
    #     self.grid.allowGrouping = True
    #     self.grid.groupSettings = {
    #         'columns': ['folder__name'],
    #         'showDropArea': False,
    #         'captionTemplate': '<div>${key} - ${count} files</div>',
    #     }
    #     # self.grid.editSettings = {
    #     #     'allowEditing': True,
    #     #     'allowAdding': False,
    #     #     'allowDeleting': True,
    #     #     'mode': 'Normal',
    #     # }
    #     # self.grid.dataBound = self.collapse_all
    #     self.first_load = True


    # def form_show(self, get_data=True, **args):
    #     super().form_show(get_data=get_data, **args)


    # def collapse_all(self, args):
    #     if self.first_load:
    #         self.grid.groupModule.collapseAll()
    #         self.first_load = False

    
    # def open_dashboard(self, args):
    #     AppEnv.navigation.show_menu('case_menu', subcomponent='case_dashboard',
    #                                 props={'case_uid': args.rowData.uid})
    #     # Expand AppSidebar Case Dashboard
    #     jQuery('#pm-sidebar-menu li.e-level-1').removeClass('e-active')
    #     jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"]').addClass('e-active')
    #     jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] div.e-icon-wrapper div.e-icons').removeClass('e-icon-expandable')
    #     jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] div.e-icon-wrapper div.e-icons').addClass('e-icon-collapsible')
    #     jQuery('#pm-sidebar-menu li[data-uid="case_dashboard"] ul')[0].style.display = "block"
