import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *


class SettingsView:
  def __init__(self, container_id, **kwargs):
    self.container_id = container_id or AppEnv.content_container_id
    self.container_el = jQuery(f"#{self.container_id}")[0]

    self.in_app_notify_id = f"in_app_notify_{uuid.uuid4()}"
    self.email_notify_id = f"email_notify_{uuid.uuid4()}"
    self.user_name_id = f"user_name_{uuid.uuid4()}"
    self.user_address_id = f"user_address_{uuid.uuid4()}"
    self.user_email_id = f"user_email_{uuid.uuid4()}"
    self.user_phone_id = f"user_phone_{uuid.uuid4()}"
    self.user_birthday_id = f"user_birthday_{uuid.uuid4()}"
    self.user_gender_id = f"user_gender_{uuid.uuid4()}"
    self.business_name_id = f"business_name_{uuid.uuid4()}"
    self.business_address_id = f"business_address_{uuid.uuid4()}"
    self.business_phone_id = f"business_phone_{uuid.uuid4()}"
    self.billing_credit_card_id = f"billing_credit_card_{uuid.uuid4()}"
    self.billing_address_id = f"billing_address_{uuid.uuid4()}"
    self.in_app_notify = ej.buttons.CheckBox({
      'label': 'In App Notification',
      'checked': False
    })
    self.email_notify = ej.buttons.CheckBox({
      'label': 'Email Notification',
      'checked': False
    })
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
    self.business_name = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.business_address = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.business_phone = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.billing_credit_card = ej.inputs.TextBox({
      'floatLabelType': 'Auto'
    })
    self.billing_address = ej.inputs.TextBox({
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
      'items': [
        {'header': {'text': 'Notification Settings'}, 'content': notification_settings_html},
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
    
    self.in_app_notify.appendTo(jQuery(f"#{self.in_app_notify_id}")[0])
    self.email_notify.appendTo(jQuery(f"#{self.email_notify_id}")[0])

  def prepare_notification_settings_html(self):
    return f'''
      <div class="notification-settings">
        <h4 class ="col-xs-12" >Notification Settings</h4>\
        <div class ="col-xs-12" style="display:flex; margin-bottom: 15px;">\
          <div class="col-xs-6">\
            <input id="{self.in_app_notify_id}" type="checkbox"/>\
          </div>\
          <div class ="col-xs-6">\
            <input id="{self.email_notify_id}" type="checkbox"/>\
          </div>\
        </div>\
        \
        <h4 class ="col-xs-12" >Case Name syntax settings</h4>\
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
            <label for="{self.user_password.el_id}" style="white-space: nowrap; margin-right:10px;">Password</label>\
            {self.user_password.html}\
          </div>\
        </div>\
      </div>
    '''

  def prepare_admin_settings_html(self):
    return f'''
      <h4 class ="col-xs-12" >Admin settings</h4>\
    '''

  def prepare_business_details_settings_html(self):
    return f'''
      <h4 class ="col-xs-12" >Tenant Settings</h4>\
      <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.business_name_id}" style="white-space: nowrap; margin-right:10px;">Business Name</label>\
          <input id="{self.business_name_id}"/>\
        </div>\
      </div>\
      <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.business_address_id}" style="white-space: nowrap; margin-right:10px;">Business Address</label>\
          <input id="{self.business_address_id}"/>\
        </div>\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.business_phone_id}" style="white-space: nowrap; margin-right:10px;">Business Phone Number</label>\
          <input id="{self.business_phone_id}"/>\
        </div>\
      </div>\
    '''

  def prepare_billing_info_settings_html(self):
    return f'''
      <h4 class ="col-xs-12">Tenant Billing Settings</h4>\
      <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.billing_credit_card_id}" style="white-space: nowrap; margin-right:10px;">Credit Card</label>\
          <input id="{self.billing_credit_card_id}"/>\
        </div>\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.billing_address_id}" style="white-space: nowrap; margin-right:10px;">Billing Address</label>\
          <input id="{self.billing_address_id}"/>\
        </div>\
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

  def init_user_profile_tab(self):
    self.user_name.appendTo(jQuery(f"#{self.user_name_id}")[0])
    self.user_address.appendTo(jQuery(f"#{self.user_address_id}")[0])
    self.user_email.appendTo(jQuery(f"#{self.user_email_id}")[0])
    self.user_phone.appendTo(jQuery(f"#{self.user_phone_id}")[0])
    self.user_birthday.appendTo(jQuery(f"#{self.user_birthday_id}")[0])
    self.user_gender.appendTo(jQuery(f"#{self.user_gender_id}")[0])

  def init_admin_tab(self):
    pass

  def init_business_details_tab(self):
    self.business_name.appendTo(jQuery(f"#{self.business_name_id}")[0])
    self.business_address.appendTo(jQuery(f"#{self.business_address_id}")[0])
    self.business_phone.appendTo(jQuery(f"#{self.business_phone_id}")[0])

  def init_billing_info_tab(self):
    self.billing_credit_card.appendTo(jQuery(f"#{self.billing_credit_card_id}")[0])
    self.billing_address.appendTo(jQuery(f"#{self.billing_address_id}")[0])
  
  def destroy(self):
    self.date_picker.destroy()
    self.radio_plus.destroy()
    self.radio_minus.destroy()
    self.radio_calendar.destroy()
    self.radio_business.destroy()
    self.numbers.destroy()
    if self.container_el:
      self.container_el.innerHTML = ''
