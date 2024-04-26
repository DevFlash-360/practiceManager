import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *

from ..app.models import Staff, User, Contact, Activity, AppAuditLog

class CaseActivityFeedView:
  def __init__(self, container_id, **kwargs):
    self.container_id = container_id or AppEnv.content_container_id
    self.container_el = jQuery(f"#{self.container_id}")[0]

    self.activity_dict = []
    all_html = self.prepare_all_html()
    invoices_html = self.prepare_invoices_html()
    events_html = self.prepare_events_html()
    documents_html = self.prepare_documents_html()
    tasks_html = self.prepare_tasks_html()
    times_html = self.prepare_times_html()
    expenses_html = self.prepare_expenses_html()
    contacts_html = self.prepare_contacts_html()
    cases_html = self.prepare_cases_html()
    leads_html = self.prepare_leads_html()
    updates_html = self.prepare_updates_html()
    payments_html = self.prepare_payments_html()
    staffs_html = self.prepare_staffs_html()
    self.invoicesTabInitialized  = False
    self.eventsTabInitialized = False
    self.documentsTabInitialized = False
    self.tasksTabInitialized = False
    self.timesTabInitialized = False
    self.expensesTabInitialized = False
    self.contactsTabInitialized = False
    self.casesTabInitialized = False
    self.leadsTabInitialized = False
    self.updatesTabInitialized = False
    self.paymentsTabInitialized = False
    self.staffsTabInitialized = False

    self.tab = ej.navigations.Tab({
      # 'heightAdjustMode': 'Auto',
      # 'overflowMode': 'Popup',
      'items': [
        {'header': {'text': 'All'}, 'content': all_html},
        {'header': {'text': 'Time Entry'}, 'content': times_html},
        {'header': {'text': 'Event'}, 'content': events_html},
        {'header': {'text': 'Task'}, 'content': tasks_html},
        {'header': {'text': 'Document'}, 'content': documents_html},
        {'header': {'text': 'Expense'}, 'content': expenses_html},
        {'header': {'text': 'Contact'}, 'content': contacts_html},
        {'header': {'text': 'Invoice'}, 'content': invoices_html},
        {'header': {'text': 'Case'}, 'content': cases_html},
        {'header': {'text': 'Lead'}, 'content': leads_html},
        {'header': {'text': 'Update'}, 'content': updates_html},
        {'header': {'text': 'Payment'}, 'content': payments_html},
        {'header': {'text': 'Staff'}, 'content': staffs_html},
      ],
      'selected': self.on_tab_selected
    })
    
  def form_show(self):
    self.container_el.innerHTML = '''
      <h4>Recent Activity</h4>
      <div id="tab-element"></div>
    '''
    self.tab.appendTo(jQuery("#tab-element")[0])
    '''
     - need to place a list view in each tab item.
     - data should be loaded from backend/database to be displayed in the list.
     - implement a filter feature to split the data into several tabs.

     .. looked at the ContactListView and the solution seemed to be tabel. (plan to see the DevFusion GridListView)
     .. looked at the TimeEntryView and found that GridView is even better. (it was from AnvilFusion)
     .. found out that i can't use the GridView in AnvilFusion directly. try find another FormInput or sth (it not, try syncfusion)

     ** prepare_ methods are to create demo html and add to DOM(meanning the tab)
     ** init_ methods are to insert actual html to each demos
     ** filter method is to filter the fetched data by the parameter(all, invoice, event, document, etc.)
     ** create_actual_html method is to create a actual html with the given parameter dictionary value.
    '''
    # self.prepare_all_html()
    self.init_all_tab()

  # how to change the stylesheet of checkbox?
  def prepare_all_html(self):
    ret_html = '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-all-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''
      # item_uid = activity['uid']
      # item = Activity.get(item_uid)
      
    return ret_html

  def prepare_invoices_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-invoices-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_events_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-events-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_documents_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-documents-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_tasks_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-tasks-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''
  
  def prepare_times_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-times-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_expenses_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-expenses-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_contacts_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-contacts-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_cases_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-cases-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_leads_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-leads-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_updates_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-updates-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_payments_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-payments-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_staffs_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-staffs-activity">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''
  
  def on_tab_selected(self, args):
    selected_index = args.selectedIndex
    print('tab selected', selected_index)
    if selected_index == 1 and not self.timesTabInitialized:
      self.init_times_tab()
      self.timesTabInitialized = True
    elif selected_index == 2 and not self.eventsTabInitialized:
      self.init_events_tab()
      self.eventsTabInitialized = True
    elif selected_index == 3 and not self.tasksTabInitialized:
      self.init_tasks_tab()
      self.tasksTabInitialized = True
    elif selected_index == 4 and not self.documentsTabInitialized:
      self.init_documents_tab()
      self.documentsTabInitialized = True
    elif selected_index == 5 and not self.expensesTabInitialized:
      self.init_expenses_tab()
      self.expensesTabInitialized = True
    elif selected_index == 6 and not self.contactsTabInitialized:
      self.init_contacts_tab()
      self.contactsTabInitialized = True
    elif selected_index == 7 and not self.invoicesTabInitialized:
      self.init_invoices_tab()
      self.invoicesTabInitialized = True
    elif selected_index == 8 and not self.casesTabInitialized:
      self.init_cases_tab()
      self.casesTabInitialized = True
    elif selected_index == 9 and not self.leadsTabInitialized:
      self.init_leads_tab()
      self.leadsTabInitialized = True
    elif selected_index == 10 and not self.updatesTabInitialized:
      self.init_updates_tab()
      self.updatesTabInitialized = True
    elif selected_index == 11 and not self.paymentsTabInitialized:
      self.init_payments_tab()
      self.paymentsTabInitialized = True
    elif selected_index == 12 and not self.staffsTabInitialized:
      self.init_staffs_tab()
      self.staffsTabInitialized = True

  def filter_data(self, type1, type2 = '', type3 = '', type4 = ''):
    ret_list = []
    for dict in self.activity_dict:
      if dict['table_name'] == type1 or dict['table_name'] == type2 or dict['table_name'] == type3 or dict['table_name'] == type4:
        ret_list.append(dict)
    return ret_list
  
  def init_all_tab(self):
    all_activity = AppAuditLog.search()
    tot_count = all_activity.count
    all_activity.page_length = 100
    all_activity.page = int(tot_count/100)

    for activity in all_activity:
      self.activity_dict.append(activity)

    if tot_count % 100:
      all_activity.page += 1
      for activity in all_activity:
        self.activity_dict.append(activity)
    self.activity_dict.reverse()
    last50_activities = []
    last50_activities = self.activity_dict[:25]

    for activity in last50_activities:
      
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      ret_html = ''
      rt_sentence = ''
      
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-all-activity").append(ret_html)

        # <div class="col-xs-12">{activity['address']}</div>

  def generate_newdict(self, activity):
    new_dict = {}
    new_dict['time'] = activity['action_time']
    new_dict['type'] = activity['action_type']
    action_by = activity['action_by']
    all_users = User.search(uid = action_by)
    email = ''
    for users in all_users:
      email = users['email']
      break

    all_staff = Staff.search(work_email = email)
    user_name = ''
    for staff in all_staff:
      user_name = staff['first_name'] + ' ' + staff['last_name']
      break
    new_dict['user_name'] = user_name
    new_dict['table_name'] = activity['table_name']
    return new_dict
  
  def generate_sentence(self, dict):
    ret_sentences = ''
    if dict['user_name'] == '':
      if dict['type'] == 'add':
        ret_sentences = dict['user_name'] + ' Added ' + dict['table_name'] + ' at ' + dict['time'].strftime("%m-%d-%Y %I:%M:%S %p")
      if dict['type'] == 'update':
        ret_sentences = dict['user_name'] + ' Updated ' + dict['table_name'] + ' at ' + dict['time'].strftime("%m-%d-%Y %I:%M:%S %p")
      if dict['type'] == 'delete':
        ret_sentences = dict['user_name'] + ' Deleted ' + dict['table_name'] + ' at ' + dict['time'].strftime("%m-%d-%Y %I:%M:%S %p")
    else:
      if dict['type'] == 'add':
        ret_sentences = dict['user_name'] + ' added ' + dict['table_name'] + ' at ' + dict['time'].strftime("%m-%d-%Y %I:%M:%S %p")
      if dict['type'] == 'update':
        ret_sentences = dict['user_name'] + ' updated ' + dict['table_name'] + ' at ' + dict['time'].strftime("%m-%d-%Y %I:%M:%S %p")
      if dict['type'] == 'delete':
        ret_sentences = dict['user_name'] + ' deleted ' + dict['table_name'] + ' at ' + dict['time'].strftime("%m-%d-%Y %I:%M:%S %p")
    return ret_sentences
    

  
  def init_invoices_tab(self):
    invoices_activity = self.filter_data('Invoice')
    last50_activities = []
    last50_activities = invoices_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-invoices-activity").append(ret_html)
    
  def init_events_tab(self):
    events_activity = self.filter_data('Event')
    last50_activities = []
    last50_activities = events_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-events-activity").append(ret_html)

  def init_documents_tab(self):
    documents_activity = self.filter_data('Document')
    last50_activities = []
    last50_activities = documents_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-documents-activity").append(ret_html)

  def init_tasks_tab(self):
    tasks_activity = self.filter_data('Task')
    print(len(tasks_activity))
    last50_activities = []
    last50_activities = tasks_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-tasks-activity").append(ret_html)

  def init_times_tab(self):
    times_activity = self.filter_data('Timesheet', 'TimeOffRequest')
    last50_activities = []
    last50_activities = times_activity[:50]
    for activity in last50_activities:
      rt_sentence = self.generate_sentence(activity)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-times-activity").append(ret_html)
  
  def init_expenses_tab(self):
    expenses_activity = self.filter_data('Expense')
    last50_activities = []
    last50_activities = expenses_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-expenses-activity").append(ret_html)

  def init_contacts_tab(self):
    contacts_activity = self.filter_data('Contact')
    last50_activities = []
    last50_activities = contacts_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-contacts-activity").append(ret_html)

  def init_cases_tab(self):
    cases_activity = self.filter_data('Case', 'CaseWorkflowItem', 'CaseWorkflow')
    last50_activities = []
    last50_activities = cases_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-cases-activity").append(ret_html)

  def init_leads_tab(self):
    leads_activity = self.filter_data('Lead')
    last50_activities = []
    last50_activities = leads_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-leads-activity").append(ret_html)

  def init_updates_tab(self):
    updates_activity = self.filter_data('PerformanceIncentive')
    last50_activities = []
    last50_activities = updates_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-updates-activity").append(ret_html)

  def init_payments_tab(self):
    payments_activity = self.filter_data('Payment', 'Payroll', 'PayrollTotal', 'ReimbursementRequest')
    last50_activities = []
    last50_activities = payments_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-payments-activity").append(ret_html)

  def init_staffs_tab(self):
    staffs_activity = self.filter_data('Staff')
    last50_activities = []
    last50_activities = staffs_activity[:50]
    for activity in last50_activities:
      new_dict = {}
      new_dict = self.generate_newdict(activity)
      rt_sentence = self.generate_sentence(new_dict)
      ret_html = f'''
        <tr class="e-row">
          <td class="e-rowcell" style="text-align: left;">{rt_sentence}</td>
        </tr>
      '''
      jQuery("#id-staffs-activity").append(ret_html)
  
  def destroy(self):
    if self.container_el:
      self.container_el.innerHTML = ''