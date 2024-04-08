import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *


def bizday_calc_func(start_date, num_days):
  my_start_date = start_date
  my_num_days = abs(num_days)
  inc = 1 if num_days > 0 else -1
  while my_num_days > 0:
    my_start_date += timedelta(days=inc)
    weekday = my_start_date.weekday()
    if weekday >= 5:
      continue
    my_num_days -= 1
  return my_start_date

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

    # self.date_picker.addEventListener('change', self.change_date)
    # self.radio_plus.addEventListener('change', self.change_plus_minus)
    # self.radio_minus.addEventListener('change', self.change_plus_minus)
    # self.radio_calendar.addEventListener('change', self.change_day_mode)
    # self.radio_business.addEventListener('change', self.change_day_mode)
    # self.numbers.addEventListener('input', self.change_number_days)
    
  def form_show(self):
    self.container_el.innerHTML = f'\
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
      \
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
      <h4 class ="col-xs-12" >Admin settings</h4>\
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
      <h4 class ="col-xs-12">Tenant Billing Settings</h4>\
      <div class ="col-xs-12" style="margin-bottom: 15px; justify-content: center;">\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.billing_credit_card_id}" style="white-space: nowrap; margin-right:10px;">Business Name</label>\
          <input id="{self.billing_credit_card_id}"/>\
        </div>\
        <div class="col-xs-6" style="align-items: center; ">\
          <label for="{self.billing_address_id}" style="white-space: nowrap; margin-right:10px;">Business Address</label>\
          <input id="{self.billing_address_id}"/>\
        </div>\
      </div>'
    
    self.in_app_notify.appendTo(jQuery(f"#{self.in_app_notify_id}")[0])
    self.email_notify.appendTo(jQuery(f"#{self.email_notify_id}")[0])
    self.user_name.appendTo(jQuery(f"#{self.user_name_id}")[0])
    self.user_address.appendTo(jQuery(f"#{self.user_address_id}")[0])
    self.user_email.appendTo(jQuery(f"#{self.user_email_id}")[0])
    self.user_phone.appendTo(jQuery(f"#{self.user_phone_id}")[0])
    self.user_birthday.appendTo(jQuery(f"#{self.user_birthday_id}")[0])
    self.user_gender.appendTo(jQuery(f"#{self.user_gender_id}")[0])
    self.business_name.appendTo(jQuery(f"#{self.business_name_id}")[0])
    self.business_address.appendTo(jQuery(f"#{self.business_address_id}")[0])
    self.business_phone.appendTo(jQuery(f"#{self.business_phone_id}")[0])
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

  def change_date(self, args):
    self.update_date()

  def change_plus_minus(self, args):
    self.update_date()
  
  def change_day_mode(self, args):
    self.update_date()
  
  def change_number_days(self, args):
    self.number_days = int(args['value'] if args['value'] else '0')
    self.update_date()
  
  def update_date(self):
    date_check_blank = self.date_picker.value is not None
    button_state_addsub = self.radio_plus.checked
    button_state_calcbiz = self.radio_calendar.checked

    output_text = 'Date: '
    if date_check_blank:
      date_origin = datetime_js_to_py(self.date_picker.value)
      date_output = date_origin
      if button_state_addsub and button_state_calcbiz:
        date_output = date_origin + timedelta(days=self.number_days)
      elif button_state_addsub == False and button_state_calcbiz:
        date_output = date_origin - timedelta(days=self.number_days)
      elif button_state_addsub and button_state_calcbiz == False:
        date_output = bizday_calc_func(date_origin, self.number_days)
      elif button_state_addsub == False and button_state_calcbiz == False:
        date_output = bizday_calc_func(date_origin, self.number_days*-1)
      output_text = f'Date: {date_output.strftime("%A, %B %d, %Y")}'
    output_el = jQuery(f"#{self.output_id}")[0]
    output_el.innerHTML = output_text
