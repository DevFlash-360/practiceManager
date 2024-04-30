import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta, datetime

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *

from ..app.models import Staff, User, Contact, Activity, AppAuditLog, TimeEntry, Expense, Case

PM_AV_PERIOD = [
  'This Month',
  'Last One Month',
  'Last Three Month',
  'This Year',
  'Last One Year',
]

init_time_entry_activity = []
init_expenses = []
init_time_staff = []
init_case_timeentry = []

class AnalyticsView:
  def __init__(self, container_id, **kwargs):
    self.container_id = container_id or AppEnv.content_container_id
    self.container_el = jQuery(f"#{self.container_id}")[0]
    # billing page
    
    billing_html = self.prepare_billing_html()
    case_html = self.prepare_case_html()
    finance_html = self.prepare_finance_html()
    firm_html = self.prepare_firm_html()
    lead_html = self.prepare_lead_html()
    lead_intake_html = self.prepare_lead_intake_html()
    staff_html = self.prepare_staff_html()
    
    self.billingTabInitialized  = False
    self.caseTabInitialized = False
    self.financeTabInitialized = False
    self.firmTabInitialized = False
    self.leadTabInitialized = False
    self.lead_intakeTabInitialized = False
    self.staffTabInitialized = False

    self.tab = ej.navigations.Tab({
      # 'heightAdjustMode': 'Auto',
      # 'overflowMode': 'Popup',
      'items': [
        {'header': {'text': 'Billing'}, 'content': billing_html},
        {'header': {'text': 'Case'}, 'content': case_html},
        {'header': {'text': 'Finance'}, 'content': finance_html},
        {'header': {'text': 'Firm'}, 'content': firm_html},
        {'header': {'text': 'Lead'}, 'content': lead_html},
        {'header': {'text': 'Lead_Intake'}, 'content': lead_intake_html},
        {'header': {'text': 'Staff'}, 'content': staff_html},
      ],
      'selected': self.on_tab_selected
    })
    
  def form_show(self):
    self.container_el.innerHTML = '''
      <h4>Analytics</h4>
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
    self.init_billing_tab()

  # how to change the stylesheet of checkbox?
  def prepare_billing_html(self):
    ret_html = '''
      <div class ="col-xs-7" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center; margin-bottom: 15px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <i class="fa-regular fa-clock-three" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Time Entries this Month</span>
                <div id="id_time_entry" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center; margin-bottom: 15px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-square-dollar" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Case Expenses this Month</span>
                <div id="id_case_expense" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding-right: 7px; margin-bottom: 15px">
          <div class="p-3" style="background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; color: white;">
            <div style="display:flex; align-items:center;">
              <i class="fa-solid fa-ballot-check" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Overdue Invoices</span>
                <div style="font-weight: bold; font-size: 1.6em;">2</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding-left: 7px; margin-bottom: 15px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-ballot-check" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Partial Invoices</span>
                <div style="font-weight: bold; font-size: 1.6em;">6</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem">Time vs Staff this Month</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem">Time Entries vs Activity</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_time_staff"></div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-left: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_time_activity"></div>
        </div>
      </div>
      <div class ="col-xs-5" style="justify-content: center; padding: 0px; background-color: white;">
        <div class="col-xs-5" style="align-items: center; margin-bottom: 15px; display: flex; padding-top:15px">
          <div id="id_total_time"></div>
        </div>
        <div class="col-xs-10" style="align-items: center; background-color: white; margin-bottom: 15px; display: flex;">
          <div id="id_case_time"></div>
        </div>
      </div>
    '''
      # item_uid = activity['uid']
      # item = Activity.get(item_uid)
      
    return ret_html

  def prepare_case_html(self):
    ret_html = '''
      <div class ="col-xs-7" style="justify-content: center; padding: 0px;">
        <div class="col-xs-4" style="align-items: center; padding: 7px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <i class="fa-regular fa-clock-three" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Open Cases</span>
                <div id="" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-4" style="align-items: center; padding: 7px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-square-dollar" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Closed Cases</span>
                <div id="id_case_expense" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-4" style="align-items: center; padding: 7px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-square-dollar" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Total Clients</span>
                <div id="id_case_expense" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 7px">
          <div class="p-3" style="background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; color: white;">
            <div style="display:flex; align-items:center;">
              <i class="fa-solid fa-ballot-check" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Open Tasks</span>
                <div style="font-weight: bold; font-size: 1.6em;">2</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding-left: 7px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-ballot-check" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Future Events</span>
                <div style="font-weight: bold; font-size: 1.6em;">6</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem">Cases by Stage</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem">Cases by Practice Area</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id=""></div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-left: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id=""></div>
        </div>
      </div>
      <div class ="col-xs-5" style="justify-content: center; padding: 0px; background-color: white;">
        <div class="col-xs-5" style="align-items: center; margin-bottom: 15px; display: flex; padding-top:15px">
          <div id="id_total_time"></div>
        </div>
        <div class="col-xs-10" style="align-items: center; background-color: white; margin-bottom: 15px; display: flex;">
          <div id=""></div>
        </div>
      </div>
    '''
      # item_uid = activity['uid']
      # item = Activity.get(item_uid)
      
    return ret_html

  def prepare_finance_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-finance-analytics">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_firm_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-firm-analytics">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_lead_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-lead-analytics">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''
  
  def prepare_lead_intake_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-lead_intake-analytics">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

  def prepare_staff_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-staff-analytics">
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
    if selected_index == 1 and not self.caseTabInitialized:
      self.init_case_tab()
      self.caseTabInitialized = True
    elif selected_index == 2 and not self.financeTabInitialized:
      self.init_finance_tab()
      self.financeTabInitialized = True
    elif selected_index == 3 and not self.firmTabInitialized:
      self.init_firm_tab()
      self.firmTabInitialized = True
    elif selected_index == 4 and not self.leadTabInitialized:
      self.init_lead_tab()
      self.leadTabInitialized = True
    elif selected_index == 5 and not self.lead_intakeTabInitialized:
      self.init_lead_intake_tab()
      self.lead_intakeTabInitialized = True
    elif selected_index == 6 and not self.staffTabInitialized:
      self.init_staff_tab()
      self.staffTabInitialized = True

  def dropdown_period_change(self, args):
    print(args.value)
    duration = 0
    if args.value == 'This Month':
      total_time_entry = 0
      time_entry_activity = []
      for time_entries in init_time_entry_activity:
        new_timeentry_activity = {}
        date = time_entries['date']
        current_date = datetime.date.today()
        if date.year == current_date.year and date.month == current_date.month:
          total_time_entry += time_entries['timeentry']
          new_timeentry_activity['activity'] = time_entries['activity']
          new_timeentry_activity['timeentry'] = time_entries['timeentry']
          time_entry_activity.append(new_timeentry_activity)
      time_entry = float(total_time_entry)
      formatted_time_entry = "{:.2f}".format(time_entry)
      ret_time_entry_html = f'''
        {formatted_time_entry}
      '''
      jQuery("#id_time_entry").empty().append(ret_time_entry_html)
  
      Case_Expenses = 0
      for Expenses in init_expenses:
        date = Expenses['date']
        current_date = datetime.date.today()
        if date.year == current_date.year and date.month == current_date.month:
          Case_Expenses += Expenses['total']
      Case_Expense = float(Case_Expenses)
      formatted_Case_Expense = "{:.2f}".format(Case_Expense)
      ret_case_expense_html = f'''
        $ {formatted_Case_Expense}
      '''
      jQuery("#id_case_expense").empty().append(ret_case_expense_html)
      
      chartData_time_staff = []
      for staff_time in init_time_staff:
        new_staff_time = {}
        new_staff_time['name'] = staff_time['name']
        new_staff_time['time'] = staff_time['time']
        chartData_time_staff.append(new_staff_time)
      print(chartData_time_staff)
      chart_time_staff = ej.charts.Chart({
        'primaryXAxis': {
            'valueType': 'Category'
        },
        'primaryYAxis': {
            'minimum': 0, 'maximum': 0.1, 'interval': 0.02
        },
        'series':[{
            'dataSource': chartData_time_staff,
            'xName': 'name', 'yName': 'time',
            'type': 'Column'
        }],
        # 'isTransposed': True,
      }, "#id_time_staff")
      ret_time_staff_html = f'''
        {chart_time_staff}
      '''
      jQuery("#id_time_staff").append(ret_time_staff_html)
      
      chartData_time_activity = []
      for temp_timeentry_activity in time_entry_activity:
        new_time_activity = {}
        new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
        new_time_activity['activity'] = temp_timeentry_activity['activity']
        chartData_time_activity.append(new_time_activity)
      chart_time_activity = ej.charts.AccumulationChart({
        'series': [
          {
              'dataSource': chartData_time_activity, 
              'innerRadius': '40%',
              'xName': 'timeentry',
              'yName': 'activity'
          }
        ]
      }, '#id_time_activity')
      ret_time_activity_html = f'''
        {chart_time_activity}
      '''
      jQuery("#id_time_activity").append(ret_time_activity_html)
      
      Case_Timeentry = [{'case': 'Case', 'total_period':'Period Total'}]
      for cases in init_case_timeentry:
        new_case = {}
        date = cases['date']
        current_date = datetime.date.today()
        if date.year == current_date.year and date.month == current_date.month:
          new_case['case'] = cases['case']
          new_case['total_period'] = cases['total_period']
          Case_Timeentry.append(new_case)
      
      ret_case_time_html = ""
      ret_case_time_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
      for item in Case_Timeentry:
        if item['case'] == "Case":
          ret_case_time_html += '''<colgroup><col span="1" style="width:80%"><col span="1" style="width:20%"></colgroup>'''
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['case'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
        else:
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['case'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</td></tr>"
      ret_case_time_html += "</table>"
      jQuery("#id_case_time").empty().append(ret_case_time_html)
      
    elif args.value == 'This Year':
      total_time_entry = 0
      time_entry_activity = []
      for time_entries in init_time_entry_activity:
        new_timeentry_activity = {}
        date = time_entries['date']
        current_date = datetime.date.today()
        if date.year == current_date.year:
          total_time_entry += time_entries['timeentry']
          new_timeentry_activity['activity'] = time_entries['activity']
          new_timeentry_activity['timeentry'] = time_entries['timeentry']
          time_entry_activity.append(new_timeentry_activity)
      time_entry = float(total_time_entry)
      formatted_time_entry = "{:.2f}".format(time_entry)
      ret_time_entry_html = f'''
        {formatted_time_entry}
      '''
      jQuery("#id_time_entry").empty().append(ret_time_entry_html)
  
      Case_Expenses = 0
      for Expenses in init_expenses:
        date = Expenses['date']
        current_date = datetime.date.today()
        if date.year == current_date.year:
          Case_Expenses += Expenses['total']
      Case_Expense = float(Case_Expenses)
      formatted_Case_Expense = "{:.2f}".format(Case_Expense)
      ret_case_expense_html = f'''
        $ {formatted_Case_Expense}
      '''
      jQuery("#id_case_expense").empty().append(ret_case_expense_html)
      
      chartData_time_staff = []
      for staff_time in init_time_staff:
        new_staff_time = {}
        new_staff_time['name'] = staff_time['name']
        new_staff_time['time'] = staff_time['time']
        chartData_time_staff.append(new_staff_time)
      print(chartData_time_staff)
      chart_time_staff = ej.charts.Chart({
        'primaryXAxis': {
            'valueType': 'Category'
        },
        'primaryYAxis': {
            'minimum': 0, 'maximum': 0.1, 'interval': 0.02
        },
        'series':[{
            'dataSource': chartData_time_staff,
            'xName': 'name', 'yName': 'time',
            'type': 'Column'
        }],
        # 'isTransposed': True,
      }, "#id_time_staff")
      ret_time_staff_html = f'''
        {chart_time_staff}
      '''
      jQuery("#id_time_staff").append(ret_time_staff_html)
      
      chartData_time_activity = []
      for temp_timeentry_activity in time_entry_activity:
        new_time_activity = {}
        new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
        new_time_activity['activity'] = temp_timeentry_activity['activity']
        chartData_time_activity.append(new_time_activity)
      chart_time_activity = ej.charts.AccumulationChart({
        'series': [
          {
              'dataSource': chartData_time_activity, 
              'innerRadius': '40%',
              'xName': 'time_entry',
              'yName': 'activity'
          }
        ]
      }, '#id_time_activity')
      ret_time_activity_html = f'''
        {chart_time_activity}
      '''
      jQuery("#id_time_activity").append(ret_time_activity_html)
      
      Case_Timeentry = [{'case': 'Case', 'total_period':'Period Total'}]
      for cases in init_case_timeentry:
        new_case = {}
        date = cases['date']
        current_date = datetime.date.today()
        if date.year == current_date.year:
          new_case['case'] = cases['case']
          new_case['total_period'] = cases['total_period']
          Case_Timeentry.append(new_case)
      
      ret_case_time_html = ""
      ret_case_time_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
      for item in Case_Timeentry:
        if item['case'] == "Case":
          ret_case_time_html += '''<colgroup><col span="1" style="width:80%"><col span="1" style="width:20%"></colgroup>'''
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['case'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
        else:
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['case'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</td></tr>"
      ret_case_time_html += "</table>"
      jQuery("#id_case_time").empty().append(ret_case_time_html)

    elif args.value == 'Last One Month':
      duration = 30
      print("Duration", duration)
      total_time_entry = 0
      time_entry_activity = []
      for time_entries in init_time_entry_activity:
        new_timeentry_activity = {}
        date = time_entries['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          total_time_entry += time_entries['timeentry']
          new_timeentry_activity['activity'] = time_entries['activity']
          new_timeentry_activity['timeentry'] = time_entries['timeentry']
          time_entry_activity.append(new_timeentry_activity)
      time_entry = float(total_time_entry)
      formatted_time_entry = "{:.2f}".format(time_entry)
      ret_time_entry_html = f'''
        {formatted_time_entry}
      '''
      jQuery("#id_time_entry").empty().append(ret_time_entry_html)
  
      Case_Expenses = 0
      for Expenses in init_expenses:
        date = Expenses['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          Case_Expenses += Expenses['total']
      Case_Expense = float(Case_Expenses)
      formatted_Case_Expense = "{:.2f}".format(Case_Expense)
      ret_case_expense_html = f'''
        $ {formatted_Case_Expense}
      '''
      jQuery("#id_case_expense").empty().append(ret_case_expense_html)
      
      chartData_time_staff = []
      for staff_time in init_time_staff:
        new_staff_time = {}
        new_staff_time['name'] = staff_time['name']
        new_staff_time['time'] = staff_time['time']
        chartData_time_staff.append(new_staff_time)
      print(chartData_time_staff)
      chart_time_staff = ej.charts.Chart({
        'primaryXAxis': {
            'valueType': 'Category'
        },
        'primaryYAxis': {
            'minimum': 0, 'maximum': 0.1, 'interval': 0.02
        },
        'series':[{
            'dataSource': chartData_time_staff,
            'xName': 'name', 'yName': 'time',
            'type': 'Column'
        }],
        # 'isTransposed': True,
      }, "#id_time_staff")
      ret_time_staff_html = f'''
        {chart_time_staff}
      '''
      jQuery("#id_time_staff").append(ret_time_staff_html)
      
      chartData_time_activity = []
      for temp_timeentry_activity in time_entry_activity:
        new_time_activity = {}
        new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
        new_time_activity['activity'] = temp_timeentry_activity['activity']
        chartData_time_activity.append(new_time_activity)
      chart_time_activity = ej.charts.AccumulationChart({
        'series': [
          {
              'dataSource': chartData_time_activity, 
              'innerRadius': '40%',
              'xName': 'time_entry',
              'yName': 'activity'
          }
        ]
      }, '#id_time_activity')
      ret_time_activity_html = f'''
        {chart_time_activity}
      '''
      jQuery("#id_time_activity").append(ret_time_activity_html)
      
      Case_Timeentry = [{'case': 'Case', 'total_period':'Period Total'}]
      for cases in init_case_timeentry:
        new_case = {}
        date = cases['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          new_case['case'] = cases['case']
          new_case['total_period'] = cases['total_period']
          Case_Timeentry.append(new_case)
      
      ret_case_time_html = ""
      ret_case_time_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
      for item in Case_Timeentry:
        if item['case'] == "Case":
          ret_case_time_html += '''<colgroup><col span="1" style="width:80%"><col span="1" style="width:20%"></colgroup>'''
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['case'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
        else:
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['case'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</td></tr>"
      ret_case_time_html += "</table>"
      jQuery("#id_case_time").empty().append(ret_case_time_html)
    elif args.value == 'Last Three Month':
      duration = 90
      total_time_entry = 0
      time_entry_activity = []
      for time_entries in init_time_entry_activity:
        new_timeentry_activity = {}
        date = time_entries['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          total_time_entry += time_entries['timeentry']
          new_timeentry_activity['activity'] = time_entries['activity']
          new_timeentry_activity['timeentry'] = time_entries['timeentry']
          time_entry_activity.append(new_timeentry_activity)
      time_entry = float(total_time_entry)
      formatted_time_entry = "{:.2f}".format(time_entry)
      ret_time_entry_html = f'''
        {formatted_time_entry}
      '''
      jQuery("#id_time_entry").empty().append(ret_time_entry_html)
  
      Case_Expenses = 0
      for Expenses in init_expenses:
        date = Expenses['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          Case_Expenses += Expenses['total']
      Case_Expense = float(Case_Expenses)
      formatted_Case_Expense = "{:.2f}".format(Case_Expense)
      ret_case_expense_html = f'''
        $ {formatted_Case_Expense}
      '''
      jQuery("#id_case_expense").empty().append(ret_case_expense_html)
      
      chartData_time_staff = []
      for staff_time in init_time_staff:
        new_staff_time = {}
        new_staff_time['name'] = staff_time['name']
        new_staff_time['time'] = staff_time['time']
        chartData_time_staff.append(new_staff_time)
      print(chartData_time_staff)
      chart_time_staff = ej.charts.Chart({
        'primaryXAxis': {
            'valueType': 'Category'
        },
        'primaryYAxis': {
            'minimum': 0, 'maximum': 0.1, 'interval': 0.02
        },
        'series':[{
            'dataSource': chartData_time_staff,
            'xName': 'name', 'yName': 'time',
            'type': 'Column'
        }],
        # 'isTransposed': True,
      }, "#id_time_staff")
      ret_time_staff_html = f'''
        {chart_time_staff}
      '''
      jQuery("#id_time_staff").append(ret_time_staff_html)
      
      chartData_time_activity = []
      for temp_timeentry_activity in time_entry_activity:
        new_time_activity = {}
        new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
        new_time_activity['activity'] = temp_timeentry_activity['activity']
        chartData_time_activity.append(new_time_activity)
      chart_time_activity = ej.charts.AccumulationChart({
        'series': [
          {
              'dataSource': chartData_time_activity, 
              'innerRadius': '40%',
              'xName': 'time_entry',
              'yName': 'activity'
          }
        ]
      }, '#id_time_activity')
      ret_time_activity_html = f'''
        {chart_time_activity}
      '''
      jQuery("#id_time_activity").append(ret_time_activity_html)
      
      Case_Timeentry = [{'case': 'Case', 'total_period':'Period Total'}]
      for cases in init_case_timeentry:
        new_case = {}
        date = cases['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          new_case['case'] = cases['case']
          new_case['total_period'] = cases['total_period']
          Case_Timeentry.append(new_case)
      
      ret_case_time_html = ""
      ret_case_time_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
      for item in Case_Timeentry:
        if item['case'] == "Case":
          ret_case_time_html += '''<colgroup><col span="1" style="width:80%"><col span="1" style="width:20%"></colgroup>'''
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['case'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
        else:
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['case'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</td></tr>"
      ret_case_time_html += "</table>"
      jQuery("#id_case_time").empty().append(ret_case_time_html)
    else:
      duration = 365
      total_time_entry = 0
      time_entry_activity = []
      for time_entries in init_time_entry_activity:
        new_timeentry_activity = {}
        date = time_entries['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          total_time_entry += time_entries['timeentry']
          new_timeentry_activity['activity'] = time_entries['activity']
          new_timeentry_activity['timeentry'] = time_entries['timeentry']
          time_entry_activity.append(new_timeentry_activity)
      time_entry = float(total_time_entry)
      formatted_time_entry = "{:.2f}".format(time_entry)
      ret_time_entry_html = f'''
        {formatted_time_entry}
      '''
      jQuery("#id_time_entry").empty().append(ret_time_entry_html)
  
      Case_Expenses = 0
      for Expenses in init_expenses:
        date = Expenses['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          Case_Expenses += Expenses['total']
      Case_Expense = float(Case_Expenses)
      formatted_Case_Expense = "{:.2f}".format(Case_Expense)
      ret_case_expense_html = f'''
        $ {formatted_Case_Expense}
      '''
      jQuery("#id_case_expense").empty().append(ret_case_expense_html)
      
      chartData_time_staff = []
      for staff_time in init_time_staff:
        new_staff_time = {}
        new_staff_time['name'] = staff_time['name']
        new_staff_time['time'] = staff_time['time']
        chartData_time_staff.append(new_staff_time)
      print(chartData_time_staff)
      chart_time_staff = ej.charts.Chart({
        'primaryXAxis': {
            'valueType': 'Category'
        },
        'primaryYAxis': {
            'minimum': 0, 'maximum': 0.1, 'interval': 0.02
        },
        'series':[{
            'dataSource': chartData_time_staff,
            'xName': 'name', 'yName': 'time',
            'type': 'Column'
        }],
        # 'isTransposed': True,
      }, "#id_time_staff")
      ret_time_staff_html = f'''
        {chart_time_staff}
      '''
      jQuery("#id_time_staff").append(ret_time_staff_html)
      
      chartData_time_activity = []
      for temp_timeentry_activity in time_entry_activity:
        new_time_activity = {}
        new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
        new_time_activity['activity'] = temp_timeentry_activity['activity']
        chartData_time_activity.append(new_time_activity)
      chart_time_activity = ej.charts.AccumulationChart({
        'series': [
          {
              'dataSource': chartData_time_activity, 
              'innerRadius': '40%',
              'xName': 'time_entry',
              'yName': 'activity'
          }
        ]
      }, '#id_time_activity')
      ret_time_activity_html = f'''
        {chart_time_activity}
      '''
      jQuery("#id_time_activity").append(ret_time_activity_html)
      
      Case_Timeentry = [{'case': 'Case', 'total_period':'Period Total'}]
      for cases in init_case_timeentry:
        new_case = {}
        date = cases['date']
        current_date = datetime.date.today()
        days = (current_date - date).days
        if days <= duration:
          new_case['case'] = cases['case']
          new_case['total_period'] = cases['total_period']
          Case_Timeentry.append(new_case)
      
      ret_case_time_html = ""
      ret_case_time_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
      for item in Case_Timeentry:
        if item['case'] == "Case":
          ret_case_time_html += '''<colgroup><col span="1" style="width:80%"><col span="1" style="width:20%"></colgroup>'''
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['case'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
        else:
          ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['case'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</td></tr>"
      ret_case_time_html += "</table>"
      jQuery("#id_case_time").empty().append(ret_case_time_html)

    

  def init_billing_tab(self):
    dropdown_period = ej.dropdowns.DropDownList({
      'dataSource': PM_AV_PERIOD,
      'placeholder': "Select a Period",
      'value': "This Month",
    }, "#id_total_time")
    
    dropdown_period.addEventListener('change', self.dropdown_period_change)

    # append time entry data to init_time_entry_activity list
    all_time_entries = TimeEntry.search()
    for time_entries in all_time_entries:
      new_timeentry_activity = {}
      if time_entries['activity'] is not None:
        new_timeentry_activity['date'] = time_entries['date']
        new_timeentry_activity['activity'] = time_entries['activity'].name
        new_timeentry_activity['timeentry'] = time_entries['duration']
        if time_entries['case'] is not None:
          new_timeentry_activity['case'] = time_entries['case'].case_name
        else:
          new_timeentry_activity['case'] = None
        init_time_entry_activity.append(new_timeentry_activity)
    # append expenses data to the init_expenses list
    all_Expenses = Expense.search()
    for Expenses in all_Expenses:
      new_expenses = {}
      new_expenses['date'] = Expenses['date']
      new_expenses['total'] = Expenses['total']
      init_expenses.append(new_expenses)
    # append staff and time data to the init_time_staff
    all_staff_time = Staff.search()
    for staff_time in all_staff_time:
      new_staff_time = {}
      new_staff_time['name'] = staff_time['first_name']
      new_staff_time['time'] = staff_time['intake_performance_incentive']
      init_time_staff.append(new_staff_time)
    # append case and timeentry data to the init_case_timeentry
    all_cases = Case.search()
    for cases in all_cases:
      new_case = {}
      total_period = 0
      new_case['date'] = cases['incident_date']
      new_case['case'] = cases['case_name']
      for casetimeentry in init_time_entry_activity:
        if casetimeentry['case'] == cases['case_name']:
          if casetimeentry['timeentry'] is not None:
            total_period += casetimeentry['timeentry']
          else:
            total_period += 0
      new_case['total_period'] = total_period
      init_case_timeentry.append(new_case)
    
    # initialize billing page
    total_time_entry = 0
    time_entry_activity = []
    for time_entries in init_time_entry_activity:
      new_timeentry_activity = {}
      date = time_entries['date']
      current_date = datetime.date.today()
      if date.year == current_date.year and date.month == current_date.month:
        total_time_entry += time_entries['timeentry']
        new_timeentry_activity['activity'] = time_entries['activity']
        new_timeentry_activity['timeentry'] = time_entries['timeentry']
        time_entry_activity.append(new_timeentry_activity)
    time_entry = float(total_time_entry)
    formatted_time_entry = "{:.2f}".format(time_entry)
    ret_time_entry_html = f'''
      {formatted_time_entry}
    '''
    jQuery("#id_time_entry").empty().append(ret_time_entry_html)

    Case_Expenses = 0
    for Expenses in init_expenses:
      date = Expenses['date']
      current_date = datetime.date.today()
      if date.year == current_date.year and date.month == current_date.month:
        Case_Expenses += Expenses['total']
    Case_Expense = float(Case_Expenses)
    formatted_Case_Expense = "{:.2f}".format(Case_Expense)
    ret_case_expense_html = f'''
      $ {formatted_Case_Expense}
    '''
    jQuery("#id_case_expense").append(ret_case_expense_html)
    
    chartData_time_staff = []
    for staff_time in init_time_staff:
      new_staff_time = {}
      new_staff_time['name'] = staff_time['name']
      new_staff_time['time'] = staff_time['time']
      chartData_time_staff.append(new_staff_time)
    print(chartData_time_staff)
    chart_time_staff = ej.charts.Chart({
      'primaryXAxis': {
          'valueType': 'Category'
      },
      'primaryYAxis': {
          'minimum': 0, 'maximum': 0.1, 'interval': 0.02
      },
      'series':[{
          'dataSource': chartData_time_staff,
          'xName': 'name', 'yName': 'time',
          'type': 'Column'
      }],
      # 'isTransposed': True,
    }, '#id_time_staff')
    ret_time_staff_html = f'''
      {chart_time_staff}
    '''
    jQuery("#id_time_staff").append(ret_time_staff_html)
    
    chartData_time_activity = []
    for temp_timeentry_activity in time_entry_activity:
      new_time_activity = {}
      new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
      new_time_activity['activity'] = temp_timeentry_activity['activity']
      chartData_time_activity.append(new_time_activity)
    chart_time_activity = ej.charts.AccumulationChart({
      'series': [
        {
            'dataSource': chartData_time_activity, 
            'innerRadius': '40%',
            'xName': 'time_entry',
            'yName': 'activity'
        }
      ]
    }, '#id_time_activity')
    ret_time_activity_html = f'''
      {chart_time_activity}
    '''
    jQuery("#id_time_activity").append(ret_time_activity_html)
    
    Case_Timeentry = [{'case': 'Case', 'total_period':'Period Total'}]
    for cases in init_case_timeentry:
      new_case = {}
      date = cases['date']
      current_date = datetime.date.today()
      if date.year == current_date.year and date.month == current_date.month:
        new_case['case'] = cases['case']
        new_case['total_period'] = cases['total_period']
        Case_Timeentry.append(new_case)
    
    ret_case_time_html = ""
    ret_case_time_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
    for item in Case_Timeentry:
      if item['case'] == "Case":
        ret_case_time_html += '''<colgroup><col span="1" style="width:80%"><col span="1" style="width:20%"></colgroup>'''
        ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['case'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
      else:
        ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['case'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</td></tr>"
    ret_case_time_html += "</table>"
    jQuery("#id_case_time").append(ret_case_time_html)

    # <div class="col-xs-12">{activity['address']}</div>
  
  def init_case_tab(self):
    pass
    
  def init_finance_tab(self):
    pass

  def init_firm_tab(self):
    pass

  def init_lead_tab(self):
    pass

  def init_lead_intake_tab(self):
    pass
  
  def init_staff_tab(self):
    pass

  
  
  def destroy(self):
    if self.container_el:
      self.container_el.innerHTML = ''