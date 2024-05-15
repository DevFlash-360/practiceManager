import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta, datetime
from collections import defaultdict

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *

from ..app.models import Staff, User, Contact, Activity, AppAuditLog, TimeEntry, Expense, Case, Task, Event, Payment, Lead, Client, Timesheet, PerformanceIncentive

PM_AV_PERIOD = [
  'This Month',
  'Last One Month',
  'Last Three Month',
  'This Year',
  'Last One Year',
]
PM_FINANCE_STAFF_INCENTIVES_REPORT_PERIOD = [
  'This Month',
  'Last Month',
  'Same Month Last Year',
  'This Year',
  'Last Year'
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
    staff_html = self.prepare_staff_html()
    
    self.billingTabInitialized  = False
    self.caseTabInitialized = False
    self.financeTabInitialized = False
    self.firmTabInitialized = False
    self.leadTabInitialized = False
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
                <div id="id_billing_time_entry" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
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
                <div id="id_billing_case_expense" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
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
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem; font-weight: bold;">Time vs Staff this Month</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem; font-weight: bold;">Time Entries vs Activity</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_billing_time_staff"></div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-left: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_billing_time_activity"></div>
        </div>
      </div>
      <div class ="col-xs-5" style="justify-content: center; padding: 0px;"> 
        <div class="col-xs-12" style="align-items: center;  padding: 8px; font-size: 1.8rem; font-weight: bold;">Total Time By Case</div>
        <div class ="col-xs-12" style="justify-content: center; padding: 0px; background-color: white; overflow-y: scroll; height: 700px;">  
          <div class="col-xs-5" style="align-items: center; margin-bottom: 15px; display: flex; padding-top:15px">
            <div id="id_billing_total_time"></div>
          </div>
          <div class="col-xs-10" style="align-items: center; margin-bottom: 15px; display: flex;">
            <div id="id_billing_case_time"></div>
          </div>
        </div>
      </div>
    '''
      
    return ret_html

  def prepare_case_html(self):
    ret_html = '''
      <div class ="col-xs-7" style="justify-content: center; padding: 0px;">
        <div class="col-xs-4" style="align-items: center; padding: 10px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-business-time" aria-hidden="true" style="color: #0d3a87; margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Open Cases</span>
                <div id="id_case_open_cases" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-4" style="align-items: center; padding: 10px">
          <div class="p-3" style="background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; color: white;">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-business-time" aria-hidden="true" style="color: #ffffff; margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Closed Cases</span>
                <div id="id_case_closed_cases" style="font-weight: bold; font-size: 1.6em"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-4" style="align-items: center; padding: 10px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <i class="fa-light fa-children" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Total Clients</span>
                <div id="id_case_total_clients" style="font-weight: bold; font-size: 1.6em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 10px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <i class="fa-solid fa-check-double" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Open Tasks</span>
                <div id="id_case_open_tasks" style="font-weight: bold; font-size: 1.6em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 10px">
          <div class="p-3" style="background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <i class="fa-solid fa-user" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Total Staffs</span>
                <div id="id_case_total_staffs" style="font-weight: bold; font-size: 1.6em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem; font-weight: bold;">Cases by Stage</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem; font-weight: bold;">Cases by Practice Area</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_case_cases_by_stage"></div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-left: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_case_cases_by_pracetice_area"></div>
        </div>
      </div>
      <div class ="col-xs-5" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center; margin-top: 10px; padding: 7px; font-size: 2rem; background-color: rgb(245, 245, 245); font-weight: bold;">Contacts Map</div>
        <div class="col-xs-12" style="align-items: center; background-color: white; margin-bottom: 15px; display: flex; height: 618px;">
          <div id="id_case_contact_map"></div>
        </div>
      </div>
    '''
      
    return ret_html

  def prepare_finance_html(self):
    ret_html = '''
    <div class ="col-xs-12" style="justify-content: center; padding: 0px;">  
      <div class ="col-xs-8" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center;  padding: 8px; font-size: 1.8rem; font-weight: bold;">Payroll & Expenses</div>
        <div class="col-xs-6" style="align-items: center; padding: 8px; padding-top: 0px">
          <div class="p-3" style="padding: 5px; background-color: white; difsplay: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center; justify-content:center;">
              <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Current Period Payroll</span>
                <div id="id_finance_current_period_payroll" style="font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px; padding-top: 0px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Firm Expenses this Month</span>
                <div id="id_finance_firm_expenses_this_month" style="font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center;  padding: 8px; font-size: 1.8rem; font-weight: bold;">Revenue Snapshot</div>
        <div class="col-xs-4" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; color: white;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center">This Month</span>
                <div id="id_finance_this_month_revenue" style="text-align: center; font-weight: bold; font-size: 1.4em"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-4" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Same Month Last Year</span>
                <div id="id_finance_same_month_last_year_revenue" style="text-align: center; font-weight: bold; font-size: 1.4em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-xs-4" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Last Month</span>
                <div id="id_finance_last_month_revenue" style="text-align: center; font-weight: bold; font-size: 1.4em; color: #333"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Current Month Projection</span>
                <div id="id_finance_current_month_projection" style="text-align: center; font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Average Daily Revenue in this Month</span>
                <div id="id_finance_average_daily_revenue" style="text-align: center; font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center;  padding-right: 8px; font-size: 1.8rem; font-weight: bold;">Current Month Stats</div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Total Referals</span>
                <div id="id_finance_total_referrals" style="text-align: center; font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Total (-)Referrals</span>
                <div id="id_finance_total_minus_referrals" style="text-align: center; font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">New Clients this Month</span>
                <div id="id_finance_new_clients_this_month" style="text-align: center; font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Existing Clients this Month</span>
                <div id="id_finance_existing_clients_this_month" style="text-align: center; font-weight: bold; font-size: 1.4em;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class ="col-xs-4" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center; padding: 8px; font-size: 1.8rem; font-weight: bold;">Staff Incentives Report</div>
        <div class="col-xs-12" style="align-items: center; background-color: white; height: 421px; overflow-y: scroll;">
          <div class="col-xs-9" style="align-items: center; margin-bottom: 15px; padding-top:15px; max-height: 100%;">
            <div id="id_finance_period"></div>
          </div>
          <div class="col-xs-9" style="align-items: center; background-color: white; margin-bottom: 15px; ">
            <div id="id_finance_staff_incentives_report"></div>
          </div>
        </div>
      </div>
    </div>
    <div class ="col-xs-12" style="justify-content: center; padding: 0px;">
      <div class="col-xs-6" style="align-items: center;  padding: 8px; padding-top: 2px; font-size: 1.8rem; font-weight: bold;">Current Month Revenue by Day</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; padding-top: 2px; font-size: 1.8rem; font-weight: bold;">Revenue by Month</div>
      <div class="col-xs-6" style="align-items: center; padding: 8px; padding-top: 2px;">
        <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; height: 250px">
          <div id="id_finance_current_month_revenue_by_day"></div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; padding-top: 2px; padding-right: 0px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 250px">
          <div id="id_finance_revenue_by_month"></div>
        </div>
      </div>
    </div>
    '''
      
    return ret_html

  def prepare_firm_html(self):
    ret_html = '''
    <div class ="col-xs-12" style="justify-content: center; padding: 0px;">
      <div class="col-xs-4" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; difsplay: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center; justify-content:center;">
            <i class="fa-duotone fa-users" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Total Staff</span>
              <div id="id_firm_total_staff" style="font-weight: bold; font-size: 1.4em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-4" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-thin fa-phone-intercom" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Employee Devices</span>
              <div id="id_firm_employee_devices" style="font-weight: bold; font-size: 1.4em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-4" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-light fa-print" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Office Devices</span>
              <div id="id_firm_office_devices" style="font-weight: bold; font-size: 1.4em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; font-size: 1.8rem; margin-bottom: 4px; font-weight: bold;">Staff vs Hourly</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; font-size: 1.8rem; margin-bottom: 4px; font-weight: bold;">Staff vs Salary</div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; height: 260px">
          <div style="color: white" id="id_firm_staff_vs_hourly"></div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 260px">
          <div style="background-color: white;" id="id_firm_staff_vs_salary"></div>
        </div>
      </div> 
      <div class="col-xs-6" style="align-items: center;  padding: 8px; margin-bottom: 4px; font-size: 1.8rem; font-weight: bold;">Gender Demographics</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; margin-bottom: 4px; font-size: 1.8rem; font-weight: bold;">Race Demographics</div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 290px">
          <div style="background-color: white;" id="id_firm_gender_demographics"></div>
        </div>
      </div> 
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 290px">
          <div style="background-color: white;" id="id_firm_race_demographics"></div>
        </div>
      </div> 
    </div>
    '''
      
    return ret_html

  def prepare_lead_html(self):
    ret_html = '''
    <div class ="col-xs-12" style="justify-content: center; padding: 0px;">
      <div class ="col-xs-6" style="justify-content: center; padding: 0px; padding-top: 42px">
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); color: white; difsplay: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center; justify-content:center;">
              <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Average Value of Open Leads</span>
                <div id="id_lead_average_value_of_open_leads" style="font-weight: bold; font-size: 1.6em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Average Vlaue of Won Leads</span>
                <div id="id_lead_average_value_of_won_leads" style="font-weight: bold; font-size: 1.6em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Average Value of Lost Leads</span>
                <div id="id_lead_average_value_of_lost_leads" style="font-weight: bold; font-size: 1.6em;">$</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class ="col-xs-6" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center;  padding: 12px; font-size: 1.8rem; font-weight: bold;">Open Deals by Stage</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px; padding-top: 0px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 218px">
            <div id="id_lead_open_deals_by_stage"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-8" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center; padding: 4px; padding-left: 8px; font-size: 1.8rem; font-weight: bold;">Lead Source vs Status</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 409px">
            <div id="id_lead_lead_source_vs_status"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-4" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center;  padding: 4px; font-size: 1.8rem; font-weight: bold;">Total Won Rate</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; padding-top: 40px; background-color: white; sdisplay: flex; align-items:center; justify-content: center; height: 180px">
            <div id="id_lead_won_rate"></div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center; padding: 4px; font-size: 1.8rem; font-weight: bold;">Won vs Lost by Stage</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
            <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 180px">
            <div id="id_lead_conversion_by_stage"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-4" style="justify-content: center; padding: 0px; padding-top: 34px">
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Total Won Leads</span>
                <div id="id_lead_total_won_lead" style="text-align: center; font-weight: bold; font-size: 1.6em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Total Lost Leads</span>
                <div id="id_lead_total_lost_lead" style="text-align: center; font-weight: bold; font-size: 1.6em;"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center; padding: 4px; padding-left: 8px; font-size: 1.8rem;font-weight: bold;">Lost Reasons</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 260px">
            <div id="id_lead_lost_reasons"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-8" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center; padding: 4px; padding-left: 8px; font-size: 1.8rem; font-weight: bold;">Value of Deals Won vs Lost</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 372px">
            <div id="id_lead_value_of_deals_won_vs_lost"></div>
          </div>
        </div>
      </div>
    </div>
    '''
      
    return ret_html


  def prepare_staff_html(self):
    ret_html = '''
    <div class ="col-xs-12" style="justify-content: center; padding: 0px;">
      <div class="col-xs-12" style="align-items: center; padding: 8px; padding-top: 30px">
        <div class="p-3" style="padding: 5px; background-color: white; difsplay: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center; justify-content:center;">
            <div>
              <span style="padding-left: 32px; padding-bottom: 5px; font-weight: bold; font-size: 1.4em">Current Pay Period</span>
              <div id="id_staff_current_pay_period" style="font-size: 1.3em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Current Period Payroll</span>
              <div id="id_staff_current_period_payroll" style="font-weight: bold; font-size: 1.6em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Total Bonus</span>
              <div id="id_staff_total_bonus" style="font-weight: bold; font-size: 1.6em;">$ </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Incentives</span>
              <div id="id_staff_incentives" style="font-weight: bold; font-size: 1.6em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Overtime Pay</span>
              <div id="id_staff_overtime_pay" style="font-weight: bold; font-size: 1.6em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-thin fa-hourglass-clock" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Total Hours Worked</span>
              <div id="id_staff_total_hours_worked" style="font-weight: bold; font-size: 1.6em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
          <div style="display:flex; align-items:center;">
            <i class="fa-thin fa-hourglass-clock" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
            <div>
              <span style="margin-right: 4px">Overtime Hours</span>
              <div id="id_staff_overtime_hours" style="font-weight: bold; font-size: 1.6em;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; font-size: 1.8rem; font-weight: bold; margin-bottom: 4px">Total Work Hours in Current vs Previous Pay Period</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; font-size: 1.8rem; font-weight: bold; margin-bottom: 4px">Total Payroll in Current vs Previous Pay Period</div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; height: 260px; color: white">
          <div style="color: white" id="id_staff_work_hours_current_vs_previous"></div>
        </div>
      </div>
      <div class="col-xs-6" style="align-items: center; padding: 8px;">
        <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 260px">
          <div style="background-color: white;" id="id_staff_payroll_current_vs_previous"></div>
        </div>
      </div> 
    </div>
    '''

    return ret_html
  
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
    elif selected_index == 5 and not self.staffTabInitialized:
      self.init_staff_tab()
      self.staffTabInitialized = True

  def dropdown_period_change(self, args):
    duration = 0
    if args.value == 'This Month':
      
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
      jQuery("#id_billing_case_time").empty().append(ret_case_time_html)
      
    elif args.value == 'This Year':
      
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
      jQuery("#id_billing_case_time").empty().append(ret_case_time_html)

    elif args.value == 'Last One Month':
      duration = 30
      
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
      jQuery("#id_billing_case_time").empty().append(ret_case_time_html)
      
    elif args.value == 'Last Three Month':
      duration = 90
      
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
      jQuery("#id_billing_case_time").empty().append(ret_case_time_html)
    else:
      duration = 365
      
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
      jQuery("#id_billing_case_time").empty().append(ret_case_time_html)

    

  def init_billing_tab(self):
    dropdown_period = ej.dropdowns.DropDownList({
      'dataSource': PM_AV_PERIOD,
      'placeholder': "Select a Period",
      'value': "This Month",
    }, "#id_billing_total_time")
    
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
    jQuery("#id_billing_time_entry").empty().append(ret_time_entry_html)

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
    jQuery("#id_billing_case_expense").append(ret_case_expense_html)
    
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
    }, '#id_billing_time_staff')
    ret_time_staff_html = f'''
      {chart_time_staff}
    '''
    jQuery("#id_billing_time_staff").append(ret_time_staff_html)
    
    chartData_time_activity = []
    for temp_timeentry_activity in time_entry_activity:
      new_time_activity = {}
      new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
      new_time_activity['activity'] = temp_timeentry_activity['activity']
      chartData_time_activity.append(new_time_activity)
    aggregated = {}
    for entry in chartData_time_activity:
      activity = entry['activity']
      timeentry = entry['timeentry']
      if activity in aggregated:
          aggregated[activity] += timeentry
      else:
          aggregated[activity] = timeentry
  
  # Convert the aggregated dictionary back to a list of dictionaries
    result_time_activity = [{'activity': activity, 'timeentry': timeentry} for activity, timeentry in aggregated.items()]
    chart_time_activity = ej.charts.AccumulationChart({
      'series': [
        {
            'dataSource': result_time_activity, 
            'innerRadius': '40%',
            'xName': 'timeentry',
            'yName': 'activity'
        }
      ]
    }, '#id_billing_time_activity')
    ret_time_activity_html = f'''
      {chart_time_activity}
    '''
    jQuery("#id_billing_time_activity").append(ret_time_activity_html)
    
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
    jQuery("#id_billing_case_time").append(ret_case_time_html)

  
  def init_case_tab(self):

    # Initialize variables
    
    all_cases = Case.search()
    unknown_cases_by_stage_count = 0
    pre_charge_count = 0
    lower_court_count = 0
    upper_court_count = 0
    appeals_court_count = 0
    unknown_practice_area_count = 0
    criminal_defense_count = 0
    family_law_count = 0
    personal_injury_count = 0
    civil_litigation_count = 0
    mass_tort_count = 0
    open_case_count = 0
    closed_case_count = 0
    open_task_count = 0
    total_client = []
    staff_count = 0
    total_temp_staffs = []
    for temp_case in all_cases:
      # cases by stage
      if temp_case['case_stage'] is None:
        unknown_cases_by_stage_count += 1
      elif temp_case['case_stage'].name == 'Pre-Charge':
        pre_charge_count += 1
      elif temp_case['case_stage'].name == 'Lower Court':
        lower_court_count += 1
      elif temp_case['case_stage'].name == 'Upper Court':
        upper_court_count += 1
      else:
        appeals_court_count += 1
      # cases by practice area
      if temp_case['practice_area'] is None:
        unknown_practice_area_count += 1
      elif temp_case['practice_area'].name == 'Criminal Defense':
        criminal_defense_count += 1
      elif temp_case['practice_area'].name == 'Family Law':
        family_law_count += 1
      elif temp_case['practice_area'].name == 'Personal Injury':
        personal_injury_count += 1
      elif temp_case['practice_area'].name == 'Civil Litigation':
        civil_litigation_count += 1
      else:
        mass_tort_count += 1
      # open and closed cases
      if temp_case['case_status'] is not None:
        if temp_case['case_status'].name == "Open":
          open_case_count += 1
        if temp_case['case_status'].name == "Closed":
          closed_case_count += 1
      # total client
      if temp_case['clients']:
        for i in range(len(temp_case['clients'])):
          total_client.append(temp_case['clients'][i].client_name)
      if temp_case['staff']:
        for i in range(len(temp_case['staff'])):
          print("staff full name  ", temp_case['staff'][i].full_name)
          total_temp_staffs.append(temp_case['staff'][i].full_name)
    unique_total_client_count = set(total_client)
    unique_total_temp_staffs = set(total_temp_staffs)
    staff_count = len(unique_total_temp_staffs)
    # open tasks
    all_tasks = Task.search()
    for task in all_tasks:
      temp_task_status = task['completed']
      if temp_task_status is False:
        open_task_count += 1
        
    # Cases by Stage
    chartData_case_stage = [
      {'name': 'Unknown', 'count': unknown_cases_by_stage_count}, 
      {'name': 'Pre-Charge', 'count': pre_charge_count},
      {'name': 'Lower Court', 'count': lower_court_count},
      {'name': 'Upper Court', 'count': upper_court_count},
      {'name': 'Appeals Court', 'count': appeals_court_count},
    ]
    # Cases By Practice Area
    chartData_practice_area = [
      {'name': 'Unknown', 'count': unknown_practice_area_count}, 
      {'name': 'Criminal Defense', 'count': criminal_defense_count},
      {'name': 'Family Law', 'count': family_law_count},
      {'name': 'Personal Injury', 'count': personal_injury_count},
      {'name': 'Civil Litigation', 'count': civil_litigation_count},
      {'name': 'Mass Tort', 'count': mass_tort_count},
    ]
    # Open Cases
    ret_open_cases_html = f'''
      {open_case_count}
    '''
    jQuery("#id_case_open_cases").empty().append(ret_open_cases_html)
    # Closed Cases
    ret_closed_cases_html = f'''
      {closed_case_count}
    '''
    jQuery("#id_case_closed_cases").empty().append(ret_closed_cases_html)
    # Total Clients
    ret_total_clients_html = f'''
      {len(unique_total_client_count)}
    '''
    jQuery("#id_case_total_clients").empty().append(ret_total_clients_html)

    # Open Tasks
    ret_open_tasks_html = f'''
      {open_task_count}
    '''
    jQuery("#id_case_open_tasks").empty().append(ret_open_tasks_html)
    
    ret_open_total_staff_html = f'''
      {staff_count}
    '''
    jQuery("#id_case_total_staffs").empty().append(ret_open_total_staff_html)
    
    # Cases by Stage Chart Part
    chart_case_stage = ej.charts.Chart({
      'primaryXAxis': {
          'valueType': 'Category'
      },
      'primaryYAxis': {
          'minimum': 0, 'maximum': 50, 'interval': 10
      },
      'series':[{
          'dataSource': chartData_case_stage,
          'xName': 'name', 'yName': 'count',
          'type': 'Column'
      }],
      'isTransposed': True,
    }, "#id_case_cases_by_stage")
    ret_case_by_stage_html = f'''
      {chart_case_stage}
    '''
    jQuery("#id_case_cases_by_stage").append(ret_case_by_stage_html)

    # Case by Practice Area Chart Part
    chart_practice_area = ej.charts.AccumulationChart({
      'series': [
        {
            'dataSource': chartData_practice_area, 
            'innerRadius': '0%',
            'xName': 'name',
            'yName': 'count'
        }
      ]
    }, '#id_case_cases_by_pracetice_area')
    ret_case_by_practice_area_html = f'''
      {chart_practice_area}
    '''
    jQuery("#id_case_cases_by_pracetice_area").append(ret_case_by_practice_area_html)

    # Contact Map
    contact_maps = ej.maps.Maps({
      'zoomSettings': {
        'enable': True,
        'toolBars': ["Zoom", "ZoomIn", "ZoomOut", "Pan", "Reset"],
        'zoomFactor': 4
      },
      'centerPosition': {
          'latitude': 29.394708,
          'longitude': -94.954653
      },
      'layers': [
          {
              'urlTemplate':"https://tile.openstreetmap.org/level/tileX/tileY.png"
          }
      ]
    }, '#id_case_contact_map');
    ret_case_contact_map_html = f'''
      {contact_maps}
    '''
    jQuery("#id_case_contact_map").append(ret_case_contact_map_html)

  
  
  def init_finance_tab(self):
    dropdown_finance_staff_incentives_report_period = ej.dropdowns.DropDownList({
      'dataSource': PM_FINANCE_STAFF_INCENTIVES_REPORT_PERIOD,
      'placeholder': "Select a Period",
      'value': "This Month",
    }, "#id_finance_period")
    
    dropdown_finance_staff_incentives_report_period.addEventListener('change', self.dropdown_finance_staff_incentives_report_period_change)
    # Current Period Payroll
    all_timesheet = Timesheet.search()
    total_payroll = 0
    for temp_timesheet in all_timesheet:
      date = temp_timesheet['clock_out_time']
      current_date = datetime.date.today()
      if date.year == current_date.year and date.month == current_date.month:
        total_payroll += temp_timesheet['payroll']
    float_total_payroll = float(total_payroll)
    formatted_total_payroll = "{:.2f}".format(float_total_payroll)
    ret_current_period_payroll_html = f'''
      $ {formatted_total_payroll}
    '''
    jQuery("#id_finance_current_period_payroll").empty().append(ret_current_period_payroll_html)

    # Firm Expenses this Month
    all_expenses = Expense.search()
    total_expenses_this_month = 0
    for temp_expenses in all_expenses:
      date = temp_expenses['date']
      current_date = datetime.date.today()
      if date.year == current_date.year and date.month == current_date.month:
        total_expenses_this_month += temp_expenses['total']
    float_total_expenses_this_month = float(total_expenses_this_month)
    formatted_total_expenses = "{:.2f}".format(float_total_expenses_this_month)
    ret_total_expenses_this_month_html = f'''
      $ {formatted_total_expenses}
    '''
    jQuery("#id_finance_firm_expenses_this_month").empty().append(ret_total_expenses_this_month_html)

    # Revenue Snapshot this month
    all_leads = Lead.search()
    this_month_revenue = 0
    same_month_last_year_revenue = 0
    last_month_revenue = 0
    days = 1
    current_month_revenues = []
    total_referrals_count = 0
    total_minus_referrals_count = 0
    all_revenues = []
    for temp_lead in all_leads:
      current_month_revenue = {}
      all_revenue = {}
      date = temp_lead['updated_time'].date()
      current_date = datetime.date.today()
      last_month_end = current_date.replace(day=1) - timedelta(days=1)
      last_month_start = last_month_end.replace(day=1)
      days = (current_date - last_month_end).days
      all_revenue['date'] = date
      if temp_lead['retainer'] is not None:
        all_revenue['revenue'] = temp_lead['retainer']
      else:
        all_revenue['revenue'] = 0
      all_revenues.append(all_revenue)
      if date.year == current_date.year and date.month == current_date.month:
        if len(temp_lead['referred_by']) == 0:
            total_minus_referrals_count += 1
        else:
          total_referrals_count += 1
        current_month_revenue['date'] = date
        if temp_lead['retainer'] is not None:
          this_month_revenue += temp_lead['retainer']
          current_month_revenue['revenue'] = temp_lead['retainer']
        else:
          this_month_revenue += 0
          current_month_revenue['revenue'] = 0
        current_month_revenues.append(current_month_revenue)  
      if date.year == current_date.year - 1 and date.month == current_date.month:
        if temp_lead['retainer'] is not None:
          same_month_last_year_revenue += temp_lead['retainer']
        else:
          same_month_last_year_revenue += 0
        
      if last_month_start <= date <= last_month_end:
        if temp_lead['retainer'] is not None:
          last_month_revenue += temp_lead['retainer']
        else:
          last_month_revenue = 0
    average_revenue_this_month = this_month_revenue / days
    formatted_this_month_revenue = "{:.2f}".format(this_month_revenue)
    formatted_same_month_last_year_revenue = "{:.2f}".format(same_month_last_year_revenue)
    formatted_last_month_revenue = "{:.2f}".format(last_month_revenue)
    formatted_average_revenue_this_month = "{:.2f}".format(average_revenue_this_month)
    ret_this_month_revenue_html = f'''
      $ {formatted_this_month_revenue}
    '''
    jQuery("#id_finance_this_month_revenue").empty().append(ret_this_month_revenue_html)
    ret_same_month_last_year_revenue_html = f'''
      $ {formatted_same_month_last_year_revenue}
    '''
    jQuery("#id_finance_same_month_last_year_revenue").empty().append(ret_same_month_last_year_revenue_html)
    ret_last_month_revenue_html = f'''
      $ {formatted_last_month_revenue}
    '''
    jQuery("#id_finance_last_month_revenue").empty().append(ret_last_month_revenue_html)
    ret_average_revenue_this_month_html = f'''
      $ {formatted_average_revenue_this_month}
    '''
    jQuery("#id_finance_average_daily_revenue").empty().append(ret_average_revenue_this_month_html)
    
    # Total Referrals
    all_leads = Lead.search()
          
    ret_total_referrals_html = f'''
      {total_referrals_count}
    '''
    jQuery("#id_finance_total_referrals").empty().append(ret_total_referrals_html)    
    ret_total_minus_referrals_html = f'''
      {total_minus_referrals_count}
    '''
    jQuery("#id_finance_total_minus_referrals").empty().append(ret_total_minus_referrals_html) 

    # Clients
    all_clients = Client.search()
    new_clients = []
    old_clients = []
    
    exist_clients_count = 0
    new_clients_count = 0
    for temp_clients in all_clients:
      date = temp_clients['created_time']
      current_date = datetime.date.today()
      print("clients  ", date.year)
      if date.year == current_date.year and date.month == current_date.month:
        new_clients.append(temp_clients['client_name'])
      else:
        old_clients.append(temp_clients['client_name'])
    for new_client in new_clients:
      if new_client in old_clients:
        exist_clients_count += 1
      else:
        new_clients_count += 1
    ret_new_clients_html = f'''
      {new_clients_count}
    '''
    jQuery("#id_finance_new_clients_this_month").empty().append(ret_new_clients_html)
    ret_exist_clients_html = f'''
      {exist_clients_count}
    '''
    jQuery("#id_finance_existing_clients_this_month").empty().append(ret_exist_clients_html)

    # Current Month Revenue by Day
    chart_current_month_revenue = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
        'labelStyle': {
                    'color': '#FFFFFF' 
        }
      },
      'primaryYAxis': {
        'labelStyle': {
                    'color': '#FFFFFF' 
        }
      },
      'series':[{
        'dataSource': current_month_revenues,
        'xName': 'date', 'yName': 'revenue',
        'type': 'Column',
        'width': 10
      }],
      'isTransposed': True,
    }, "#id_finance_current_month_revenue_by_day")
    ret_current_month_revenue_by_day_html = f'''
      {chart_current_month_revenue}
    '''
    jQuery("#id_finance_current_month_revenue_by_day").append(ret_current_month_revenue_by_day_html)

    # Revenue By Month
    grouped_revenues = defaultdict(int)

    for entry in all_revenues:
        # Extract month and year from the date object
        month_year = f"{entry['date'].month:02d}/{entry['date'].year}"
        grouped_revenues[month_year] += entry['revenue']

    combined_revenue_data = [{'date': key, 'revenue': value} for key, value in grouped_revenues.items()]
    chart_revenue_by_month = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category'
      },
      'primaryYAxis': {},
      'series':[{
        'dataSource': combined_revenue_data,
        'xName': 'date', 'yName': 'revenue',
        'type': 'Column',
        'width': 30
      }],
      # 'isTransposed': True,
    }, "#id_finance_revenue_by_month")
    ret_revenue_by_month_html = f'''
      {chart_revenue_by_month}
    '''
    jQuery("#id_finance_revenue_by_month").append(ret_revenue_by_month_html)
    # Staff Incentives Report
    staff_incentives = [{'staff': 'Staff', 'total_period':'Period Total'}]
    all_incentives = PerformanceIncentive.search()
    for temp_incentives in all_incentives:
      new_staff_incentive = {}
      date = temp_incentives['payment'].payment_time
      current_date = datetime.date.today()
      if date.year == current_date.year and date.month == current_date.month:
        new_staff_incentive['staff'] = temp_incentives['staff'].first_name
        new_staff_incentive['total_period'] = temp_incentives['amount']
        staff_incentives.append(new_staff_incentive)
    print(staff_incentives)
    ret_staff_incentive_html = ""
    ret_staff_incentive_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
    for item in staff_incentives:
      if item['staff'] == "Staff":
        ret_staff_incentive_html += '''<colgroup><col span="1" style="width:70%"><col span="1" style="width:30%"></colgroup>'''
        ret_staff_incentive_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['staff'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
      else:
        ret_staff_incentive_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['staff'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">$ ''' + str(item['total_period']) + "</td></tr>"
    ret_staff_incentive_html += "</table>"
    jQuery("#id_finance_staff_incentives_report").empty().append(ret_staff_incentive_html)

  def dropdown_finance_staff_incentives_report_period_change(self, args):
    staff_incentives = [{'staff': 'Staff', 'total_period':'Period Total'}]
    all_incentives = PerformanceIncentive.search()
    for temp_incentives in all_incentives:
      new_staff_incentive = {}
      date = temp_incentives['payment'].payment_time
      current_date = datetime.date.today()
      print(date)
      if args.value == "This Month":
        if date.year == current_date.year and date.month == current_date.month:
          new_staff_incentive['staff'] = temp_incentives['staff'].first_name
          new_staff_incentive['total_period'] = temp_incentives['amount']
          staff_incentives.append(new_staff_incentive)
      elif args.value == "Last Month":
        last_month_end = current_date.replace(day=1) - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        if last_month_start <= date.date() <= last_month_end:
          new_staff_incentive['staff'] = temp_incentives['staff'].first_name
          new_staff_incentive['total_period'] = temp_incentives['amount']
          staff_incentives.append(new_staff_incentive)
      elif args.value == "Same Month Last Year":
        if date.year == current_date.year - 1 and date.month == current_date.month:
          new_staff_incentive['staff'] = temp_incentives['staff'].first_name
          new_staff_incentive['total_period'] = temp_incentives['amount']
          staff_incentives.append(new_staff_incentive)
      elif args.value == "This Year":
        if date.year == current_date.year:
          new_staff_incentive['staff'] = temp_incentives['staff'].first_name
          new_staff_incentive['total_period'] = temp_incentives['amount']
          staff_incentives.append(new_staff_incentive)
      else:
        if date.year == current_date.year - 1:
          new_staff_incentive['staff'] = temp_incentives['staff'].first_name
          new_staff_incentive['total_period'] = temp_incentives['amount']
          staff_incentives.append(new_staff_incentive)
    print(staff_incentives)
    ret_staff_incentive_html = ""
    ret_staff_incentive_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
    for item in staff_incentives:
      if item['staff'] == "Staff":
        ret_staff_incentive_html += '''<colgroup><col span="1" style="width:70%"><col span="1" style="width:30%"></colgroup>'''
        ret_staff_incentive_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['staff'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
      else:
        ret_staff_incentive_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['staff'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">$ ''' + str(item['total_period']) + "</td></tr>"
    ret_staff_incentive_html += "</table>"
    jQuery("#id_finance_staff_incentives_report").empty().append(ret_staff_incentive_html)
      
  
  def init_firm_tab(self):
    # total staff, employee deivces, office devices
    all_staff = Staff.search()
    staffs = []
    employee_devices = []
    office_devices = []
    staff_count = 0
    employee_device_count = 0
    office_device_count = 0
    staff_vs_hourly = []
    staff_vs_salary = []
    gender_unknown_count = 0
    gender_male_count = 0
    gender_female_count = 0
    gender_other_count = 0
    race_unknown_count = 0
    race_caucasian_count = 0
    race_black_or_african_american_count = 0
    race_native_hawaiian_or_other_pacific_islander_count = 0
    race_asian_count = 0
    race_american_indian_or_alaskan_native_count = 0
    race_hispanic_or_latino_count = 0
    
    for temp_staff in all_staff:
      staffs_name = temp_staff['first_name'] + temp_staff['last_name']
      staffs.append(staffs_name)
      employee_devices.append(temp_staff['personal_phone'])
      office_devices.append(temp_staff['work_phone'])
      temp_staff_vs_hourly = {}
      temp_staff_vs_salary = {}
      if temp_staff['pay_type'] == 'hourly':
        temp_staff_vs_hourly['name'] = temp_staff['first_name']
        temp_staff_vs_hourly['hourly_rate'] = temp_staff['pay_rate']
        staff_vs_hourly.append(temp_staff_vs_hourly)
      else:
        temp_staff_vs_salary['name'] = temp_staff['first_name']
        temp_staff_vs_salary['salary_rate'] = temp_staff['pay_rate']
        staff_vs_salary.append(temp_staff_vs_salary)
      if temp_staff['personal_gender'] is None:
        gender_unknown_count += 1
      else:
        if temp_staff['personal_gender'] == 'male':
          gender_male_count += 1
        elif temp_staff['personal_gender'] == 'female':
          gender_female_count += 1
        else:
          gender_other_count += 1
      if temp_staff['personal_race'] is None:
        race_unknown_count += 1
      else:
        if temp_staff['personal_race'] == 'caucasian':
          race_caucasian_count += 1
        elif temp_staff['personal_race'] == 'asian':
          race_asian_count += 1
        elif temp_staff['personal_race'] == 'black or african american':
          race_black_or_african_american_count += 1
        elif temp_staff['personal_race'] == 'native hawaiian or other pacific islander':
          race_native_hawaiian_or_other_pacific_islander_count += 1
        elif temp_staff['personal_race'] == 'american indian or alaskan native':
          race_american_indian_or_alaskan_native_count += 1
        else:
          race_hispanic_or_latino_count += 1

    unique_staffs = set(staffs)
    staff_count = len(unique_staffs)
    unique_employee_devices = set(employee_devices)
    employee_device_count = len(unique_employee_devices)
    unique_office_devices = set(office_devices)
    office_device_count = len(unique_office_devices)
    ret_total_staff_html = f'''
      {staff_count}
    '''
    jQuery("#id_firm_total_staff").empty().append(ret_total_staff_html)
    
    ret_employee_devices_html = f'''
      {employee_device_count}
    '''
    jQuery("#id_firm_employee_devices").empty().append(ret_employee_devices_html)
    
    ret_office_device_html = f'''
      {office_device_count}
    '''
    jQuery("#id_firm_office_devices").empty().append(ret_office_device_html)

    # staff vs hourly
    chart_staff_vs_hourly = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
        'labelStyle': {
                    'color': '#FFFFFF' 
        }
      },
      'primaryYAxis': {
        'minimum': 0, 'maximum': 550, 'interval': 50, 
        'labelStyle': {
          'color': '#FFFFFF' ,
          'padding': { 'right': 10 }
        },
        'labelFormat': '${value}', 
      },
      'series':[{
        'dataSource': staff_vs_hourly,
        'xName': 'name', 'yName': 'hourly_rate',
        'type': 'Column',
        'fill': '#FFFFFF'
      }],
      'isTransposed': True,
    }, "#id_firm_staff_vs_hourly")
    ret_firm_staff_vs_hourly_html = f'''
      {chart_staff_vs_hourly}
    '''
    jQuery("#id_firm_staff_vs_hourly").append(ret_firm_staff_vs_hourly_html)

    # staff vs salary
    chart_staff_vs_salary = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
      },
      'primaryYAxis': {
        'minimum': 0, 'maximum': 14000, 'interval': 2000, 'labelFormat': '${value}'
      },
      'series':[{
        'dataSource': staff_vs_salary,
        'xName': 'name', 'yName': 'salary_rate',
        'type': 'Column',
      }],
      'isTransposed': True,
    }, "#id_firm_staff_vs_salary")
    ret_firm_staff_vs_salary_html = f'''
      {chart_staff_vs_salary}
    '''
    jQuery("#id_firm_staff_vs_salary").append(ret_firm_staff_vs_salary_html)

    # Gender Demography
    chartData_firm_gender_demographics = [
      {'gender': 'unknown', 'count': gender_unknown_count},
      {'gender': 'male', 'count': gender_male_count},
      {'gender': 'female', 'count': gender_female_count},
      {'gender': 'other', 'count': gender_other_count},
    ]

    chart_firm_gender_demographics = ej.charts.AccumulationChart({
    'series': [
        {
          'dataSource': chartData_firm_gender_demographics,
          'innerRadius': '40%',
          'startAngle': 270,
          'endAngle': 90,
          'xName': 'gender',
          'yName': 'count'
        }
      ]
    }, '#id_firm_gender_demographics')
    ret_firm_gender_demographics_html = f'''
      {chart_firm_gender_demographics}
    '''
    jQuery("#id_firm_gender_demographics").append(ret_firm_gender_demographics_html)
    
    # Race Demography
    chartData_firm_race_demographics = [
      {'race': 'unknown', 'count': race_unknown_count},
      {'race': 'caucasian', 'count': race_caucasian_count},
      {'race': 'asian', 'count': race_asian_count},
      {'race': 'black or african american', 'count': race_black_or_african_american_count},
      {'race': 'native hawaiian or other pacific islander', 'count': race_native_hawaiian_or_other_pacific_islander_count},
      {'race': 'american indian or alaskan native', 'count': race_american_indian_or_alaskan_native_count},
      {'race': 'hispanic or latino', 'count': race_hispanic_or_latino_count},
    ]
    chart_firm_race_demographics = ej.charts.AccumulationChart({
      'series': [
        {
            'dataSource': chartData_firm_race_demographics, 
            'innerRadius': '40%',
            'xName': 'race',
            'yName': 'count'
        }
      ]
    }, '#id_firm_race_demographics')
    ret_firm_race_demographics_html = f'''
      {chart_firm_race_demographics}
    '''
    jQuery("#firm_race_demographics").append(ret_firm_race_demographics_html)
      
  def init_lead_tab(self):
    unknown_lead_source_count = 0
    email_count = 0
    google_message_count = 0
    phone_call_count = 0
    referral_count = 0
    website_form_count = 0
    yelp_count = 0
    unknown_lead_case_stage_open_count = 0
    unknown_lead_case_stage_won_count = 0
    unknown_lead_case_stage_lost_count = 0
    pre_charge_open_count = 0
    pre_charge_won_count = 0
    pre_charge_lost_count = 0
    lower_court_open_count = 0
    lower_court_won_count = 0
    lower_court_lost_count = 0
    upper_court_open_count = 0
    upper_court_won_count = 0
    upper_court_lost_count = 0
    appeals_court_open_count = 0
    appeals_court_won_count = 0
    appeals_court_lost_count = 0
    total_won_lead = 0
    total_lost_lead = 0
    total_open_lead = 0
    total_value_of_won_lead = 0
    total_value_of_lost_lead = 0
    total_value_of_open_lead = 0
    total_won_rate = 0
    lost_reason_battery_count = 0
    lost_reason_bigamy_count = 0
    lost_reason_murder_first_degree_count = 0
    lost_reason_kidnapping_count = 0
    unknown_case_stage_open_value = 0
    pre_charge_open_value = 0
    lower_court_open_value = 0
    upper_court_open_value = 0
    appeals_court_open_value = 0
    all_leads = Lead.search()
    value_of_won_vs_lost = []
    for temp_lead in all_leads:
      temp_value_of_won_vs_lost = {}
      formatted_date = temp_lead['updated_time'].strftime("%m/%Y")
      temp_value_of_won_vs_lost['date'] = formatted_date
      if temp_lead['lead_status'] == 'Won':
        if temp_lead['retainer'] is not None:
          temp_value_of_won_vs_lost['won_value'] = temp_lead['retainer']
        else:
          temp_value_of_won_vs_lost['won_value'] = 0
        temp_value_of_won_vs_lost['lost_value'] = 0
      elif temp_lead['lead_status'] == 'Lost':
        if temp_lead['retainer'] is not None:
          temp_value_of_won_vs_lost['lost_value'] = temp_lead['retainer']
        else:
          temp_value_of_won_vs_lost['lost_value'] = 0
        temp_value_of_won_vs_lost['won_value'] = 0
      else:
        temp_value_of_won_vs_lost['won_value'] = 0
        temp_value_of_won_vs_lost['lost_value'] = 0
      found = False
      for item in value_of_won_vs_lost:
        if item['date'] == temp_value_of_won_vs_lost['date']:
          item['won_value'] += temp_value_of_won_vs_lost['won_value']
          item['lost_value'] += temp_value_of_won_vs_lost['lost_value']
          found = True
          break
      if not found:
        value_of_won_vs_lost.append(temp_value_of_won_vs_lost)  
        
      if temp_lead['lead_source'] is None:
        unknown_lead_source_count += 1
      elif temp_lead['lead_source'].name == 'Email':
        email_count += 1
      elif temp_lead['lead_source'].name == 'Google Messages':
        google_message_count += 1
      elif temp_lead['lead_source'].name == 'Phone Call':
        phone_call_count += 1
      elif temp_lead['lead_source'].name == 'Referral':
        referral_count += 1
      elif temp_lead['lead_source'].name == 'Website Form':
        website_form_count += 1
      else:
        yelp_count += 1
      if temp_lead['case_stage'] is None:
        if temp_lead['lead_status'] == 'Open':
          unknown_lead_case_stage_open_count += 1
          if temp_lead['retainer'] is not None:
            unknown_case_stage_open_value += temp_lead['retainer']
        elif temp_lead['lead_status'] == 'Won':
          unknown_lead_case_stage_won_count += 1
        else:
          unknown_lead_case_stage_lost_count += 1
      elif temp_lead['case_stage'].name == 'Pre-Charge':
        if temp_lead['lead_status'] == 'Open':
          pre_charge_open_count += 1
          if temp_lead['retainer'] is not None:
            pre_charge_open_value += temp_lead['retainer']
        elif temp_lead['lead_status'] == 'Won':
          pre_charge_won_count += 1
        else:
          pre_charge_lost_count += 1
      elif temp_lead['case_stage'].name == 'Lower Court':
        if temp_lead['lead_status'] == 'Open':
          lower_court_open_count += 1
          if temp_lead['retainer'] is not None:
            lower_court_open_value += temp_lead['retainer']
        elif temp_lead['lead_status'] == 'Won':
          lower_court_won_count += 1
        else:
          lower_court_lost_count += 1
      elif temp_lead['case_stage'].name == 'Upper Court':
        if temp_lead['lead_status'] == 'Open':
          upper_court_open_count += 1
          if temp_lead['retainer'] is not None:
            upper_court_open_value += temp_lead['retainer']
        elif temp_lead['lead_status'] == 'Won':
          upper_court_won_count += 1
        else:
          upper_court_lost_count += 1
      else:
        if temp_lead['lead_status'] == 'Open':
          appeals_court_open_count += 1
          appeals_court_open_value += temp_lead['retainer']
        elif temp_lead['lead_status'] == 'Won':
          appeals_court_won_count += 1
        else:
          appeals_court_lost_count += 1
      if temp_lead['lead_status'] == 'Won':
        if temp_lead['retainer'] is not None:
          total_value_of_won_lead += temp_lead['retainer']
        total_won_lead += 1
      elif temp_lead['lead_status'] == 'Lost':
        if temp_lead['cause_of_action'] is not None:
          for temp in temp_lead['cause_of_action']:
            if temp.cause_of_action == 'Battery':
              lost_reason_battery_count += 1
            elif temp.cause_of_action == 'Bigamy':
              lost_reason_bigamy_count += 1
            elif temp.cause_of_action == 'Murder, first degree':
              lost_reason_murder_first_degree_count += 1
            else:
              lost_reason_kidnapping_count += 1
            print(temp.cause_of_action)
        total_lost_lead += 1
        if temp_lead['retainer'] is not None:
          total_value_of_lost_lead += temp_lead['retainer']
      else:
        total_open_lead += 1
        if temp_lead['retainer'] is not None:
          total_value_of_open_lead += temp_lead['retainer']
    value_of_won_vs_lost_list = [item for item in value_of_won_vs_lost if not (item['won_value'] == 0 and item['lost_value'] == 0)]
    
    total_won_rate = float(total_won_lead / (total_won_lead + total_lost_lead)) * 100
    formatted_total_won_rate = "{:.2f}".format(total_won_rate)
    avg_value_of_won_lead = float(total_value_of_won_lead / total_won_lead)
    formatted_avg_value_of_won_lead = "{:.2f}".format(avg_value_of_won_lead)
    avg_value_of_lost_lead = float(total_value_of_lost_lead / total_lost_lead)
    formatted_avg_value_of_lost_lead = "{:.2f}".format(avg_value_of_lost_lead)
    avg_value_of_open_lead = float(total_value_of_open_lead / total_open_lead)
    formatted_avg_value_of_open_lead = "{:.2f}".format(avg_value_of_open_lead)
        
    # Average Value of Won, Lost and Open Leads
    ret_avg_value_of_won_lead_html = f'''
      $ {formatted_avg_value_of_won_lead}
    '''
    jQuery("#id_lead_average_value_of_won_leads").empty().append(ret_avg_value_of_won_lead_html)
    
    ret_avg_value_of_lost_lead_html = f'''
      $ {formatted_avg_value_of_lost_lead}
    '''
    jQuery("#id_lead_average_value_of_lost_leads").empty().append(ret_avg_value_of_lost_lead_html)
    
    ret_avg_value_of_open_lead_html = f'''
      $ {formatted_avg_value_of_open_lead}
    '''
    jQuery("#id_lead_average_value_of_open_leads").empty().append(ret_avg_value_of_open_lead_html)

    # Open Deals by Stage
    chartdata_open_deal_value = [
      {'name': 'Unknown', 'value': unknown_case_stage_open_value},
      {'name': 'Pre-Charge', 'value': pre_charge_open_value},
      {'name': 'Lower Court', 'value': lower_court_open_value},
      {'name': 'Upper Court', 'value': upper_court_open_value},
      {'name': 'Appeals Court', 'value': appeals_court_open_value},
    ]
    chart_open_deal_value = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
      },
      'primaryYAxis': {
      },
      'series':[{
        'dataSource': chartdata_open_deal_value,
        'xName': 'name', 'yName': 'value',
        'type': 'Column',
      }],
      # 'isTransposed': True,
    }, "#id_lead_open_deals_by_stage")
    ret_lead_open_deals_by_stage_html = f'''
      {chart_open_deal_value}
    '''
    jQuery("#id_lead_open_deals_by_stage").append(ret_lead_open_deals_by_stage_html)
    
    # Won vs Lost by Stage
    chartdata_lead_by_case_stage = [
      {'stagename': 'Unknown', 'woncount': unknown_lead_case_stage_won_count, 'lostcount': unknown_lead_case_stage_lost_count},
      {'stagename': 'Pre-Charge', 'woncount': pre_charge_won_count, 'lostcount': pre_charge_lost_count},
      {'stagename': 'Lower Court', 'woncount': lower_court_won_count, 'lostcount': lower_court_lost_count},
      {'stagename': 'Upper Court', 'woncount': upper_court_won_count, 'lostcount': upper_court_lost_count},
      {'stagename': 'Appeals Court', 'woncount': appeals_court_won_count, 'lostcount': appeals_court_lost_count}
    ]
    
    chart_lead_by_stage = ej.charts.Chart({
      'width': '450',
      'primaryXAxis': {
        'valueType': 'Category',
        # // label placement as on ticks
        'labelPlacement': 'OnTicks',
        # 'title': 'Case Stage'
      },
      'primaryYAxis': {
        'minimum': 0, 'maximum': 5, 'interval': 1,
        # 'title': 'Count'
      },
      'series': [
        {'dataSource': chartdata_lead_by_case_stage, 'xName': 'stagename', 'yName': 'woncount', 'name': 'Won', 'type': 'Column'},
        {'dataSource': chartdata_lead_by_case_stage, 'xName': 'stagename', 'yName': 'lostcount', 'name': 'Lost', 'type': 'Column'}
      ],
    }, '#id_lead_conversion_by_stage')
    
    ret_lead_lead_by_stage_html = f'''
      {chart_lead_by_stage}
    '''
    jQuery("#id_lead_conversion_by_stage").append(ret_lead_lead_by_stage_html)

    # Lead Source
    chartdata_lead_source = [
      {'name': 'Unknown', 'count': unknown_lead_source_count},
      {'name': 'Email', 'count': email_count},
      {'name': 'Google Messages', 'count': google_message_count},
      {'name': 'Phone Call', 'count': phone_call_count},
      {'name': 'Referral', 'count': referral_count},
      {'name': 'Website Form', 'count': website_form_count},
      {'name': 'Yelp', 'count': yelp_count},
    ]
    chart_lead_source = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
      },
      'primaryYAxis': {
        'minimum': 0, 'maximum': 10, 'interval': 1
      },
      'series':[{
        'dataSource': chartdata_lead_source,
        'xName': 'name', 'yName': 'count',
        'type': 'Column',
      }],
      'isTransposed': True,
    }, "#id_lead_lead_source_vs_status")
    ret_lead_lead_source_vs_status_html = f'''
      {chart_lead_source}
    '''
    jQuery("#id_lead_lead_source_vs_status").append(ret_lead_lead_source_vs_status_html)

    # Total Won and Lost
    ret_total_won_lead_html = f'''
      {total_won_lead}
    '''
    jQuery("#id_lead_total_won_lead").append(ret_total_won_lead_html)

    ret_lead_total_lost_lead_html = f'''
      {total_lost_lead}
    '''
    jQuery("#id_lead_total_lost_lead").append(ret_lead_total_lost_lead_html)

    # Conversion Rate
    circularGauge_won_rate = ej.circulargauge.CircularGauge({
      'height': '170',
      'background': 'transparent',
      'legendSettings':{
        'visible':False
      },
      'axes': [{
        'annotations': [{
            'angle': 165,
            'radius': '45%',
            'zIndex':'1',
            'content':
                  f'<div style="font-size:14px;margin-left: -10px;margin-top: -12px; color:#00FF00">{formatted_total_won_rate}%</div>',
        }],
        'lineStyle': { 'width': 10, 'color': 'transparent' },
        'labelStyle': {
          'position': 'Outside', 
          'useRangeColor': False,
          'offset': -10,
          'font': { 
            'size': '12px', 
            'color': '#00FF00', 
            'fontFamily': 'Roboto', 
            'fontStyle': 'Regular' 
          }
        }, 
        'majorTicks': { 
            'height': 7, 
            'color': '#9E9E9E' 
        }, 
        'minorTicks': { 'height': 0 },
        'startAngle': 270, 
        'endAngle': 90, 
        'minimum': 0, 
        'maximum': 100, 
        'radius': '90',
        'ranges': [{ 
            'start': 0, 
            'end': formatted_total_won_rate, 
            'startWidth': 17,
            'endWidth': 17,
            'color': '#30B32D' 
        }, 
        { 
            'start': formatted_total_won_rate, 
            'end': 100, 
            'startWidth': 17,
            'endWidth': 17,
            'color': '#FFDD00' 
        }],
        'pointers': [{
            'animation': { 'enable': False },
            'value': formatted_total_won_rate, 
            'radius': '60%', 
            'color': '#757575', 
            'pointerWidth': 8,
            'cap': { 
                'radius': 7, 
                'color': '#757575' 
            }, 
            'needleTail': { 
                'length': '18%' 
            }
        }]
      }]
    }, "#id_lead_won_rate");
    ret_won_rate_html = f'''
      {circularGauge_won_rate}
    '''
    jQuery("#id_lead_won_rate").append(ret_won_rate_html)

    # Lost Reasons
    chartData_lead_lost_reasons = [
      {'reason': 'Battery', 'count': lost_reason_battery_count},
      {'reason': 'Bigamy', 'count': lost_reason_bigamy_count},
      {'reason': 'Murder, first degree', 'count': lost_reason_murder_first_degree_count},
      {'reason': 'Kidnapping, first degree, no substantial bodily harm', 'count': lost_reason_kidnapping_count},
    ]
    chart_lead_lost_reasons = ej.charts.AccumulationChart({
      'series': [
        {
            'dataSource': chartData_lead_lost_reasons, 
            'innerRadius': '0%',
            'xName': 'reason',
            'yName': 'count'
        }
      ]
    }, '#id_lead_lost_reasons')
    ret_lead_lost_reasons_html = f'''
      {chart_lead_lost_reasons}
    '''
    jQuery("#id_lead_lost_reasons").append(ret_lead_lost_reasons_html)

    # Value of Deals Won vs Lost
    
    chart_lead_value_of_deals_won_vs_lost = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
      },
      'primaryYAxis': {},
      'series':[
        {
            'type': 'StackingColumn',
            'dataSource': value_of_won_vs_lost_list,
            'xName': 'date',
            'yName': 'won_value',
            'name': 'Won',
            'fill': '#00FF00'
        },
        {
            'type': 'StackingColumn',
            'dataSource': value_of_won_vs_lost_list,
            'xName': 'date',
            'yName': 'lost_value',
            'name': 'Lost',
            'fill': '#00FFAE'
        }
      ],
      'tooltip': { 'enable': True },
      'legend': { 'visible': True }
    }, "#id_lead_value_of_deals_won_vs_lost")
    ret_lead_value_of_deals_won_vs_lost_html = f'''
      {chart_lead_value_of_deals_won_vs_lost}
    '''
    jQuery("#id_lead_value_of_deals_won_vs_lost").append(ret_lead_value_of_deals_won_vs_lost_html)
  
  def init_staff_tab(self):
    # Currend Pay Period
    base_pay_period_start = datetime.datetime(year=2024, month=4, day=8)
    current_date = datetime.date.today()
    days_since_start = (current_date - base_pay_period_start).days
    weeks_since_start = days_since_start // 7
    flag = weeks_since_start % 2
    if flag:
        current_pay_period_start = base_pay_period_start + timedelta(weeks=weeks_since_start - 1)
    else:
        current_pay_period_start = base_pay_period_start + timedelta(weeks=weeks_since_start)
    current_pay_period_end = current_pay_period_start + timedelta(days=13)
    print(current_pay_period_end)
    current_pay_period = current_pay_period_start.strftime("%m/%d/%Y") + " - " + current_pay_period_end.strftime("%m/%d/%Y")
    ret_staff_current_pay_period_html = f'''
      {current_pay_period}
    '''
    jQuery("#id_staff_current_pay_period").append(ret_staff_current_pay_period_html)
    # Current Period Payroll
    logged_user = User.get(AppEnv.logged_user.get('user_uid'))
    logged_staff = Staff.search(user=logged_user)
    all_timesheets = Timesheet.search()
    all_performanceincentives = PerformanceIncentive.search()
    current_period_payroll = 0
    overtime_hours = 0
    incentives = 0
    overtime_pay = 0
    total_bonus = 0
    total_hours_worked = 0
    previous_period_payroll = 0
    previous_total_work_hours = 0
    for staff in logged_staff:
      for temp_timesheet in all_timesheets:
        date = temp_timesheet['clock_out_time']
        if staff['first_name'] == temp_timesheet['staff'].first_name:
          if current_pay_period_start <= date <= current_pay_period_end:
            current_period_payroll += temp_timesheet['payroll']
            overtime_hours += temp_timesheet['hours_worked'] - 8
            total_hours_worked += temp_timesheet['hours_worked']
          if current_pay_period_start - 14 <= date <= current_pay_period_end - 14:
            previous_total_work_hours += temp_timesheet['hours_worked']
            previous_period_payroll += temp_timesheet['payroll']
      for temp_performanceincentive in all_performanceincentives:
        date = temp_performanceincentive['payment_date']
        if staff['first_name'] == temp_performanceincentive['staff'].first_name:
          if date is not None and current_pay_period_start <= date <= current_pay_period_end:
            incentives += temp_performanceincentive['amount']
      overtime_pay = overtime_hours * staff['overtime_rate']
    formatted_current_period_payroll = "{:.2f}".format(current_period_payroll)
    formatted_incentive = "{:.2f}".format(incentives)
    formatted_overtime_pay = "{:.2f}".format(overtime_pay)
    formatted_total_bonus = "{:.2f}".format(total_bonus)
    ret_current_period_payroll_html = f'''
      {formatted_current_period_payroll}
    '''
    jQuery("#id_staff_current_period_payroll").append(ret_current_period_payroll_html)
    ret_total_bonus_html = f'''
      $ {formatted_total_bonus}
    '''
    jQuery("#id_staff_total_bonus").empty().append(ret_total_bonus_html)
    ret_overtime_hours_html = f'''
      {overtime_hours}
    '''
    jQuery("#id_staff_overtime_hours").append(ret_overtime_hours_html)
    ret_total_hours_worked_html = f'''
      {total_hours_worked}
    '''
    jQuery("#id_staff_total_hours_worked").append(ret_total_hours_worked_html)
    ret_incentives_html = f'''
      $ {formatted_incentive}
    '''
    jQuery("#id_staff_incentives").empty().append(ret_incentives_html)
    ret_overtime_pay_html = f'''
      $ {formatted_overtime_pay}
    '''
    jQuery("#id_staff_overtime_pay").empty().append(ret_overtime_pay_html)

    total_work_hours_current_vs_previous = [
      {'period': 'Current', 'hours': total_hours_worked},
      {'period': 'Previous', 'hours': previous_total_work_hours}
    ]
    total_payroll_current_vs_previous = [
      {'period': 'Current', 'payroll': current_period_payroll},
      {'period': 'Previous', 'payroll': previous_period_payroll}
    ]
    # Work Hours
    chart_work_hours_current_vs_previous = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
        'labelStyle': {
                    'color': '#FFFFFF' 
        }
      },
      'primaryYAxis': {
        'labelStyle': {
                    'color': '#FFFFFF' 
        }
      },
      'series':[{
        'dataSource': total_work_hours_current_vs_previous,
        'xName': 'period', 'yName': 'hours',
        'type': 'Column',
        'width': 40
      }],
      'isTransposed': True,
    }, "#id_staff_work_hours_current_vs_previous")
    ret_work_hours_current_vs_previous_html = f'''
      {chart_work_hours_current_vs_previous}
    '''
    jQuery("#id_staff_work_hours_current_vs_previous").append(ret_work_hours_current_vs_previous_html)
    # Total Payroll
    chart_total_payroll_current_vs_previous = ej.charts.Chart({
      'primaryXAxis': {
        'valueType': 'Category',
      },
      'primaryYAxis': {},
      'series':[{
        'dataSource': total_payroll_current_vs_previous,
        'xName': 'period', 'yName': 'hours',
        'type': 'Column',
        'width': 40
      }],
      'isTransposed': True,
    }, "#id_staff_payroll_current_vs_previous")
    ret_total_payroll_current_vs_previous_html = f'''
      {chart_total_payroll_current_vs_previous}
    '''
    jQuery("#id_staff_payroll_current_vs_previous").append(ret_total_payroll_current_vs_previous_html)
  
  def destroy(self):
    if self.container_el:
      self.container_el.innerHTML = ''