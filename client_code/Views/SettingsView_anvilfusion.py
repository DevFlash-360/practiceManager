import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from datetime import timedelta
from anvil.js.window import ej, jQuery
import uuid
import anvil.js

class SettingsView(FormBase):

    def __init__(self, **kwargs):
      kwargs['model'] = 'Settings'

      admin_userlist_view = {
          'model': 'SettingsUserlist',
          'columns': [
              {'name': 'activity', 'label': 'Activity', 'width': '25%'},
              {'name': 'due_time', 'label': 'Due Time', 'width': '25%'},
              {'name': 'status', 'label': 'Satus', 'width': '15%'},
              {'name': '_spacer', 'label': '', 'width': '40%'},
          ],
      }
      self.user_permission = SubformGrid(name='user_permission', label='User Permission Settings', model='SettingsUserlist',
                                          link_model='Settings', link_field='settings', 
                                          form_container_id=kwargs.get('target'),
                                          view_config=admin_userlist_view,
                                          add_edit_form=SettingsUserlistForm,
                                          )

      # User -> notification settings
      self.in_app_notify = CheckboxInput(name='in_app_notification', label='Allow In App Notifications')
      self.email_notify = CheckboxInput(name='email_notify', label='Allow Email Notifications')
      self.case_name_syntax = CheckboxInput(name='case_name_syntax', label='Case Name Syntax')
      # User -> general settings
      self.general_username = TextInput(name='general_username', label='User Name')
      self.general_address = TextInput(name='general_address', label='Address')
      self.general_phone = TextInput(name='general_phone', label='Phone Number')
      # Tenant Settings -> General
      self.business_name = TextInput(name='business_name', label='Business Name')
      self.business_address = TextInput(name='business_address', label='Business Address')
      self.business_phone = TextInput(name='business_phone', label='Business Phone')
      # Tenant Settings -> Billing
      self.credit_card_info = TextInput(name='credit_card_info', label='Credit Card Infomation')
      self.billing_address = TextInput(name='billing_address', label='Billing Address')
      # Admin Settings -> add/adding/editing/removing users
      self.user_new = TextInput(name='user_new', label='New User')
      self.user_delete = TextInput(name='user_delete', label="Delete User")

      # # when save button cliked returns err
      # super().save.onClick() => {
        
      # }

      # title FormBase Add + {modelname}
      # super().modelName="Settings"

      # User Permission Settings when pressing + button
      
      
    
      tabs = [
        {'name': 'lead_details', 'label': 'User', 'sections': [
          {'name': 'notification_settings', 'label': 'Notification Settings', 'rows': [
            [
              self.in_app_notify,
              self.email_notify,
            ]
          ]},
          {'name': 'notification_settings', 'label': 'Case name syntax Settings', 'rows': [
            [
              self.case_name_syntax,
            ]
          ]},
          {'name': 'general_settings', 'label': 'General Settings', 'cols': [
            [
              self.general_username,
              self.general_address,
              self.general_phone,
            ],
          ]},
        ]},
        {'name': 'billing', 'label': 'Admin Settings', 'sections': [
            {'name': 'billing_details', 'label': 'User Add/Edit/Remove', 'rows': [
                [
                  self.user_new,
                  self.user_delete,
                ],
            ]},
            {'name': 'billing_details', 'label': 'User Permission', 'rows': [
                [
                  self.user_permission,
                ],
            ]},
        ]},
        {'name': 'tenant_settings', 'label': 'Tenant Settings', 'sections': [
            # {'name': '_', 'label': '', 'rows': [
            #     [self.lead_activities]
            # ]},
          {'name': 'tenant_general_settings', 'label': 'General Settings', 'cols': [
            [
              self.business_name,
              self.business_address,
              self.business_phone,
            ],
          ]},
          {'name': 'tenant_billing_settings', 'label': 'Billing Settings', 'cols': [
            [
              self.credit_card_info,
              self.billing_address,
            ],
          ]}
        ]},
        {'name': 'import_export', 'label': 'Import/Export', 'sections':[
          {'name':'_', 'label':'', 'cols':[
            [
              self.user_new
            ],
            [
              self.user_permission,
            ]
          ]}
        ]},
      ]

      super().__init__(tabs=tabs, width=POPUP_WIDTH_COL3, **kwargs)
      self.fullscreen = True
    
    # def form_open(self, args):
    #     super().form_open(args)
    #     # self.lead_status.hide()

    def form_show(self):
      super().form_show()
      # print(super().self.buttons)

  
    def after_open(self):
        print(f"after_open self.data = {self.data}")
        if not self.data:
          print('self.data is None')
        else:
          print('self.data exist!')


class SettingsUserlistForm(FormBase):

    def __init__(self, **kwargs):
        kwargs['model'] = 'SettingsUserlist'

        self.activity = TextInput(name='activity', label='Activity')
        self.due_time = DateTimeInput(name='due_time', label='Due Time')
        self.status = TextInput(name='status', label='Status')
        self.completed = CheckboxInput(name='completed', label='Completed', save=False)

        sections = [
            {'name': '_', 'cols': [
                [self.activity, self.due_time, self.status, self.completed],
            ]}
        ]

        # def click_plus_button():
        #   pass
      
        super().__init__(sections=sections, width=POPUP_WIDTH_COL1, **kwargs)
