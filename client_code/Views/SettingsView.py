import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *

PM_BI_COUNTRY = [
    'United States',
    'Ukraine',
    'United Kingdom',
    'Canada',
    'New Zealand',
]

PM_BI_STATE = [
  'Las Vegas',
  'California',
  'Texas',
]

class SettingsView:
  def __init__(self, container_id, **kwargs):
    self.container_id = container_id or AppEnv.content_container_id
    self.container_el = jQuery(f"#{self.container_id}")[0]

    # self.in_app_notify_id = f"in_app_notify_{uuid.uuid4()}"
    # self.email_notify_id = f"email_notify_{uuid.uuid4()}"
    self.user_name_id = f"user_name_{uuid.uuid4()}"
    self.user_address_id = f"user_address_{uuid.uuid4()}"
    self.user_email_id = f"user_email_{uuid.uuid4()}"
    self.user_phone_id = f"user_phone_{uuid.uuid4()}"
    self.user_birthday_id = f"user_birthday_{uuid.uuid4()}"
    self.user_gender_id = f"user_gender_{uuid.uuid4()}"
    # self.business_name_id = f"business_name_{uuid.uuid4()}"
    # self.business_address_id = f"business_address_{uuid.uuid4()}"
    # self.business_phone_id = f"business_phone_{uuid.uuid4()}"
    
    self.admin_new_user_id = f"admin_new_user_{uuid.uuid4()}"
    self.admin_delete_user_id = f"admin_delete_user_{uuid.uuid4()}"
    self.admin_user_permissions_id = f"admin_user_permissions_{uuid.uuid4()}"
    
    # self.in_app_notify = ej.buttons.CheckBox({
    #   'label': 'In App Notification',
    #   'checked': False
    # })
    # self.email_notify = ej.buttons.CheckBox({
    #   'label': 'Email Notification',
    #   'checked': False
    # })
    self.user_name = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.user_address = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.user_email = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.user_phone = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.user_birthday = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.user_gender = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    # self.business_name = ej.inputs.TextBox({
    #   'floatLabelType': 'Auto'
    # })
    # self.business_address = ej.inputs.TextBox({
    #   'floatLabelType': 'Auto'
    # })
    # self.business_phone = ej.inputs.TextBox({
    #   'floatLabelType': 'Auto'
    # })

    # My Notification Settings
    self.nt_cases_1 = CheckboxInput(name='nt_cases_1')
    self.nt_cases_2 = CheckboxInput(name='nt_cases_2')
    self.nt_cases_new_1 = CheckboxInput(name='nt_cases_new_1')
    self.nt_cases_new_2 = CheckboxInput(name='nt_cases_new_2')
    self.nt_case_update_1 = CheckboxInput(name='nt_case_update_1')
    self.nt_case_update_2 = CheckboxInput(name='nt_case_update_2')
    self.nt_case_close_1 = CheckboxInput(name='nt_case_close_1')
    self.nt_case_close_2 = CheckboxInput(name='nt_case_close_2')
    self.nt_case_reopen_1 = CheckboxInput(name='nt_case_reopen_1')
    self.nt_case_reopen_2 = CheckboxInput(name='nt_case_reopen_2')
    self.nt_case_delete_1 = CheckboxInput(name='nt_case_delete_1')
    self.nt_case_delete_2 = CheckboxInput(name='nt_case_delete_2')
    self.nt_case_note_1 = CheckboxInput(name='nt_case_note_1')
    self.nt_case_note_2 = CheckboxInput(name='nt_case_note_2')
    self.nt_case_you_1 = CheckboxInput(name='nt_case_you_1')
    self.nt_case_you_2 = CheckboxInput(name='nt_case_you_2')
    self.nt_case_company_1 = CheckboxInput(name='nt_case_company_1')
    self.nt_case_company_2 = CheckboxInput(name='nt_case_company_2')
    self.nt_case_user_1 = CheckboxInput(name='nt_case_user_1')
    self.nt_case_user_2 = CheckboxInput(name='nt_case_user_2')
    self.nt_calendar_1 = CheckboxInput(name='nt_calendar_1')
    self.nt_calendar_2 = CheckboxInput(name='nt_calendar_2')
    self.nt_calendar_3 = CheckboxInput(name='nt_calendar_3')
    self.nt_calendar_new_1 = CheckboxInput(name='nt_calendar_new_1')
    self.nt_calendar_new_2 = CheckboxInput(name='nt_calendar_new_2')
    self.nt_calendar_new_3 = CheckboxInput(name='nt_calendar_new_3')
    self.nt_calendar_update_1 = CheckboxInput(name='nt_calendar_update_1')
    self.nt_calendar_update_2 = CheckboxInput(name='nt_calendar_update_2')
    self.nt_calendar_delete_1 = CheckboxInput(name='nt_calendar_delete_1')
    self.nt_calendar_delete_2 = CheckboxInput(name='nt_calendar_delete_2')
    self.nt_calendar_comment_1 = CheckboxInput(name='nt_calendar_comment_1')
    self.nt_calendar_comment_2 = CheckboxInput(name='nt_calendar_comment_2')
    self.nt_calendar_comment_3 = CheckboxInput(name='nt_calendar_comment_3')
    self.nt_calendar_view_1 = CheckboxInput(name='nt_calendar_view_1')
    self.nt_calendar_view_2 = CheckboxInput(name='nt_calendar_view_2')
    self.nt_document_1 = CheckboxInput(name='nt_document_1')
    self.nt_document_2 = CheckboxInput(name='nt_document_2')
    self.nt_document_3 = CheckboxInput(name='nt_document_3')
    self.nt_document_new_1 = CheckboxInput(name='nt_document_new_1')
    self.nt_document_new_2 = CheckboxInput(name='nt_document_new_2')
    self.nt_document_new_3 = CheckboxInput(name='nt_document_new_3')
    self.nt_document_update_1 = CheckboxInput(name='nt_document_update_1')
    self.nt_document_update_2 = CheckboxInput(name='nt_document_update_2')
    self.nt_document_delete_1 = CheckboxInput(name='nt_document_delete_1')
    self.nt_document_delete_2 = CheckboxInput(name='nt_document_delete_2')
    self.nt_document_comment_1 = CheckboxInput(name='nt_document_comment_1')
    self.nt_document_comment_2 = CheckboxInput(name='nt_document_comment_2')
    self.nt_document_comment_3 = CheckboxInput(name='nt_document_comment_3')
    self.nt_document_view_1 = CheckboxInput(name='nt_document_view_1')
    self.nt_document_view_2 = CheckboxInput(name='nt_document_view_2')
    
    
    
    # Business Details 
    self.bd_office_name = TextInput(name='bd_office_name')
    self.bd_primary_office = CheckboxInput(name='bd_primary_office', label='This is our primary office')
    self.bd_main_phone = TextInput(name='bd_main_phone')
    self.bd_fax_line = TextInput(name='bd_fax_line')
    self.bd_address_address1 = TextInput(name='bd_address_address1', label='Address', placeholder="Address")
    self.bd_address_address2 = TextInput(name='bd_address_address2', label='Address 2')
    self.bd_address_city = TextInput(name='bd_address_city', label='City')
    self.bd_address_state = DropdownInput(name='bd_address_state', label='State', options=PM_BI_STATE)
    self.bd_address_zip = NumberInput(name='bd_address_zip', label='Zip')
    self.bd_address_country = DropdownInput(name='bd_address_country', label='Country', options=PM_BI_COUNTRY)
    

    # Billing Information
    self.bi_card_name = TextInput(name='bi_card_name', label='Card Name')
    self.bi_card_number = NumberInput(name='bi_card_number', label='Card Number')
    self.bi_card_cvv = NumberInput(name='bi_card_cvv', label='CVV')
    self.bi_card_month = NumberInput(name='bi_card_month', label='Month')
    self.bi_card_year = NumberInput(name='bi_card_year', label='Year')
    self.bi_address_address1 = TextInput(name='bi_address_address1', label='Address')
    self.bi_address_address2 = TextInput(name='bi_address_address2', label='Address 2')
    self.bi_address_city = TextInput(name='bi_address_city', label='City')
    self.bi_address_state = DropdownInput(name='bi_address_state', label='State', options=PM_BI_STATE)
    self.bi_address_zip = NumberInput(name='bi_address_zip', label='Zip')
    self.bi_address_country = DropdownInput(name='bi_address_country', label='Country', options=PM_BI_COUNTRY)
    
    self.admin_new_user = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.admin_delete_user = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.admin_user_permissions = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })

    self.user_password = TextInput(name='user_password', label='Password')

    notification_settings_html = self.prepare_notification_settings_html()
    user_profile_settings_html = self.prepare_user_profile_settings_html()
    admin_settings_html = self.prepare_admin_settings_html()
    business_details_settings_html = self.prepare_business_details_settings_html()
    billing_info_settings_html = self.prepare_billing_info_settings_html()
    self.userProfileTabInitialized  = False
    self.adminTabInitialized = False
    self.businessDetailsTabInitialized = False
    self.billingInfoTabInitialized = False
    
    self.tab = ej.navigations.Tab({
      # 'heightAdjustMode': 'Auto',
      # 'overflowMode': 'Popup',
      'items': [
        {'header': {'text': 'My Notification Settings'}, 'content': notification_settings_html},
        {'header': {'text': 'User Profile'}, 'content': user_profile_settings_html},
        {'header': {'text': 'Admin Settings'}, 'content': admin_settings_html},
        {'header': {'text': 'Business Details'}, 'content': business_details_settings_html},
        {'header': {'text': 'Billing Information'}, 'content': billing_info_settings_html}
      ],
      'selected': self.on_tab_selected
    })
    
  def form_show(self):
    self.container_el.innerHTML = f'\
      <div id="tab-element"></div>'
    self.tab.appendTo(jQuery("#tab-element")[0])

    self.init_notification_tab()

  # how to change the stylesheet of checkbox?
  def prepare_notification_settings_html(self):
    return f'''
      <div class="col-xs-12">
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">CASES</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div style="margin-top: -23px;">{self.nt_cases_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div style="margin-top: -23px;">{self.nt_cases_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new case is added to the system</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_cases_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_cases_new_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing case is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_update_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An open case is closed</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_close_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_close_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A closed case is reopened</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_reopen_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_reopen_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A closed case is deleted</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new note is added, edited, or deleted on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_note_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_note_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">You are added or removed from a case</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_you_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_you_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact / company is added or removed from a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_company_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_company_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A firm user is added or removed from a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_user_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_case_user_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">CALENDAR</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div style="margin-top: -23px;">{self.nt_calendar_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div style="margin-top: -23px;">{self.nt_calendar_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN-APP NOTIFICATION</div>
              <div style="margin-top: -23px;">{self.nt_calendar_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new event is added to the system</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_new_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_new_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing event is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_update_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes an event</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone comments on an event</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_comment_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_comment_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_comment_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact views an event</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_view_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_calendar_view_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">DOCUMENTS</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div style="margin-top: -23px;">{self.nt_document_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div style="margin-top: -23px;">{self.nt_document_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN-APP NOTIFICATION</div>
              <div style="margin-top: -23px;">{self.nt_document_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new document is uploaded in the system</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_new_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_new_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing document is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_update_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes a document</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone comments on a document</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_comment_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_comment_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_comment_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact views a document</div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_view_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div style="margin-top: -23px;">{self.nt_document_view_2.html}</div>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_user_profile_settings_html(self):
    return f'''
      <div>
        <h4 class ="col-xs-12" >General user profile settings</h4>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            <label for="{self.user_name_id}" style="white-space: nowrap;">User Name</label>\
            <input id="{self.user_name_id}"/>\
          </div>\
          <div class="col-xs-6" style=" align-items: center; ">\
            <label for="{self.user_email_id}" style="white-space: nowrap; margin-right:10px;">Email Address</label>\
            <input id="{self.user_email_id}"/>\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            <label for="{self.user_address_id}" style="white-space: nowrap;">Address</label>\
            <input id="{self.user_address_id}"/>\
          </div>\
          <div class="col-xs-6" style="align-items: center; ">\
            <label for="{self.user_phone_id}" style="white-space: nowrap; margin-right:10px;">Phone Number</label>\
            <input id="{self.user_phone_id}"/>\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            <label for="{self.user_birthday_id}" style="white-space: nowrap; margin-right:10px;">Date of Birth</label>\
            <input id="{self.user_birthday_id}"/>\
          </div>\
          <div class="col-xs-6" style="align-items: center; ">\
            <label for="{self.user_gender_id}" style="white-space: nowrap; margin-right:10px;">Gender</label>\
            <input id="{self.user_gender_id}"/>\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            <label for="{self.user_password.el_id}" style="white-space: nowrap; margin-right:10px;">{self.user_password.label}</label>\
            {self.user_password.html}\
          </div>\
        </div>\
      </div>
    '''

  def prepare_admin_settings_html(self):
    return f'''
      <h4 class ="col-xs-12" >Admin settings</h4>\
      <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.admin_new_user_id}" style="white-space: nowrap;">Add User</label>\
          <input id="{self.admin_new_user_id}"/>\
        </div>\
        <div class="col-xs-6" style=" align-items: center; ">\
          <label for="{self.admin_delete_user_id}" style="white-space: nowrap; margin-right:10px;">Delete User</label>\
          <input id="{self.admin_delete_user_id}"/>\
        </div>\
      </div>\
      <h4 class ="col-xs-12" >User Permissions</h4>\
      <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.admin_user_permissions_id}" style="white-space: nowrap;">Add User</label>\
          <input id="{self.admin_user_permissions_id}"/>\
        </div>\
      </div>\
    '''

  def prepare_business_details_settings_html(self):
    return f'''
      <div class ="col-xs-12 p-2" style="justify-content: center;">Offices</div>
      <div class ="col-xs-2 e-float-text e-label-top" style="justify-content: center;">Office Name</div>
      <div class ="col-xs-10" style="justify-content: center;">
        <div class ="col-xs-12 p-2" style="justify-content: center;">{self.bd_office_name.html}</div>
        <div class ="col-xs-12 p-2" style="justify-content: center; margin-top: -28px;">{self.bd_primary_office.html}</div>
      </div>
      <div class ="col-xs-2 e-float-text e-label-top" style="justify-content: center;">Main Phone</div>
      <div class ="col-xs-10" style="justify-content: center;">
        <div class ="col-xs-12 p-2" style="justify-content: center;">{self.bd_main_phone.html}</div>
      </div>
      <div class ="col-xs-2 e-float-text e-label-top" style="justify-content: center;">Fax Line</div>
      <div class ="col-xs-10" style="justify-content: center;">
        <div class ="col-xs-12 p-2" style="justify-content: center;">{self.bd_fax_line.html}</div>
      </div>
      <div class ="col-xs-2 e-float-text e-label-top" style="justify-content: center;">Address<span style="font-size: 10px">This address will be displayed on invoices and on merge fields for document templates.</span></div>
      <div class ="col-xs-10" style="justify-content: center;">
        <div class ="col-xs-12 p-2" style="justify-content: center;">{self.bd_address_address1.html}</div>
        <div class ="col-xs-12 p-2" style="justify-content: center;">{self.bd_address_address2.html}</div>
        <div class ="col-xs-6 p-2" style="justify-content: center;">{self.bd_address_city.html}</div>
        <div class ="col-xs-2 p-2" style="justify-content: center;">{self.bd_address_state.html}</div>
        <div class ="col-xs-4 p-2" style="justify-content: center;">{self.bd_address_zip.html}</div>
        <div class ="col-xs-12 p-2" style="justify-content: center;">{self.bd_address_country.html}</div>
      </div>
    '''

  def prepare_billing_info_settings_html(self):
    return f'''
      <div class ="col-xs-12 p-2" style="justify-content: center;">Credit Card Information</div>
      <div class ="col-xs-12" style="justify-content: center;">\
        {self.bi_card_name.html}
      </div>
      <div class="col-xs-9" style="align-items: center; ">\
        {self.bi_card_number.html}
      </div>\
      <div class="col-xs-3" style="align-items: center; ">\
        {self.bi_card_cvv.html}
      </div>\
      <div class="col-xs-8" style="align-items: center; ">\
        {self.bi_card_month.html}
      </div>\
      <div class="col-xs-4" style="align-items: center; ">\
        {self.bi_card_year.html}
      </div>\
      <div class ="col-xs-12 p-2" style="justify-content: center;">Billing Address</div>
      <div class ="col-xs-12" style="justify-content: center;">\
        {self.bi_address_address1.html}
      </div>
      <div class ="col-xs-12" style="justify-content: center;">\
        {self.bi_address_address2.html}
      </div>
      <div class="col-xs-6" style="align-items: center; ">\
        {self.bi_address_city.html}
      </div>\
      <div class="col-xs-2" style="align-items: center; ">\
        {self.bi_address_state.html}
      </div>\
      <div class="col-xs-4" style="align-items: center; ">\
        {self.bi_address_zip.html}
      </div>\
      <div class ="col-xs-12" style="justify-content: center;">\
        {self.bi_address_country.html}
      </div>
    '''
  
  def on_tab_selected(self, args):
    selected_index = args.selectedIndex
    # print('tab selected', selected_index)
    if selected_index == 1 and not self.userProfileTabInitialized:
      self.init_user_profile_tab()
      self.userProfileTabInitialized = True
    elif selected_index == 2 and not self.adminTabInitialized:
      self.init_admin_tab()
      self.adminTabInitialized = True
    elif selected_index == 3 and not self.businessDetailsTabInitialized:
      self.init_business_details_tab()
      self.businessDetailsTabInitialized = True
    elif selected_index == 4 and not self.billingInfoTabInitialized:
      self.init_billing_info_tab()
      self.billingInfoTabInitialized = True
      print('4th tab selected')
      print(self.bi_address_country.control)
      print(self.bi_address_country.html)
      print(self.bi_address_country.add_el_id)

  def init_notification_tab(self):
    self.nt_cases_1.create_control()
    self.nt_cases_1.control.appendTo(jQuery(f"#{self.nt_cases_1.el_id}")[0])
    self.nt_cases_2.create_control()
    self.nt_cases_2.control.appendTo(jQuery(f"#{self.nt_cases_2.el_id}")[0])
    self.nt_cases_new_1.create_control()
    self.nt_cases_new_1.control.appendTo(jQuery(f"#{self.nt_cases_new_1.el_id}")[0])
    self.nt_cases_new_2.create_control()
    self.nt_cases_new_2.control.appendTo(jQuery(f"#{self.nt_cases_new_2.el_id}")[0])
    self.nt_case_update_1.create_control()
    self.nt_case_update_1.control.appendTo(jQuery(f"#{self.nt_case_update_1.el_id}")[0])
    self.nt_case_update_2.create_control()
    self.nt_case_update_2.control.appendTo(jQuery(f"#{self.nt_case_update_2.el_id}")[0])
    self.nt_case_close_1.create_control()
    self.nt_case_close_1.control.appendTo(jQuery(f"#{self.nt_case_close_1.el_id}")[0])
    self.nt_case_close_2.create_control()
    self.nt_case_close_2.control.appendTo(jQuery(f"#{self.nt_case_close_2.el_id}")[0])
    self.nt_case_reopen_1.create_control()
    self.nt_case_reopen_1.control.appendTo(jQuery(f"#{self.nt_case_reopen_1.el_id}")[0])
    self.nt_case_reopen_2.create_control()
    self.nt_case_reopen_2.control.appendTo(jQuery(f"#{self.nt_case_reopen_2.el_id}")[0])
    self.nt_case_delete_1.create_control()
    self.nt_case_delete_1.control.appendTo(jQuery(f"#{self.nt_case_delete_1.el_id}")[0])
    self.nt_case_delete_2.create_control()
    self.nt_case_delete_2.control.appendTo(jQuery(f"#{self.nt_case_delete_2.el_id}")[0])
    self.nt_case_note_1.create_control()
    self.nt_case_note_1.control.appendTo(jQuery(f"#{self.nt_case_note_1.el_id}")[0])
    self.nt_case_note_2.create_control()
    self.nt_case_note_2.control.appendTo(jQuery(f"#{self.nt_case_note_2.el_id}")[0])
    self.nt_case_you_1.create_control()
    self.nt_case_you_1.control.appendTo(jQuery(f"#{self.nt_case_you_1.el_id}")[0])
    self.nt_case_you_2.create_control()
    self.nt_case_you_2.control.appendTo(jQuery(f"#{self.nt_case_you_2.el_id}")[0])
    self.nt_case_company_1.create_control()
    self.nt_case_company_1.control.appendTo(jQuery(f"#{self.nt_case_company_1.el_id}")[0])
    self.nt_case_company_2.create_control()
    self.nt_case_company_2.control.appendTo(jQuery(f"#{self.nt_case_company_2.el_id}")[0])
    self.nt_case_user_1.create_control()
    self.nt_case_user_1.control.appendTo(jQuery(f"#{self.nt_case_user_1.el_id}")[0])
    self.nt_case_user_2.create_control()
    self.nt_case_user_2.control.appendTo(jQuery(f"#{self.nt_case_user_2.el_id}")[0])
    self.nt_calendar_1.create_control()
    self.nt_calendar_1.control.appendTo(jQuery(f"#{self.nt_calendar_1.el_id}")[0])
    self.nt_calendar_2.create_control()
    self.nt_calendar_2.control.appendTo(jQuery(f"#{self.nt_calendar_2.el_id}")[0])
    self.nt_calendar_3.create_control()
    self.nt_calendar_3.control.appendTo(jQuery(f"#{self.nt_calendar_3.el_id}")[0])
    self.nt_calendar_new_1.create_control()
    self.nt_calendar_new_1.control.appendTo(jQuery(f"#{self.nt_calendar_new_1.el_id}")[0])
    self.nt_calendar_new_2.create_control()
    self.nt_calendar_new_2.control.appendTo(jQuery(f"#{self.nt_calendar_new_2.el_id}")[0])
    self.nt_calendar_new_3.create_control()
    self.nt_calendar_new_3.control.appendTo(jQuery(f"#{self.nt_calendar_new_3.el_id}")[0])
    self.nt_calendar_update_1.create_control()
    self.nt_calendar_update_1.control.appendTo(jQuery(f"#{self.nt_calendar_update_1.el_id}")[0])
    self.nt_calendar_update_2.create_control()
    self.nt_calendar_update_2.control.appendTo(jQuery(f"#{self.nt_calendar_update_2.el_id}")[0])
    self.nt_calendar_delete_1.create_control()
    self.nt_calendar_delete_1.control.appendTo(jQuery(f"#{self.nt_calendar_delete_1.el_id}")[0])
    self.nt_calendar_delete_2.create_control()
    self.nt_calendar_delete_2.control.appendTo(jQuery(f"#{self.nt_calendar_delete_2.el_id}")[0])
    self.nt_calendar_comment_1.create_control()
    self.nt_calendar_comment_1.control.appendTo(jQuery(f"#{self.nt_calendar_comment_1.el_id}")[0])
    self.nt_calendar_comment_2.create_control()
    self.nt_calendar_comment_2.control.appendTo(jQuery(f"#{self.nt_calendar_comment_2.el_id}")[0])
    self.nt_calendar_comment_3.create_control()
    self.nt_calendar_comment_3.control.appendTo(jQuery(f"#{self.nt_calendar_comment_3.el_id}")[0])
    self.nt_calendar_view_1.create_control()
    self.nt_calendar_view_1.control.appendTo(jQuery(f"#{self.nt_calendar_view_1.el_id}")[0])
    self.nt_calendar_view_2.create_control()
    self.nt_calendar_view_2.control.appendTo(jQuery(f"#{self.nt_calendar_view_2.el_id}")[0])
    self.nt_document_1.create_control()
    self.nt_document_1.control.appendTo(jQuery(f"#{self.nt_document_1.el_id}")[0])
    self.nt_document_2.create_control()
    self.nt_document_2.control.appendTo(jQuery(f"#{self.nt_document_2.el_id}")[0])
    self.nt_document_3.create_control()
    self.nt_document_3.control.appendTo(jQuery(f"#{self.nt_document_3.el_id}")[0])
    self.nt_document_new_1.create_control()
    self.nt_document_new_1.control.appendTo(jQuery(f"#{self.nt_document_new_1.el_id}")[0])
    self.nt_document_new_2.create_control()
    self.nt_document_new_2.control.appendTo(jQuery(f"#{self.nt_document_new_2.el_id}")[0])
    self.nt_document_new_3.create_control()
    self.nt_document_new_3.control.appendTo(jQuery(f"#{self.nt_document_new_3.el_id}")[0])
    self.nt_document_update_1.create_control()
    self.nt_document_update_1.control.appendTo(jQuery(f"#{self.nt_document_update_1.el_id}")[0])
    self.nt_document_update_2.create_control()
    self.nt_document_update_2.control.appendTo(jQuery(f"#{self.nt_document_update_2.el_id}")[0])
    self.nt_document_delete_1.create_control()
    self.nt_document_delete_1.control.appendTo(jQuery(f"#{self.nt_document_delete_1.el_id}")[0])
    self.nt_document_delete_2.create_control()
    self.nt_document_delete_2.control.appendTo(jQuery(f"#{self.nt_document_delete_2.el_id}")[0])
    self.nt_document_comment_1.create_control()
    self.nt_document_comment_1.control.appendTo(jQuery(f"#{self.nt_document_comment_1.el_id}")[0])
    self.nt_document_comment_2.create_control()
    self.nt_document_comment_2.control.appendTo(jQuery(f"#{self.nt_document_comment_2.el_id}")[0])
    self.nt_document_comment_3.create_control()
    self.nt_document_comment_3.control.appendTo(jQuery(f"#{self.nt_document_comment_3.el_id}")[0])
    self.nt_document_view_1.create_control()
    self.nt_document_view_1.control.appendTo(jQuery(f"#{self.nt_document_view_1.el_id}")[0])
    self.nt_document_view_2.create_control()
    self.nt_document_view_2.control.appendTo(jQuery(f"#{self.nt_document_view_2.el_id}")[0])

  
  def init_user_profile_tab(self):
    self.user_name.appendTo(jQuery(f"#{self.user_name_id}")[0])
    self.user_address.appendTo(jQuery(f"#{self.user_address_id}")[0])
    self.user_email.appendTo(jQuery(f"#{self.user_email_id}")[0])
    self.user_phone.appendTo(jQuery(f"#{self.user_phone_id}")[0])
    self.user_birthday.appendTo(jQuery(f"#{self.user_birthday_id}")[0])
    self.user_gender.appendTo(jQuery(f"#{self.user_gender_id}")[0])

  def init_admin_tab(self):
    self.admin_new_user.appendTo(jQuery(f"#{self.admin_new_user_id}")[0])
    self.admin_delete_user.appendTo(jQuery(f"#{self.admin_delete_user_id}")[0])
    self.admin_user_permissions.appendTo(jQuery(f"#{self.admin_user_permissions_id}")[0])

  def init_business_details_tab(self):
    # self.business_name.appendTo(jQuery(f"#{self.business_name_id}")[0])
    # self.business_address.appendTo(jQuery(f"#{self.business_address_id}")[0])
    # self.business_phone.appendTo(jQuery(f"#{self.business_phone_id}")[0])
    self.bd_office_name.create_control()
    self.bd_office_name.control.appendTo(jQuery(f"#{self.bd_office_name.el_id}")[0])
    self.bd_primary_office.create_control()
    self.bd_primary_office.control.appendTo(jQuery(f"#{self.bd_primary_office.el_id}")[0])
    self.bd_main_phone.create_control()
    self.bd_main_phone.control.appendTo(jQuery(f"#{self.bd_main_phone.el_id}")[0])
    self.bd_fax_line.create_control()
    self.bd_fax_line.control.appendTo(jQuery(f"#{self.bd_fax_line.el_id}")[0])
    self.bd_address_address1.create_control()
    self.bd_address_address1.control.appendTo(jQuery(f"#{self.bd_address_address1.el_id}")[0])
    self.bd_address_address2.create_control()
    self.bd_address_address2.control.appendTo(jQuery(f"#{self.bd_address_address2.el_id}")[0])
    self.bd_address_city.create_control()
    self.bd_address_city.control.appendTo(jQuery(f"#{self.bd_address_city.el_id}")[0])
    self.bd_address_state.create_control()
    self.bd_address_state.control.appendTo(jQuery(f"#{self.bd_address_state.el_id}")[0])
    self.bd_address_zip.create_control()
    self.bd_address_zip.control.appendTo(jQuery(f"#{self.bd_address_zip.el_id}")[0])
    self.bd_address_country.create_control()
    self.bd_address_country.control.appendTo(jQuery(f"#{self.bd_address_country.el_id}")[0])

  def init_billing_info_tab(self):
    # self.billing_credit_card.appendTo(jQuery(f"#{self.billing_credit_card_id}")[0])
    # self.billing_address.appendTo(jQuery(f"#{self.billing_address_id}")[0])
    self.bi_card_name.create_control()
    self.bi_card_name.control.appendTo(jQuery(f"#{self.bi_card_name.el_id}")[0])
    self.bi_card_number.create_control()
    self.bi_card_number.control.appendTo(jQuery(f"#{self.bi_card_number.el_id}")[0])
    self.bi_card_cvv.create_control()
    self.bi_card_cvv.control.appendTo(jQuery(f"#{self.bi_card_cvv.el_id}")[0])
    self.bi_card_month.create_control()
    self.bi_card_month.control.appendTo(jQuery(f"#{self.bi_card_month.el_id}")[0])
    self.bi_card_year.create_control()
    self.bi_card_year.control.appendTo(jQuery(f"#{self.bi_card_year.el_id}")[0])
    self.bi_address_address1.create_control()
    self.bi_address_address1.control.appendTo(jQuery(f"#{self.bi_address_address1.el_id}")[0])
    self.bi_address_address2.create_control()
    self.bi_address_address2.control.appendTo(jQuery(f"#{self.bi_address_address2.el_id}")[0])
    self.bi_address_city.create_control()
    self.bi_address_city.control.appendTo(jQuery(f"#{self.bi_address_city.el_id}")[0])
    self.bi_address_zip.create_control()
    self.bi_address_zip.control.appendTo(jQuery(f"#{self.bi_address_zip.el_id}")[0])
    self.bi_address_state.create_control()
    self.bi_address_state.control.appendTo(jQuery(f"#{self.bi_address_state.el_id}")[0])
    self.bi_address_country.create_control()
    self.bi_address_country.control.appendTo(jQuery(f"#{self.bi_address_country.el_id}")[0])
    pass
  
  def destroy(self):
    self.date_picker.destroy()
    self.radio_plus.destroy()
    self.radio_minus.destroy()
    self.radio_calendar.destroy()
    self.radio_business.destroy()
    self.numbers.destroy()
    if self.container_el:
      self.container_el.innerHTML = ''
