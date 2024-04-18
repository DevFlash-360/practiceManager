import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *

from ..app.models import Staff, User

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
    self.user_emergency_address_id = f"user_emergency_address_{uuid.uuid4()}"
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
    self.nt_case_1 = CheckboxInput(name='nt_case_1')
    self.nt_case_2 = CheckboxInput(name='nt_case_2')
    self.nt_case_new_1 = CheckboxInput(name='nt_case_new_1')
    self.nt_case_new_2 = CheckboxInput(name='nt_case_new_2')
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
    self.nt_task_1 = CheckboxInput(name='nt_task_1')
    self.nt_task_2 = CheckboxInput(name='nt_task_2')
    self.nt_task_3 = CheckboxInput(name='nt_task_3')
    self.nt_task_new_1 = CheckboxInput(name='nt_task_new_1')
    self.nt_task_new_2 = CheckboxInput(name='nt_task_new_2')
    self.nt_task_new_3 = CheckboxInput(name='nt_task_new_3')
    self.nt_task_update_1 = CheckboxInput(name='nt_task_update_1')
    self.nt_task_update_2 = CheckboxInput(name='nt_task_update_2')
    self.nt_task_update_3 = CheckboxInput(name='nt_task_update_3')
    self.nt_task_delete_1 = CheckboxInput(name='nt_task_delete_1')
    self.nt_task_delete_2 = CheckboxInput(name='nt_task_delete_2')
    self.nt_task_complete_1 = CheckboxInput(name='nt_task_complete_1')
    self.nt_task_complete_2 = CheckboxInput(name='nt_task_complete_2')
    self.nt_task_incomplete_1 = CheckboxInput(name='nt_task_incomplete_1')
    self.nt_task_incomplete_2 = CheckboxInput(name='nt_task_incomplete_2')
    self.nt_time_1 = CheckboxInput(name='nt_time_1')
    self.nt_time_2 = CheckboxInput(name='nt_time_2')
    self.nt_time_new_1 = CheckboxInput(name='nt_time_new_1')
    self.nt_time_new_2 = CheckboxInput(name='nt_time_new_2')
    self.nt_time_update_1 = CheckboxInput(name='nt_time_update_1')
    self.nt_time_update_2 = CheckboxInput(name='nt_time_update_2')
    self.nt_time_delete_1 = CheckboxInput(name='nt_time_delete_1')
    self.nt_time_delete_2 = CheckboxInput(name='nt_time_delete_2')
    self.nt_time_inv_added_1 = CheckboxInput(name='nt_time_inv_added_1')
    self.nt_time_inv_added_2 = CheckboxInput(name='nt_time_inv_added_2')
    self.nt_time_inv_updated_1 = CheckboxInput(name='nt_time_inv_updated_1')
    self.nt_time_inv_updated_2 = CheckboxInput(name='nt_time_inv_updated_2')
    self.nt_time_inv_view_1 = CheckboxInput(name='nt_time_inv_view_1')
    self.nt_time_inv_view_2 = CheckboxInput(name='nt_time_inv_view_2')
    self.nt_time_inv_delete_1 = CheckboxInput(name='nt_time_inv_delete_1')
    self.nt_time_inv_delete_2 = CheckboxInput(name='nt_time_inv_delete_2')
    self.nt_time_pay_made_1 = CheckboxInput(name='nt_time_pay_made_1')
    self.nt_time_pay_made_2 = CheckboxInput(name='nt_time_pay_made_2')
    self.nt_time_pay_refunded_1 = CheckboxInput(name='nt_time_pay_refunded_1')
    self.nt_time_pay_refunded_2 = CheckboxInput(name='nt_time_pay_refunded_2')
    self.nt_time_share_1 = CheckboxInput(name='nt_time_share_1')
    self.nt_time_share_2 = CheckboxInput(name='nt_time_share_2')
    self.nt_time_reminder_1 = CheckboxInput(name='nt_time_reminder_1')
    self.nt_time_reminder_2 = CheckboxInput(name='nt_time_reminder_2')
    self.nt_contact_1 = CheckboxInput(name='nt_contact_1')
    self.nt_contact_2 = CheckboxInput(name='nt_contact_2')
    self.nt_contact_new_1 = CheckboxInput(name='nt_contact_new_1')
    self.nt_contact_new_2 = CheckboxInput(name='nt_contact_new_2')
    self.nt_contact_updated_1 = CheckboxInput(name='nt_contact_updated_1')
    self.nt_contact_updated_2 = CheckboxInput(name='nt_contact_updated_2')
    self.nt_contact_archive_1 = CheckboxInput(name='nt_contact_archive_1')
    self.nt_contact_archive_2 = CheckboxInput(name='nt_contact_archive_2')
    self.nt_contact_unarchive_1 = CheckboxInput(name='nt_contact_unarchive_1')
    self.nt_contact_unarchive_2 = CheckboxInput(name='nt_contact_unarchive_2')
    self.nt_contact_delete_1 = CheckboxInput(name='nt_contact_delete_1')
    self.nt_contact_delete_2 = CheckboxInput(name='nt_contact_delete_2')
    self.nt_contact_login_1 = CheckboxInput(name='nt_contact_login_1')
    self.nt_contact_login_2 = CheckboxInput(name='nt_contact_login_2')
    self.nt_contact_note_1 = CheckboxInput(name='nt_contact_note_1')
    self.nt_contact_note_2 = CheckboxInput(name='nt_contact_note_2')
    self.nt_firm_1 = CheckboxInput(name='nt_firm_1')
    self.nt_firm_2 = CheckboxInput(name='nt_firm_2')
    self.nt_firm_new_1 = CheckboxInput(name='nt_firm_new_1')
    self.nt_firm_new_2 = CheckboxInput(name='nt_firm_new_2')
    self.nt_firm_updated_1 = CheckboxInput(name='nt_firm_updated_1')
    self.nt_firm_updated_2 = CheckboxInput(name='nt_firm_updated_2')
    self.nt_firm_activate_1 = CheckboxInput(name='nt_firm_activate_1')
    self.nt_firm_activate_2 = CheckboxInput(name='nt_firm_activate_2')
    self.nt_firm_permission_1 = CheckboxInput(name='nt_firm_permission_1')
    self.nt_firm_permission_2 = CheckboxInput(name='nt_firm_permission_2')
    self.nt_firm_item_1 = CheckboxInput(name='nt_firm_item_1')
    self.nt_firm_item_2 = CheckboxInput(name='nt_firm_item_2')
    self.nt_firm_info_1 = CheckboxInput(name='nt_firm_info_1')
    self.nt_firm_info_2 = CheckboxInput(name='nt_firm_info_2')

    # User Profile
    self.user_first_name = TextInput(name='user_first_name', label='First Name')
    self.user_last_name = TextInput(name='user_last_name', label='Last Name')
    self.user_birthday = DateInput(name='user_birthday', label='Birthday')
    self.user_gender = TextInput(name='user_gender', label='Gender')
    self.user_race = TextInput(name='user_race', label='Personal race')
    self.user_username = TextInput(name='user_username', label='Username')
    self.user_password = TextInput(name='user_password', label='Password')
    self.user_work_email = TextInput(name='user_email', label='Work Email')
    self.user_work_phone = TextInput(name='user_work_phone', label='Work Phone')
    self.user_staff_group = TextInput(name='user_staff_group', label='Staff Group')
    self.user_work_extension = TextInput(name='user_work_extension', label='Work Extension')
    self.user_emergency_address = TextInput(name='user_emergency_address', label='Emergency Address')
    
    
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
              <div>{self.nt_case_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div>{self.nt_case_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new case is added to the system</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_new_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing case is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_update_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An open case is closed</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_close_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_close_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A closed case is reopened</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_reopen_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_reopen_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A closed case is deleted</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new note is added, edited, or deleted on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_note_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_note_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">You are added or removed from a case</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_you_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_you_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact / company is added or removed from a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_company_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_company_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A firm user is added or removed from a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_user_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_case_user_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">CALENDAR</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div>{self.nt_calendar_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div>{self.nt_calendar_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN-APP NOTIFICATION</div>
              <div>{self.nt_calendar_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new event is added to the system</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_new_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_new_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing event is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_update_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes an event</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone comments on an event</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_comment_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_comment_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_comment_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact views an event</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_view_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_calendar_view_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">DOCUMENTS</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div>{self.nt_document_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div>{self.nt_document_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN-APP NOTIFICATION</div>
              <div>{self.nt_document_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new document is uploaded in the system</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_new_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_new_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing document is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_update_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes a document</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone comments on a document</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_comment_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_comment_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_comment_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact views a document</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_view_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_document_view_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">TASKS</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div>{self.nt_task_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div>{self.nt_task_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN-APP NOTIFICATION</div>
              <div>{self.nt_task_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new task is added</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_new_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_new_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing task is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_update_2.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_update_3.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes a task</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A task is completed</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_complete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_complete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A completed task is marked incomplete</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_incomplete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_task_incomplete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">TIME & BILLING</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div>{self.nt_time_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div>{self.nt_time_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new time entry / expense is added</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_new_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing time entry / expense is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_update_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_update_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes a time entry / expense</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new invoice is added to a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_added_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_added_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing invoice is updated on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_updated_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_updated_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact views an invoice</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_view_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_view_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes an invoice on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_inv_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A payment is made on an invoice on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_pay_made_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_pay_made_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A payment is refunded on an invoice on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_pay_refunded_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_pay_refunded_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone shares an invoice on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_share_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_share_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone sends a reminder on a case you're linked to</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_reminder_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_time_reminder_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">CONTACTS & COMPANIES</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div>{self.nt_contact_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div>{self.nt_contact_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new contact/company is added to the system</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_new_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">An existing contact/company is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_updated_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_updated_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone archives a contact/company</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_archive_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_archive_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone unarchives a contact/company</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_unarchive_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_unarchive_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Someone deletes a company</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_delete_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_delete_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A contact logs in to MyCase</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_login_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_login_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new note is added, edited, or deleted on a contact</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_note_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_contact_note_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 p-5" style="background-color: rgba(200,200,200,.5); display:flex; align-items: center;">
            <div class="col-xs-6">FIRM ADMINISTRATION</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY EMAIL</div>
              <div>{self.nt_firm_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>IN ACTIVITY FEED</div>
              <div>{self.nt_firm_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A new firm user is added</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_new_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_new_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Firm user contact information is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_updated_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_updated_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">A firm user is deactivated or reactivated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_activate_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_activate_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Firm user permissions are changed</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_permission_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_permission_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Items are imported into MyCase</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_item_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_item_2.html}</div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class ="col-xs-12 p-5" style="display:flex; align-items: center;">
            <div class="col-xs-6">Firm information is updated</div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_info_1.html}</div>
            </div>
            <div class="col-xs-2" style="text-align: center;">
              <div>{self.nt_firm_info_2.html}</div>
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
            {self.user_first_name.html}\
          </div>\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_last_name.html}\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_birthday.html}\
          </div>\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_gender.html}\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_race.html}\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_username.html}\
          </div>\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_password.html}\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_work_email.html}\
          </div>\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_work_phone.html}\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_staff_group.html}\
          </div>\
          <div class="col-xs-6" style="align-items: center; ">\
            {self.user_work_extension.html}\
          </div>\
        </div>\
        <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
          <div class="col-xs-12" style="align-items: center; ">\
            {self.user_emergency_address.html}\
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
        <div class ="col-xs-12 p-2" style="justify-content: center;">{self.bd_primary_office.html}</div>
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
      self.display_user_profile_info()
    elif selected_index == 2 and not self.adminTabInitialized:
      self.init_admin_tab()
      self.adminTabInitialized = True
    elif selected_index == 3 and not self.businessDetailsTabInitialized:
      self.init_business_details_tab()
      self.businessDetailsTabInitialized = True
    elif selected_index == 4 and not self.billingInfoTabInitialized:
      self.init_billing_info_tab()
      self.billingInfoTabInitialized = True

  def init_notification_tab(self):
    self.nt_case_create_control()
    self.nt_case_set_attribute()
    self.nt_case_appendTo()
    self.nt_calendar_create_control()
    self.nt_calendar_set_attribute()
    self.nt_calendar_appendTo()
    self.nt_document_create_control()
    self.nt_document_set_attribute()
    self.nt_document_appendTo()
    self.nt_task_create_control()
    self.nt_task_set_attribute()
    self.nt_task_appendTo()
    self.nt_time_create_control()
    self.nt_time_set_attribute()
    self.nt_time_appendTo()
    self.nt_contact_create_control()
    self.nt_contact_set_attribute()
    self.nt_contact_appendTo()
    self.nt_firm_create_control()
    self.nt_firm_set_attribute()
    self.nt_firm_appendTo()

  def nt_case_create_control(self):
    self.nt_case_1.create_control()
    self.nt_case_2.create_control()
    self.nt_case_new_1.create_control()
    self.nt_case_new_2.create_control()
    self.nt_case_update_1.create_control()
    self.nt_case_update_2.create_control()
    self.nt_case_close_1.create_control()
    self.nt_case_close_2.create_control()
    self.nt_case_reopen_1.create_control()
    self.nt_case_reopen_2.create_control()
    self.nt_case_delete_1.create_control()
    self.nt_case_delete_2.create_control()
    self.nt_case_note_1.create_control()
    self.nt_case_note_2.create_control()
    self.nt_case_you_1.create_control()
    self.nt_case_you_2.create_control()
    self.nt_case_company_1.create_control()
    self.nt_case_company_2.create_control()
    self.nt_case_user_1.create_control()
    self.nt_case_user_2.create_control()
    self.nt_case_1.on_change = self.on_nt_case_change_all_1
    self.nt_case_2.on_change = self.on_nt_case_change_all_2
    self.nt_case_new_1.on_change = self.on_nt_case_change_1
    self.nt_case_new_2.on_change = self.on_nt_case_change_2
    self.nt_case_update_1.on_change = self.on_nt_case_change_1
    self.nt_case_update_2.on_change = self.on_nt_case_change_2
    self.nt_case_close_1.on_change = self.on_nt_case_change_1
    self.nt_case_close_2.on_change = self.on_nt_case_change_2
    self.nt_case_reopen_1.on_change = self.on_nt_case_change_1
    self.nt_case_reopen_2.on_change = self.on_nt_case_change_2
    self.nt_case_delete_1.on_change = self.on_nt_case_change_1
    self.nt_case_delete_2.on_change = self.on_nt_case_change_2
    self.nt_case_note_1.on_change = self.on_nt_case_change_1
    self.nt_case_note_2.on_change = self.on_nt_case_change_2
    self.nt_case_you_1.on_change = self.on_nt_case_change_1
    self.nt_case_you_2.on_change = self.on_nt_case_change_2
    self.nt_case_company_1.on_change = self.on_nt_case_change_1
    self.nt_case_company_2.on_change = self.on_nt_case_change_2
    self.nt_case_user_1.on_change = self.on_nt_case_change_1
    self.nt_case_user_2.on_change = self.on_nt_case_change_2
  
  def nt_case_set_attribute(self):
    self.nt_case_2.value = True
    self.nt_case_new_2.value = True
    self.nt_case_update_2.value = True
    self.nt_case_close_2.value = True
    self.nt_case_reopen_2.value = True
    self.nt_case_delete_2.value = True
    self.nt_case_note_2.value = True
    self.nt_case_you_2.value = True
    self.nt_case_company_2.value = True
    self.nt_case_user_2.value = True
  
  def nt_case_appendTo(self):
    self.nt_case_1.control.appendTo(jQuery(f"#{self.nt_case_1.el_id}")[0])
    self.nt_case_2.control.appendTo(jQuery(f"#{self.nt_case_2.el_id}")[0])
    self.nt_case_new_1.control.appendTo(jQuery(f"#{self.nt_case_new_1.el_id}")[0])
    self.nt_case_new_2.control.appendTo(jQuery(f"#{self.nt_case_new_2.el_id}")[0])
    self.nt_case_update_1.control.appendTo(jQuery(f"#{self.nt_case_update_1.el_id}")[0])
    self.nt_case_update_2.control.appendTo(jQuery(f"#{self.nt_case_update_2.el_id}")[0])
    self.nt_case_close_1.control.appendTo(jQuery(f"#{self.nt_case_close_1.el_id}")[0])
    self.nt_case_close_2.control.appendTo(jQuery(f"#{self.nt_case_close_2.el_id}")[0])
    self.nt_case_reopen_1.control.appendTo(jQuery(f"#{self.nt_case_reopen_1.el_id}")[0])
    self.nt_case_reopen_2.control.appendTo(jQuery(f"#{self.nt_case_reopen_2.el_id}")[0])
    self.nt_case_delete_1.control.appendTo(jQuery(f"#{self.nt_case_delete_1.el_id}")[0])
    self.nt_case_delete_2.control.appendTo(jQuery(f"#{self.nt_case_delete_2.el_id}")[0])
    self.nt_case_note_1.control.appendTo(jQuery(f"#{self.nt_case_note_1.el_id}")[0])
    self.nt_case_note_2.control.appendTo(jQuery(f"#{self.nt_case_note_2.el_id}")[0])
    self.nt_case_you_1.control.appendTo(jQuery(f"#{self.nt_case_you_1.el_id}")[0])
    self.nt_case_you_2.control.appendTo(jQuery(f"#{self.nt_case_you_2.el_id}")[0])
    self.nt_case_company_1.control.appendTo(jQuery(f"#{self.nt_case_company_1.el_id}")[0])
    self.nt_case_company_2.control.appendTo(jQuery(f"#{self.nt_case_company_2.el_id}")[0])
    self.nt_case_user_1.control.appendTo(jQuery(f"#{self.nt_case_user_1.el_id}")[0])
    self.nt_case_user_2.control.appendTo(jQuery(f"#{self.nt_case_user_2.el_id}")[0])

  def nt_calendar_create_control(self):
    self.nt_calendar_1.create_control()
    self.nt_calendar_2.create_control()
    self.nt_calendar_3.create_control()
    self.nt_calendar_new_1.create_control()
    self.nt_calendar_new_2.create_control()
    self.nt_calendar_new_3.create_control()
    self.nt_calendar_update_1.create_control()
    self.nt_calendar_update_2.create_control()
    self.nt_calendar_delete_1.create_control()
    self.nt_calendar_delete_2.create_control()
    self.nt_calendar_comment_1.create_control()
    self.nt_calendar_comment_2.create_control()
    self.nt_calendar_comment_3.create_control()
    self.nt_calendar_view_1.create_control()
    self.nt_calendar_view_2.create_control()
    self.nt_calendar_1.on_change = self.on_nt_calendar_change_all_1
    self.nt_calendar_2.on_change = self.on_nt_calendar_change_all_2
    self.nt_calendar_3.on_change = self.on_nt_calendar_change_all_3
    self.nt_calendar_new_1.on_change = self.on_nt_calendar_change_1
    self.nt_calendar_new_2.on_change = self.on_nt_calendar_change_2
    self.nt_calendar_new_3.on_change = self.on_nt_calendar_change_3
    self.nt_calendar_update_1.on_change = self.on_nt_calendar_change_1
    self.nt_calendar_update_2.on_change = self.on_nt_calendar_change_2
    self.nt_calendar_delete_1.on_change = self.on_nt_calendar_change_1
    self.nt_calendar_delete_2.on_change = self.on_nt_calendar_change_2
    self.nt_calendar_comment_1.on_change = self.on_nt_calendar_change_1
    self.nt_calendar_comment_2.on_change = self.on_nt_calendar_change_2
    self.nt_calendar_comment_3.on_change = self.on_nt_calendar_change_3
    self.nt_calendar_view_1.on_change = self.on_nt_calendar_change_1
    self.nt_calendar_view_2.on_change = self.on_nt_calendar_change_2
    

  def nt_calendar_set_attribute(self):
    self.nt_calendar_1.control.indeterminate = True
    self.nt_calendar_1.enabled = False
    self.nt_calendar_2.value = True
    self.nt_calendar_3.value = True
    self.nt_calendar_3.enabled = False
    self.nt_calendar_new_2.value = True
    self.nt_calendar_new_3.value = True
    self.nt_calendar_update_2.value = True
    self.nt_calendar_delete_2.value = True
    self.nt_calendar_comment_1.value = True
    self.nt_calendar_comment_1.enabled = False
    self.nt_calendar_comment_2.value = True
    self.nt_calendar_comment_3.value = True
    self.nt_calendar_comment_3.enabled = False
    self.nt_calendar_view_2.value = True

  def nt_calendar_appendTo(self):
    self.nt_calendar_1.control.appendTo(jQuery(f"#{self.nt_calendar_1.el_id}")[0])
    self.nt_calendar_2.control.appendTo(jQuery(f"#{self.nt_calendar_2.el_id}")[0])
    self.nt_calendar_3.control.appendTo(jQuery(f"#{self.nt_calendar_3.el_id}")[0])
    self.nt_calendar_new_1.control.appendTo(jQuery(f"#{self.nt_calendar_new_1.el_id}")[0])
    self.nt_calendar_new_2.control.appendTo(jQuery(f"#{self.nt_calendar_new_2.el_id}")[0])
    self.nt_calendar_new_3.control.appendTo(jQuery(f"#{self.nt_calendar_new_3.el_id}")[0])
    self.nt_calendar_update_1.control.appendTo(jQuery(f"#{self.nt_calendar_update_1.el_id}")[0])
    self.nt_calendar_update_2.control.appendTo(jQuery(f"#{self.nt_calendar_update_2.el_id}")[0])
    self.nt_calendar_delete_1.control.appendTo(jQuery(f"#{self.nt_calendar_delete_1.el_id}")[0])
    self.nt_calendar_delete_2.control.appendTo(jQuery(f"#{self.nt_calendar_delete_2.el_id}")[0])
    self.nt_calendar_comment_1.control.appendTo(jQuery(f"#{self.nt_calendar_comment_1.el_id}")[0])
    self.nt_calendar_comment_2.control.appendTo(jQuery(f"#{self.nt_calendar_comment_2.el_id}")[0])
    self.nt_calendar_comment_3.control.appendTo(jQuery(f"#{self.nt_calendar_comment_3.el_id}")[0])
    self.nt_calendar_view_1.control.appendTo(jQuery(f"#{self.nt_calendar_view_1.el_id}")[0])
    self.nt_calendar_view_2.control.appendTo(jQuery(f"#{self.nt_calendar_view_2.el_id}")[0])

  def nt_document_create_control(self):
    self.nt_document_1.create_control()
    self.nt_document_2.create_control()
    self.nt_document_3.create_control()
    self.nt_document_new_1.create_control()
    self.nt_document_new_2.create_control()
    self.nt_document_new_3.create_control()
    self.nt_document_update_1.create_control()
    self.nt_document_update_2.create_control()
    self.nt_document_delete_1.create_control()
    self.nt_document_delete_2.create_control()
    self.nt_document_comment_1.create_control()
    self.nt_document_comment_2.create_control()
    self.nt_document_comment_3.create_control()
    self.nt_document_view_1.create_control()
    self.nt_document_view_2.create_control()
    self.nt_document_1.on_change = self.on_nt_document_change_all_1
    self.nt_document_2.on_change = self.on_nt_document_change_all_2
    self.nt_document_3.on_change = self.on_nt_document_change_all_3
    self.nt_document_new_1.on_change = self.on_nt_document_change_1
    self.nt_document_new_2.on_change = self.on_nt_document_change_2
    self.nt_document_new_3.on_change = self.on_nt_document_change_3
    self.nt_document_update_1.on_change = self.on_nt_document_change_1
    self.nt_document_update_2.on_change = self.on_nt_document_change_2
    self.nt_document_delete_1.on_change = self.on_nt_document_change_1
    self.nt_document_delete_2.on_change = self.on_nt_document_change_2
    self.nt_document_comment_1.on_change = self.on_nt_document_change_1
    self.nt_document_comment_2.on_change = self.on_nt_document_change_2
    self.nt_document_comment_3.on_change = self.on_nt_document_change_3
    self.nt_document_view_1.on_change = self.on_nt_document_change_1
    self.nt_document_view_2.on_change = self.on_nt_document_change_2

  def nt_document_set_attribute(self):
    self.nt_document_1.control.indeterminate = True
    self.nt_document_1.enabled = False
    self.nt_document_2.value = True
    self.nt_document_3.value = True
    self.nt_document_3.enabled = False
    self.nt_document_new_2.value = True
    self.nt_document_new_3.value = True
    self.nt_document_update_2.value = True
    self.nt_document_delete_2.value = True
    self.nt_document_comment_1.value = True
    self.nt_document_comment_1.enabled = False
    self.nt_document_comment_2.value = True
    self.nt_document_comment_3.value = True
    self.nt_document_comment_3.enabled = False
    self.nt_document_view_2.value = True
  
  def nt_document_appendTo(self):
    self.nt_document_1.control.appendTo(jQuery(f"#{self.nt_document_1.el_id}")[0])
    self.nt_document_2.control.appendTo(jQuery(f"#{self.nt_document_2.el_id}")[0])
    self.nt_document_3.control.appendTo(jQuery(f"#{self.nt_document_3.el_id}")[0])
    self.nt_document_new_1.control.appendTo(jQuery(f"#{self.nt_document_new_1.el_id}")[0])
    self.nt_document_new_2.control.appendTo(jQuery(f"#{self.nt_document_new_2.el_id}")[0])
    self.nt_document_new_3.control.appendTo(jQuery(f"#{self.nt_document_new_3.el_id}")[0])
    self.nt_document_update_1.control.appendTo(jQuery(f"#{self.nt_document_update_1.el_id}")[0])
    self.nt_document_update_2.control.appendTo(jQuery(f"#{self.nt_document_update_2.el_id}")[0])
    self.nt_document_delete_1.control.appendTo(jQuery(f"#{self.nt_document_delete_1.el_id}")[0])
    self.nt_document_delete_2.control.appendTo(jQuery(f"#{self.nt_document_delete_2.el_id}")[0])
    self.nt_document_comment_1.control.appendTo(jQuery(f"#{self.nt_document_comment_1.el_id}")[0])
    self.nt_document_comment_2.control.appendTo(jQuery(f"#{self.nt_document_comment_2.el_id}")[0])
    self.nt_document_comment_3.control.appendTo(jQuery(f"#{self.nt_document_comment_3.el_id}")[0])
    self.nt_document_view_1.control.appendTo(jQuery(f"#{self.nt_document_view_1.el_id}")[0])
    self.nt_document_view_2.control.appendTo(jQuery(f"#{self.nt_document_view_2.el_id}")[0])

  def nt_task_create_control(self):
    self.nt_task_1.create_control()
    self.nt_task_2.create_control()
    self.nt_task_3.create_control()
    self.nt_task_new_1.create_control()
    self.nt_task_new_2.create_control()
    self.nt_task_new_3.create_control()
    self.nt_task_update_1.create_control()
    self.nt_task_update_2.create_control()
    self.nt_task_update_3.create_control()
    self.nt_task_delete_1.create_control()
    self.nt_task_delete_2.create_control()
    self.nt_task_complete_1.create_control()
    self.nt_task_complete_2.create_control()
    self.nt_task_incomplete_1.create_control()
    self.nt_task_incomplete_2.create_control()
    self.nt_task_1.on_change = self.on_nt_task_change_all_1
    self.nt_task_2.on_change = self.on_nt_task_change_all_2
    self.nt_task_3.on_change = self.on_nt_task_change_all_3
    self.nt_task_new_1.on_change = self.on_nt_task_change_1
    self.nt_task_new_2.on_change = self.on_nt_task_change_2
    self.nt_task_new_3.on_change = self.on_nt_task_change_3
    self.nt_task_update_1.on_change = self.on_nt_task_change_1
    self.nt_task_update_2.on_change = self.on_nt_task_change_2
    self.nt_task_update_3.on_change = self.on_nt_task_change_3
    self.nt_task_delete_1.on_change = self.on_nt_task_change_1
    self.nt_task_delete_2.on_change = self.on_nt_task_change_2
    self.nt_task_complete_1.on_change = self.on_nt_task_change_1
    self.nt_task_complete_2.on_change = self.on_nt_task_change_2
    self.nt_task_incomplete_1.on_change = self.on_nt_task_change_1
    self.nt_task_incomplete_2.on_change = self.on_nt_task_change_2

  def nt_task_set_attribute(self):
    self.nt_task_2.value = True
    self.nt_task_3.value = True
    self.nt_task_new_2.value = True
    self.nt_task_new_3.value = True
    self.nt_task_update_2.value = True
    self.nt_task_update_3.value = True
    self.nt_task_delete_2.value = True
    self.nt_task_complete_2.value = True
    self.nt_task_incomplete_2.value = True

  def nt_task_appendTo(self):
    self.nt_task_1.control.appendTo(jQuery(f"#{self.nt_task_1.el_id}")[0])
    self.nt_task_2.control.appendTo(jQuery(f"#{self.nt_task_2.el_id}")[0])
    self.nt_task_3.control.appendTo(jQuery(f"#{self.nt_task_3.el_id}")[0])
    self.nt_task_new_1.control.appendTo(jQuery(f"#{self.nt_task_new_1.el_id}")[0])
    self.nt_task_new_2.control.appendTo(jQuery(f"#{self.nt_task_new_2.el_id}")[0])
    self.nt_task_new_3.control.appendTo(jQuery(f"#{self.nt_task_new_3.el_id}")[0])
    self.nt_task_update_1.control.appendTo(jQuery(f"#{self.nt_task_update_1.el_id}")[0])
    self.nt_task_update_2.control.appendTo(jQuery(f"#{self.nt_task_update_2.el_id}")[0])
    self.nt_task_update_3.control.appendTo(jQuery(f"#{self.nt_task_update_3.el_id}")[0])
    self.nt_task_delete_1.control.appendTo(jQuery(f"#{self.nt_task_delete_1.el_id}")[0])
    self.nt_task_delete_2.control.appendTo(jQuery(f"#{self.nt_task_delete_2.el_id}")[0])
    self.nt_task_complete_1.control.appendTo(jQuery(f"#{self.nt_task_complete_1.el_id}")[0])
    self.nt_task_complete_2.control.appendTo(jQuery(f"#{self.nt_task_complete_2.el_id}")[0])
    self.nt_task_incomplete_1.control.appendTo(jQuery(f"#{self.nt_task_incomplete_1.el_id}")[0])
    self.nt_task_incomplete_2.control.appendTo(jQuery(f"#{self.nt_task_incomplete_2.el_id}")[0])
  
  def nt_time_create_control(self):
    self.nt_time_1.create_control()
    self.nt_time_2.create_control()
    self.nt_time_new_1.create_control()
    self.nt_time_new_2.create_control()
    self.nt_time_update_1.create_control()
    self.nt_time_update_2.create_control()
    self.nt_time_delete_1.create_control()
    self.nt_time_delete_2.create_control()
    self.nt_time_inv_added_1.create_control()
    self.nt_time_inv_added_2.create_control()
    self.nt_time_inv_updated_1.create_control()
    self.nt_time_inv_updated_2.create_control()
    self.nt_time_inv_view_1.create_control()
    self.nt_time_inv_view_2.create_control()
    self.nt_time_inv_delete_1.create_control()
    self.nt_time_inv_delete_2.create_control()
    self.nt_time_pay_made_1.create_control()
    self.nt_time_pay_made_2.create_control()
    self.nt_time_pay_refunded_1.create_control()
    self.nt_time_pay_refunded_2.create_control()
    self.nt_time_share_1.create_control()
    self.nt_time_share_2.create_control()
    self.nt_time_reminder_1.create_control()
    self.nt_time_reminder_2.create_control()
    self.nt_time_1.on_change = self.on_nt_time_change_all_1
    self.nt_time_2.on_change = self.on_nt_time_change_all_2
    self.nt_time_new_1.on_change = self.on_nt_time_change_1
    self.nt_time_new_2.on_change = self.on_nt_time_change_2
    self.nt_time_update_1.on_change = self.on_nt_time_change_1
    self.nt_time_update_2.on_change = self.on_nt_time_change_2
    self.nt_time_delete_1.on_change = self.on_nt_time_change_1
    self.nt_time_delete_2.on_change = self.on_nt_time_change_2
    self.nt_time_inv_added_1.on_change = self.on_nt_time_change_1
    self.nt_time_inv_added_2.on_change = self.on_nt_time_change_2
    self.nt_time_inv_updated_1.on_change = self.on_nt_time_change_1
    self.nt_time_inv_updated_2.on_change = self.on_nt_time_change_2
    self.nt_time_inv_view_1.on_change = self.on_nt_time_change_1
    self.nt_time_inv_view_2.on_change = self.on_nt_time_change_2
    self.nt_time_inv_delete_1.on_change = self.on_nt_time_change_1
    self.nt_time_inv_delete_2.on_change = self.on_nt_time_change_2
    self.nt_time_pay_made_1.on_change = self.on_nt_time_change_1
    self.nt_time_pay_made_2.on_change = self.on_nt_time_change_2
    self.nt_time_pay_refunded_1.on_change = self.on_nt_time_change_1
    self.nt_time_pay_refunded_2.on_change = self.on_nt_time_change_2
    self.nt_time_share_1.on_change = self.on_nt_time_change_1
    self.nt_time_share_2.on_change = self.on_nt_time_change_2
    self.nt_time_reminder_1.on_change = self.on_nt_time_change_1
    self.nt_time_reminder_2.on_change = self.on_nt_time_change_2

  def nt_time_set_attribute(self):
    self.nt_time_1.control.indeterminate = True
    self.nt_time_2.value = True
    self.nt_time_new_2.value = True
    self.nt_time_update_2.value = True
    self.nt_time_delete_2.value = True
    self.nt_time_inv_added_2.value = True
    self.nt_time_inv_updated_2.value = True
    self.nt_time_inv_view_2.value = True
    self.nt_time_inv_delete_2.value = True
    self.nt_time_pay_made_1.value = True
    self.nt_time_pay_made_2.value = True
    self.nt_time_pay_refunded_1.value = True
    self.nt_time_pay_refunded_2.value = True
    self.nt_time_share_2.value = True
    self.nt_time_reminder_2.value = True

  def nt_time_appendTo(self):
    self.nt_time_1.control.appendTo(jQuery(f"#{self.nt_time_1.el_id}")[0])
    self.nt_time_2.control.appendTo(jQuery(f"#{self.nt_time_2.el_id}")[0])
    self.nt_time_new_1.control.appendTo(jQuery(f"#{self.nt_time_new_1.el_id}")[0])
    self.nt_time_new_2.control.appendTo(jQuery(f"#{self.nt_time_new_2.el_id}")[0])
    self.nt_time_update_1.control.appendTo(jQuery(f"#{self.nt_time_update_1.el_id}")[0])
    self.nt_time_update_2.control.appendTo(jQuery(f"#{self.nt_time_update_2.el_id}")[0])
    self.nt_time_delete_1.control.appendTo(jQuery(f"#{self.nt_time_delete_1.el_id}")[0])
    self.nt_time_delete_2.control.appendTo(jQuery(f"#{self.nt_time_delete_2.el_id}")[0])
    self.nt_time_inv_added_1.control.appendTo(jQuery(f"#{self.nt_time_inv_added_1.el_id}")[0])
    self.nt_time_inv_added_2.control.appendTo(jQuery(f"#{self.nt_time_inv_added_2.el_id}")[0])
    self.nt_time_inv_updated_1.control.appendTo(jQuery(f"#{self.nt_time_inv_updated_1.el_id}")[0])
    self.nt_time_inv_updated_2.control.appendTo(jQuery(f"#{self.nt_time_inv_updated_2.el_id}")[0])
    self.nt_time_inv_view_1.control.appendTo(jQuery(f"#{self.nt_time_inv_view_1.el_id}")[0])
    self.nt_time_inv_view_2.control.appendTo(jQuery(f"#{self.nt_time_inv_view_2.el_id}")[0])
    self.nt_time_inv_delete_1.control.appendTo(jQuery(f"#{self.nt_time_inv_delete_1.el_id}")[0])
    self.nt_time_inv_delete_2.control.appendTo(jQuery(f"#{self.nt_time_inv_delete_2.el_id}")[0])
    self.nt_time_pay_made_1.control.appendTo(jQuery(f"#{self.nt_time_pay_made_1.el_id}")[0])
    self.nt_time_pay_made_2.control.appendTo(jQuery(f"#{self.nt_time_pay_made_2.el_id}")[0])
    self.nt_time_pay_refunded_1.control.appendTo(jQuery(f"#{self.nt_time_pay_refunded_1.el_id}")[0])
    self.nt_time_pay_refunded_2.control.appendTo(jQuery(f"#{self.nt_time_pay_refunded_2.el_id}")[0])
    self.nt_time_share_1.control.appendTo(jQuery(f"#{self.nt_time_share_1.el_id}")[0])
    self.nt_time_share_2.control.appendTo(jQuery(f"#{self.nt_time_share_2.el_id}")[0])
    self.nt_time_reminder_1.control.appendTo(jQuery(f"#{self.nt_time_reminder_1.el_id}")[0])
    self.nt_time_reminder_2.control.appendTo(jQuery(f"#{self.nt_time_reminder_2.el_id}")[0])
  
  def nt_contact_create_control(self):
    self.nt_contact_1.create_control()
    self.nt_contact_2.create_control()
    self.nt_contact_new_1.create_control()
    self.nt_contact_new_2.create_control()
    self.nt_contact_updated_1.create_control()
    self.nt_contact_updated_2.create_control()
    self.nt_contact_archive_1.create_control()
    self.nt_contact_archive_2.create_control()
    self.nt_contact_unarchive_1.create_control()
    self.nt_contact_unarchive_2.create_control()
    self.nt_contact_delete_1.create_control()
    self.nt_contact_delete_2.create_control()
    self.nt_contact_login_1.create_control()
    self.nt_contact_login_2.create_control()
    self.nt_contact_note_1.create_control()
    self.nt_contact_note_2.create_control()
    self.nt_contact_1.on_change = self.on_nt_contact_change_all_1
    self.nt_contact_2.on_change = self.on_nt_contact_change_all_2
    self.nt_contact_new_1.on_change = self.on_nt_contact_change_1
    self.nt_contact_new_2.on_change = self.on_nt_contact_change_2
    self.nt_contact_updated_1.on_change = self.on_nt_contact_change_1
    self.nt_contact_updated_2.on_change = self.on_nt_contact_change_2
    self.nt_contact_archive_1.on_change = self.on_nt_contact_change_1
    self.nt_contact_archive_2.on_change = self.on_nt_contact_change_2
    self.nt_contact_unarchive_1.on_change = self.on_nt_contact_change_1
    self.nt_contact_unarchive_2.on_change = self.on_nt_contact_change_2
    self.nt_contact_delete_1.on_change = self.on_nt_contact_change_1
    self.nt_contact_delete_2.on_change = self.on_nt_contact_change_2
    self.nt_contact_login_1.on_change = self.on_nt_contact_change_1
    self.nt_contact_login_2.on_change = self.on_nt_contact_change_2
    self.nt_contact_note_1.on_change = self.on_nt_contact_change_1
    self.nt_contact_note_2.on_change = self.on_nt_contact_change_2

  def nt_contact_set_attribute(self):
    self.nt_contact_2.value = True
    self.nt_contact_new_2.value = True
    self.nt_contact_updated_2.value = True
    self.nt_contact_archive_2.value = True
    self.nt_contact_unarchive_2.value = True
    self.nt_contact_delete_2.value = True
    self.nt_contact_login_2.value = True
    self.nt_contact_note_2.value = True

  def nt_contact_appendTo(self):
    self.nt_contact_1.control.appendTo(jQuery(f"#{self.nt_contact_1.el_id}")[0])
    self.nt_contact_2.control.appendTo(jQuery(f"#{self.nt_contact_2.el_id}")[0])
    self.nt_contact_new_1.control.appendTo(jQuery(f"#{self.nt_contact_new_1.el_id}")[0])
    self.nt_contact_new_2.control.appendTo(jQuery(f"#{self.nt_contact_new_2.el_id}")[0])
    self.nt_contact_updated_1.control.appendTo(jQuery(f"#{self.nt_contact_updated_1.el_id}")[0])
    self.nt_contact_updated_2.control.appendTo(jQuery(f"#{self.nt_contact_updated_2.el_id}")[0])
    self.nt_contact_archive_1.control.appendTo(jQuery(f"#{self.nt_contact_archive_1.el_id}")[0])
    self.nt_contact_archive_2.control.appendTo(jQuery(f"#{self.nt_contact_archive_2.el_id}")[0])
    self.nt_contact_unarchive_1.control.appendTo(jQuery(f"#{self.nt_contact_unarchive_1.el_id}")[0])
    self.nt_contact_unarchive_2.control.appendTo(jQuery(f"#{self.nt_contact_unarchive_2.el_id}")[0])
    self.nt_contact_delete_1.control.appendTo(jQuery(f"#{self.nt_contact_delete_1.el_id}")[0])
    self.nt_contact_delete_2.control.appendTo(jQuery(f"#{self.nt_contact_delete_2.el_id}")[0])
    self.nt_contact_login_1.control.appendTo(jQuery(f"#{self.nt_contact_login_1.el_id}")[0])
    self.nt_contact_login_2.control.appendTo(jQuery(f"#{self.nt_contact_login_2.el_id}")[0])
    self.nt_contact_note_1.control.appendTo(jQuery(f"#{self.nt_contact_note_1.el_id}")[0])
    self.nt_contact_note_2.control.appendTo(jQuery(f"#{self.nt_contact_note_2.el_id}")[0])
  
  def nt_firm_create_control(self):
    self.nt_firm_1.create_control()
    self.nt_firm_2.create_control()
    self.nt_firm_new_1.create_control()
    self.nt_firm_new_2.create_control()
    self.nt_firm_updated_1.create_control()
    self.nt_firm_updated_2.create_control()
    self.nt_firm_activate_1.create_control()
    self.nt_firm_activate_2.create_control()
    self.nt_firm_permission_1.create_control()
    self.nt_firm_permission_2.create_control()
    self.nt_firm_item_1.create_control()
    self.nt_firm_item_2.create_control()
    self.nt_firm_info_1.create_control()
    self.nt_firm_info_2.create_control()
    self.nt_firm_1.on_change = self.on_nt_firm_change_all_1
    self.nt_firm_2.on_change = self.on_nt_firm_change_all_2
    self.nt_firm_new_1.on_change = self.on_nt_firm_change_1
    self.nt_firm_new_2.on_change = self.on_nt_firm_change_2
    self.nt_firm_updated_1.on_change = self.on_nt_firm_change_1
    self.nt_firm_updated_2.on_change = self.on_nt_firm_change_2
    self.nt_firm_activate_1.on_change = self.on_nt_firm_change_1
    self.nt_firm_activate_2.on_change = self.on_nt_firm_change_2
    self.nt_firm_permission_1.on_change = self.on_nt_firm_change_1
    self.nt_firm_permission_2.on_change = self.on_nt_firm_change_2
    self.nt_firm_item_1.on_change = self.on_nt_firm_change_1
    self.nt_firm_item_2.on_change = self.on_nt_firm_change_2
    self.nt_firm_info_1.on_change = self.on_nt_firm_change_1
    self.nt_firm_info_2.on_change = self.on_nt_firm_change_2

  def nt_firm_appendTo(self):
    self.nt_firm_1.control.appendTo(jQuery(f"#{self.nt_firm_1.el_id}")[0])
    self.nt_firm_2.control.appendTo(jQuery(f"#{self.nt_firm_2.el_id}")[0])
    self.nt_firm_new_1.control.appendTo(jQuery(f"#{self.nt_firm_new_1.el_id}")[0])
    self.nt_firm_new_2.control.appendTo(jQuery(f"#{self.nt_firm_new_2.el_id}")[0])
    self.nt_firm_updated_1.control.appendTo(jQuery(f"#{self.nt_firm_updated_1.el_id}")[0])
    self.nt_firm_updated_2.control.appendTo(jQuery(f"#{self.nt_firm_updated_2.el_id}")[0])
    self.nt_firm_activate_1.control.appendTo(jQuery(f"#{self.nt_firm_activate_1.el_id}")[0])
    self.nt_firm_activate_2.control.appendTo(jQuery(f"#{self.nt_firm_activate_2.el_id}")[0])
    self.nt_firm_permission_1.control.appendTo(jQuery(f"#{self.nt_firm_permission_1.el_id}")[0])
    self.nt_firm_permission_2.control.appendTo(jQuery(f"#{self.nt_firm_permission_2.el_id}")[0])
    self.nt_firm_item_1.control.appendTo(jQuery(f"#{self.nt_firm_item_1.el_id}")[0])
    self.nt_firm_item_2.control.appendTo(jQuery(f"#{self.nt_firm_item_2.el_id}")[0])
    self.nt_firm_info_1.control.appendTo(jQuery(f"#{self.nt_firm_info_1.el_id}")[0])
    self.nt_firm_info_2.control.appendTo(jQuery(f"#{self.nt_firm_info_2.el_id}")[0])
  
  def nt_firm_set_attribute(self):
    self.nt_firm_1.value = True
    self.nt_firm_2.value = True
    self.nt_firm_new_1.value = True
    self.nt_firm_new_2.value = True
    self.nt_firm_updated_1.value = True
    self.nt_firm_updated_2.value = True
    self.nt_firm_activate_1.value = True
    self.nt_firm_activate_2.value = True
    self.nt_firm_permission_1.value = True
    self.nt_firm_permission_2.value = True
    self.nt_firm_item_1.value = True
    self.nt_firm_item_2.value = True
    self.nt_firm_info_1.value = True
    self.nt_firm_info_2.value = True
  
  def init_user_profile_tab(self):
    self.user_first_name.create_control()
    self.user_last_name.create_control()
    self.user_birthday.create_control()
    self.user_gender.create_control()
    self.user_race.create_control()
    self.user_username.create_control()
    self.user_password.create_control()
    self.user_work_email.create_control()
    self.user_work_phone.create_control()
    self.user_staff_group.create_control()
    self.user_work_extension.create_control()
    self.user_emergency_address.create_control()
    self.user_profile_set_attribute()
    self.user_first_name.control.appendTo(jQuery(f"#{self.user_first_name.el_id}")[0])
    self.user_last_name.control.appendTo(jQuery(f"#{self.user_last_name.el_id}")[0])
    self.user_birthday.control.appendTo(jQuery(f"#{self.user_birthday.el_id}")[0])
    self.user_gender.control.appendTo(jQuery(f"#{self.user_gender.el_id}")[0])
    self.user_race.control.appendTo(jQuery(f"#{self.user_race.el_id}")[0])
    self.user_username.control.appendTo(jQuery(f"#{self.user_username.el_id}")[0])
    self.user_password.control.appendTo(jQuery(f"#{self.user_password.el_id}")[0])
    self.user_work_email.control.appendTo(jQuery(f"#{self.user_work_email.el_id}")[0])
    self.user_work_phone.control.appendTo(jQuery(f"#{self.user_work_phone.el_id}")[0])
    self.user_staff_group.control.appendTo(jQuery(f"#{self.user_staff_group.el_id}")[0])
    self.user_work_extension.control.appendTo(jQuery(f"#{self.user_work_extension.el_id}")[0])
    self.user_emergency_address.control.appendTo(jQuery(f"#{self.user_emergency_address.el_id}")[0])
    
    

  def user_profile_set_attribute(self):
    logged_user = User.get(AppEnv.logged_user.get('user_uid'))
    logged_staff = Staff.search(user=logged_user)
    item_uid = None
    for staff in logged_staff:
      item_uid = staff['uid']
    item = Staff.get(item_uid)
      
    self.user_first_name.enabled = False
    self.user_first_name.value = item['first_name']
    self.user_last_name.value = item['last_name']
    self.user_birthday.value = item['date_of_birth']
    self.user_gender.value = item['personal_gender']
    self.user_race.value = item['personal_race']

    self.user_username.value = item['user_name']
    self.user_username.enabled = False
    self.user_password.value = 'change..'
    self.user_work_email.value = item['work_email']
    self.user_work_email.enabled = False
    self.user_work_phone.value = item['work_phone']
    self.user_work_phone.enabled = False
    self.user_staff_group.value = item['staff_group'].name
    self.user_staff_group.enabled = False
    self.user_work_extension.value = item['extension']
    self.user_work_extension.enabled = False
    self.user_emergency_address.value = item['personal_address']
    
  
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

  def on_nt_case_change_1(self, args):
    print('checkbox 1 is clicked')
    count = 0
    count += self.nt_case_new_1.value
    count += self.nt_case_update_1.value
    count += self.nt_case_close_1.value
    count += self.nt_case_reopen_1.value
    count += self.nt_case_delete_1.value
    count += self.nt_case_note_1.value
    count += self.nt_case_you_1.value
    count += self.nt_case_company_1.value
    count += self.nt_case_user_1.value
    if count == 9:
      self.nt_case_1.value = True
      self.nt_case_1.control.indeterminate = False
    elif count == 0:
      self.nt_case_1.value = False
      self.nt_case_1.control.indeterminate = False
    else:
      self.nt_case_1.value = False
      self.nt_case_1.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_case_change_2(self, args):
    print('checkbox 2 is clicked')
    count = 0
    count += self.nt_case_new_2.value
    count += self.nt_case_update_2.value
    count += self.nt_case_close_2.value
    count += self.nt_case_reopen_2.value
    count += self.nt_case_delete_2.value
    count += self.nt_case_note_2.value
    count += self.nt_case_you_2.value
    count += self.nt_case_company_2.value
    count += self.nt_case_user_2.value
    if count == 9:
      self.nt_case_2.value = True
      self.nt_case_2.control.indeterminate = False
    elif count == 0:
      self.nt_case_2.value = False
      self.nt_case_2.control.indeterminate = False
    else:
      self.nt_case_2.value = False
      self.nt_case_2.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_case_change_all_1(self, args):
    print('checkbox 1 is clicked all')
    if self.nt_case_1.value:
      self.nt_case_new_1.value = True
      self.nt_case_update_1.value = True
      self.nt_case_close_1.value = True
      self.nt_case_reopen_1.value = True
      self.nt_case_delete_1.value = True
      self.nt_case_note_1.value = True
      self.nt_case_you_1.value = True
      self.nt_case_company_1.value = True
      self.nt_case_user_1.value = True
    else:
      self.nt_case_new_1.value = False
      self.nt_case_update_1.value = False
      self.nt_case_close_1.value = False
      self.nt_case_reopen_1.value = False
      self.nt_case_delete_1.value = False
      self.nt_case_note_1.value = False
      self.nt_case_you_1.value = False
      self.nt_case_company_1.value = False
      self.nt_case_user_1.value = False
    self.save_checkbox_status()
      
  def on_nt_case_change_all_2(self, args):
    print('checkbox 2 is clicked all')
    if self.nt_case_2.value:
      self.nt_case_new_2.value = True
      self.nt_case_update_2.value = True
      self.nt_case_close_2.value = True
      self.nt_case_reopen_2.value = True
      self.nt_case_delete_2.value = True
      self.nt_case_note_2.value = True
      self.nt_case_you_2.value = True
      self.nt_case_company_2.value = True
      self.nt_case_user_2.value = True
    else:
      self.nt_case_new_2.value = False
      self.nt_case_update_2.value = False
      self.nt_case_close_2.value = False
      self.nt_case_reopen_2.value = False
      self.nt_case_delete_2.value = False
      self.nt_case_note_2.value = False
      self.nt_case_you_2.value = False
      self.nt_case_company_2.value = False
      self.nt_case_user_2.value = False
    self.save_checkbox_status()

  def on_nt_calendar_change_1(self, args):
    print('on nt calender change 1')
    count = 0
    count += self.nt_calendar_new_1.value
    count += self.nt_calendar_update_1.value
    count += self.nt_calendar_delete_1.value
    count += self.nt_calendar_view_1.value
    if count == 4:
      self.nt_calendar_1.value = True
      self.nt_calendar_1.control.indeterminate = False
    else:
      self.nt_calendar_1.value = False
      self.nt_calendar_1.control.indeterminate = True
    self.save_checkbox_status()

  def on_nt_calendar_change_2(self, args):
    print('on nt calender change 2')
    count = 0
    count += self.nt_calendar_new_2.value
    count += self.nt_calendar_update_2.value
    count += self.nt_calendar_delete_2.value
    count += self.nt_calendar_comment_2.value
    count += self.nt_calendar_view_2.value
    if count == 5:
      self.nt_calendar_2.value = True
      self.nt_calendar_2.control.indeterminate = False
    elif count == 0:
      self.nt_calendar_2.value = False
      self.nt_calendar_2.control.indeterminate = False
    else:
      self.nt_calendar_2.value = False
      self.nt_calendar_2.control.indeterminate = True
    self.save_checkbox_status()
    
  def on_nt_calendar_change_3(self, args):
    print('on_nt_calendar_change_3')
    if self.nt_calendar_new_3.value:
      self.nt_calendar_3.value = True
      self.nt_calendar_3.control.indeterminate = False
    else:
      self.nt_calendar_3.value = False
      self.nt_calendar_3.control.indeterminate = True
    self.save_checkbox_status()
    
  def on_nt_calendar_change_all_1(self, args):
    print('on_nt_calendar_change_all_1')
    self.save_checkbox_status()
    
  def on_nt_calendar_change_all_2(self, args):
    print('on_nt_calendar_change_all_2')
    if self.nt_calendar_2.value:
      self.nt_calendar_new_2.value = True
      self.nt_calendar_update_2.value = True
      self.nt_calendar_delete_2.value = True
      self.nt_calendar_comment_2.value = True
      self.nt_calendar_view_2.value = True
    else:
      self.nt_calendar_new_2.value = False
      self.nt_calendar_update_2.value = False
      self.nt_calendar_delete_2.value = False
      self.nt_calendar_comment_2.value = False
      self.nt_calendar_view_2.value = False
    self.save_checkbox_status()

  def on_nt_calendar_change_all_3(self, args):
    print('on_nt_calendar_change_all_3')
    self.save_checkbox_status()

  def on_nt_document_change_1(self, args):
    print('on_nt_document_change_1')
    count = 0
    count += self.nt_document_new_1.value
    count += self.nt_document_update_1.value
    count += self.nt_document_delete_1.value
    # count += self.nt_document_comment_1.value
    count += self.nt_document_view_1.value
    if count == 4:
      self.nt_document_1.value = True
      self.nt_document_1.control.indeterminate = False
    else:
      self.nt_document_1.value = False
      self.nt_document_1.control.indeterminate = True
    self.save_checkbox_status()
      
  
  def on_nt_document_change_2(self, args):
    print('on_nt_document_change_2')
    count = 0
    count += self.nt_document_new_2.value
    count += self.nt_document_update_2.value
    count += self.nt_document_delete_2.value
    count += self.nt_document_comment_2.value
    count += self.nt_document_view_2.value
    if count == 5:
      self.nt_document_2.value = True
      self.nt_document_2.control.indeterminate = False
    elif count == 0:
      self.nt_document_2.value = False
      self.nt_document_2.control.indeterminate = False
    else:
      self.nt_document_2.value = False
      self.nt_document_2.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_document_change_3(self, args):
    print('on_nt_document_change_3')
    if self.nt_document_new_3.value:
      self.nt_document_3.value = True
      self.nt_document_3.control.indeterminate = False
    else:
      self.nt_document_3.value = False
      self.nt_document_3.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_document_change_all_1(self, args):
    print('on_nt_document_change_all_1')
    self.save_checkbox_status()
  
  def on_nt_document_change_all_2(self, args):
    print('on_nt_document_change_all_2')
    if self.nt_document_2.value == True:
      self.nt_document_new_2.value = True
      self.nt_document_update_2.value = True
      self.nt_document_delete_2.value = True
      self.nt_document_comment_2.value = True
      self.nt_document_view_2.value = True
    else:
      self.nt_document_new_2.value = False
      self.nt_document_update_2.value = False
      self.nt_document_delete_2.value = False
      self.nt_document_comment_2.value = False
      self.nt_document_view_2.value = False
    self.save_checkbox_status()
  
  def on_nt_document_change_all_3(self, args):
    print('on_nt_document_change_all_3')
    self.save_checkbox_status()
  
  def on_nt_task_change_1(self, args):
    print('on_nt_task_change_1')
    count = 0
    count += self.nt_task_new_1.value
    count += self.nt_task_update_1.value
    count += self.nt_task_delete_1.value
    count += self.nt_task_complete_1.value
    count += self.nt_task_incomplete_1.value
    if count == 5:
      self.nt_task_1.value = True
      self.nt_task_1.control.indeterminate = False
    elif count == 0:
      self.nt_task_1.value = False
      self.nt_task_1.control.indeterminate = False
    else:
      self.nt_task_1.value = False
      self.nt_task_1.control.indeterminate = True
    self.save_checkbox_status()

  def on_nt_task_change_2(self, args):
    print('on_nt_task_change_2')
    count = 0
    count += self.nt_task_new_2.value
    count += self.nt_task_update_2.value
    count += self.nt_task_delete_2.value
    count += self.nt_task_complete_2.value
    count += self.nt_task_incomplete_2.value
    if count == 5:
      self.nt_task_2.value = True
      self.nt_task_2.control.indeterminate = False
    elif count == 0:
      self.nt_task_2.value = False
      self.nt_task_2.control.indeterminate = False
    else:
      self.nt_task_2.value = False
      self.nt_task_2.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_task_change_3(self, args):
    print('on_nt_task_change_3')
    count = 0
    count += self.nt_task_new_3.value
    count += self.nt_task_update_3.value
    if count == 2:
      self.nt_task_3.value = True
      self.nt_task_3.control.indeterminate = False
    elif count == 0:
      self.nt_task_3.value = False
      self.nt_task_3.control.indeterminate = False
    else:
      self.nt_task_3.value = False
      self.nt_task_3.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_task_change_all_1(self, args):
    print('on_nt_task_change_all_1')
    if self.nt_task_1.value:
      self.nt_task_new_1.value = True
      self.nt_task_update_1.value = True
      self.nt_task_delete_1.value = True
      self.nt_task_complete_1.value = True
      self.nt_task_incomplete_1.value = True
    else:
      self.nt_task_new_1.value = False
      self.nt_task_update_1.value = False
      self.nt_task_delete_1.value = False
      self.nt_task_complete_1.value = False
      self.nt_task_incomplete_1.value = False
    self.save_checkbox_status()

  def on_nt_task_change_all_2(self, args):
    print('on_nt_task_change_all_2')
    if self.nt_task_2.value:
      self.nt_task_new_2.value = True
      self.nt_task_update_2.value = True
      self.nt_task_delete_2.value = True
      self.nt_task_complete_2.value = True
      self.nt_task_incomplete_2.value = True
    else:
      self.nt_task_new_2.value = False
      self.nt_task_update_2.value = False
      self.nt_task_delete_2.value = False
      self.nt_task_complete_2.value = False
      self.nt_task_incomplete_2.value = False
    self.save_checkbox_status()
  
  def on_nt_task_change_all_3(self, args):
    print('on_nt_task_change_all_3')
    if self.nt_task_3.value:
      self.nt_task_new_3.value = True
      self.nt_task_update_3.value = True
    else:
      self.nt_task_new_3.value = False
      self.nt_task_update_3.value = False
    self.save_checkbox_status()
  
  def on_nt_time_change_1(self, args):
    print('on_nt_time_change_1')
    count = 0
    count += self.nt_time_new_1.value
    count += self.nt_time_update_1.value
    count += self.nt_time_delete_1.value
    count += self.nt_time_inv_added_1.value
    count += self.nt_time_inv_updated_1.value
    count += self.nt_time_inv_view_1.value
    count += self.nt_time_inv_delete_1.value
    count += self.nt_time_pay_made_1.value
    count += self.nt_time_pay_refunded_1.value
    count += self.nt_time_share_1.value
    count += self.nt_time_reminder_1.value
    if count == 11:
      self.nt_time_1.value = True
      self.nt_time_1.control.indeterminate = False
    elif count == 0:
      self.nt_time_1.value = False
      self.nt_time_1.control.indeterminate = False
    else:
      self.nt_time_1.value = False
      self.nt_time_1.control.indeterminate = True
    self.save_checkbox_status()
      
  
  def on_nt_time_change_2(self, args):
    print('on_nt_time_change_2')
    count = 0
    count += self.nt_time_new_2.value
    count += self.nt_time_update_2.value
    count += self.nt_time_delete_2.value
    count += self.nt_time_inv_added_2.value
    count += self.nt_time_inv_updated_2.value
    count += self.nt_time_inv_view_2.value
    count += self.nt_time_inv_delete_2.value
    count += self.nt_time_pay_made_2.value
    count += self.nt_time_pay_refunded_2.value
    count += self.nt_time_share_2.value
    count += self.nt_time_reminder_2.value
    if count == 11:
      self.nt_time_2.value = True
      self.nt_time_2.control.indeterminate = False
    elif count == 0:
      self.nt_time_2.value = False
      self.nt_time_2.control.indeterminate = False
    else:
      self.nt_time_2.value = False
      self.nt_time_2.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_time_change_all_1(self, args):
    print('on_nt_time_change_all_1')
    if self.nt_time_1.value:
      self.nt_time_new_1.value = True
      self.nt_time_update_1.value = True
      self.nt_time_delete_1.value = True
      self.nt_time_inv_added_1.value = True
      self.nt_time_inv_updated_1.value = True
      self.nt_time_inv_view_1.value = True
      self.nt_time_inv_delete_1.value = True
      self.nt_time_pay_made_1.value = True
      self.nt_time_pay_refunded_1.value = True
      self.nt_time_share_1.value = True
      self.nt_time_reminder_1.value = True
    else:
      self.nt_time_new_1.value = False
      self.nt_time_update_1.value = False
      self.nt_time_delete_1.value = False
      self.nt_time_inv_added_1.value = False
      self.nt_time_inv_updated_1.value = False
      self.nt_time_inv_view_1.value = False
      self.nt_time_inv_delete_1.value = False
      self.nt_time_pay_made_1.value = False
      self.nt_time_pay_refunded_1.value = False
      self.nt_time_share_1.value = False
      self.nt_time_reminder_1.value = False
    self.save_checkbox_status()
  
  def on_nt_time_change_all_2(self, args):
    print('on_nt_time_change_all_2')
    if self.nt_time_2.value:
      self.nt_time_new_2.value = True
      self.nt_time_update_2.value = True
      self.nt_time_delete_2.value = True
      self.nt_time_inv_added_2.value = True
      self.nt_time_inv_updated_2.value = True
      self.nt_time_inv_view_2.value = True
      self.nt_time_inv_delete_2.value = True
      self.nt_time_pay_made_2.value = True
      self.nt_time_pay_refunded_2.value = True
      self.nt_time_share_2.value = True
      self.nt_time_reminder_2.value = True
    else:
      self.nt_time_new_2.value = False
      self.nt_time_update_2.value = False
      self.nt_time_delete_2.value = False
      self.nt_time_inv_added_2.value = False
      self.nt_time_inv_updated_2.value = False
      self.nt_time_inv_view_2.value = False
      self.nt_time_inv_delete_2.value = False
      self.nt_time_pay_made_2.value = False
      self.nt_time_pay_refunded_2.value = False
      self.nt_time_share_2.value = False
      self.nt_time_reminder_2.value = False
    self.save_checkbox_status()
  
  def on_nt_contact_change_1(self, args):
    print('on_nt_contact_change_1')
    count = 0
    count += self.nt_contact_new_1.value
    count += self.nt_contact_updated_1.value
    count += self.nt_contact_archive_1.value
    count += self.nt_contact_unarchive_1.value
    count += self.nt_contact_delete_1.value
    count += self.nt_contact_login_1.value
    count += self.nt_contact_note_1.value
    if count == 7:
      self.nt_contact_1.value = True
      self.nt_contact_1.control.indeterminate = False
    elif count == 0:
      self.nt_contact_1.value = False
      self.nt_contact_1.control.indeterminate = False
    else:
      self.nt_contact_1.value = False
      self.nt_contact_1.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_contact_change_2(self, args):
    print('on_nt_contact_change_2')
    count = 0
    count += self.nt_contact_new_2.value
    count += self.nt_contact_updated_2.value
    count += self.nt_contact_archive_2.value
    count += self.nt_contact_unarchive_2.value
    count += self.nt_contact_delete_2.value
    count += self.nt_contact_login_2.value
    count += self.nt_contact_note_2.value
    if count == 7:
      self.nt_contact_2.value = True
      self.nt_contact_2.control.indeterminate = False
    elif count == 0:
      self.nt_contact_2.value = False
      self.nt_contact_2.control.indeterminate = False
    else:
      self.nt_contact_2.value = False
      self.nt_contact_2.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_contact_change_all_1(self, args):
    print('on_nt_contact_change_all_1')
    if self.nt_contact_1.value:
      self.nt_contact_new_1.value = True
      self.nt_contact_updated_1.value = True
      self.nt_contact_archive_1.value = True
      self.nt_contact_unarchive_1.value = True
      self.nt_contact_delete_1.value = True
      self.nt_contact_login_1.value = True
      self.nt_contact_note_1.value = True
    else:
      self.nt_contact_new_1.value = False
      self.nt_contact_updated_1.value = False
      self.nt_contact_archive_1.value = False
      self.nt_contact_unarchive_1.value = False
      self.nt_contact_delete_1.value = False
      self.nt_contact_login_1.value = False
      self.nt_contact_note_1.value = False
    self.save_checkbox_status()
  
  def on_nt_contact_change_all_2(self, args):
    print('on_nt_contact_change_all_2')
    if self.nt_contact_2.value:
      self.nt_contact_new_2.value = True
      self.nt_contact_updated_2.value = True
      self.nt_contact_archive_2.value = True
      self.nt_contact_unarchive_2.value = True
      self.nt_contact_delete_2.value = True
      self.nt_contact_login_2.value = True
      self.nt_contact_note_2.value = True
    else:
      self.nt_contact_new_2.value = False
      self.nt_contact_updated_2.value = False
      self.nt_contact_archive_2.value = False
      self.nt_contact_unarchive_2.value = False
      self.nt_contact_delete_2.value = False
      self.nt_contact_login_2.value = False
      self.nt_contact_note_2.value = False
    self.save_checkbox_status()
  
  def on_nt_firm_change_1(self, args):
    print('on_nt_firm_change_1')
    count = 0
    count += self.nt_firm_new_1.value
    count += self.nt_firm_updated_1.value
    count += self.nt_firm_activate_1.value
    count += self.nt_firm_permission_1.value
    count += self.nt_firm_item_1.value
    count += self.nt_firm_info_1.value
    if count == 6:
      self.nt_firm_1.value = True
      self.nt_firm_1.control.indeterminate = False
    elif count == 0:
      self.nt_firm_1.value = False
      self.nt_firm_1.control.indeterminate = False
    else:
      self.nt_firm_1.value = False
      self.nt_firm_1.control.indeterminate = True
    self.save_checkbox_status()

  def on_nt_firm_change_2(self, args):
    print('on_nt_firm_change_2')
    count = 0
    count += self.nt_firm_new_2.value
    count += self.nt_firm_updated_2.value
    count += self.nt_firm_activate_2.value
    count += self.nt_firm_permission_2.value
    count += self.nt_firm_item_2.value
    count += self.nt_firm_info_2.value
    if count == 6:
      self.nt_firm_2.value = True
      self.nt_firm_2.control.indeterminate = False
    elif count == 0:
      self.nt_firm_2.value = False
      self.nt_firm_2.control.indeterminate = False
    else:
      self.nt_firm_2.value = False
      self.nt_firm_2.control.indeterminate = True
    self.save_checkbox_status()
  
  def on_nt_firm_change_all_1(self, args):
    print('on_nt_firm_change_all_1')
    if self.nt_firm_1.value:
      self.nt_firm_new_1.value = True
      self.nt_firm_updated_1.value = True
      self.nt_firm_activate_1.value = True
      self.nt_firm_permission_1.value = True
      self.nt_firm_item_1.value = True
      self.nt_firm_info_1.value = True
    else:
      self.nt_firm_new_1.value = False
      self.nt_firm_updated_1.value = False
      self.nt_firm_activate_1.value = False
      self.nt_firm_permission_1.value = False
      self.nt_firm_item_1.value = False
      self.nt_firm_info_1.value = False
    self.save_checkbox_status()
  
  def on_nt_firm_change_all_2(self, args):
    print('on_nt_firm_change_all_2')
    if self.nt_firm_2.value:
      self.nt_firm_new_2.value = True
      self.nt_firm_updated_2.value = True
      self.nt_firm_activate_2.value = True
      self.nt_firm_permission_2.value = True
      self.nt_firm_item_2.value = True
      self.nt_firm_info_2.value = True
    else:
      self.nt_firm_new_2.value = False
      self.nt_firm_updated_2.value = False
      self.nt_firm_activate_2.value = False
      self.nt_firm_permission_2.value = False
      self.nt_firm_item_2.value = False
      self.nt_firm_info_2.value = False
    self.save_checkbox_status()

  def save_checkbox_status(self):
    pass

  def display_user_profile_info(self):
    print('1')
    print(AppEnv.logged_user.email)
  
  def destroy(self):
    # self.date_picker.destroy()
    # self.radio_plus.destroy()
    # self.radio_minus.destroy()
    # self.radio_calendar.destroy()
    # self.radio_business.destroy()
    # self.numbers.destroy()
    if self.container_el:
      self.container_el.innerHTML = ''