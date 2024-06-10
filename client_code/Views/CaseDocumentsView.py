import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormBase import FormBase
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
            ],
        }
        super().__init__(model='Document', view_config=view_config, **kwargs)
      
    def open_settings_dlg(self, args):
      print('handled this ESign button click!!!!!!')
      try:
        form_class = getattr(AppEnv.forms, "ESignSettingsForm")
        # form_control = form_class(target = content_el_id)
        form_control = form_class(target = 'pm-content')
      except Exception as e:
          print(e.args)
          # form_control = FormBase(model="ESignSettings", target=content_el_id)
          form_control = FormBase(model="ESignSettings", target='pm-content')
      form_control.form_show()

# define open_settings_dlg to handle the ESign button click
# Bingo!! the pop-up is shown when the ESign button is clicked