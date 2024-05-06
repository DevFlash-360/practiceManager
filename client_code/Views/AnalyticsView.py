import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta, datetime

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *

from ..app.models import Staff, User, Contact, Activity, AppAuditLog, TimeEntry, Expense, Case, Task, Event, Payment, Lead, Client

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
        <div class="col-xs-12" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem">Time vs Staff this Month</div>
        <div class="col-xs-5" style="align-items: center; margin-bottom: 15px; display: flex; padding-top:15px">
          <div id="id_total_time"></div>
        </div>
        <div class="col-xs-10" style="align-items: center; background-color: white; margin-bottom: 15px; display: flex;">
          <div id="id_case_time"></div>
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
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem">Cases by Stage</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px; font-size: 1.8rem">Cases by Practice Area</div>
        <div class="col-xs-6" style="align-items: center;  padding-right: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_case_cases_by_stage"></div>
        </div>
        <div class="col-xs-6" style="align-items: center;  padding-left: 7px; margin-bottom: 15px">
          <div style="background-color: white;" id="id_case_cases_by_pracetice_area"></div>
        </div>
      </div>
      <div class ="col-xs-5" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center; margin-top: 10px; padding: 7px; font-size: 2rem; background-color: rgb(245, 245, 245)">Contacts Map</div>
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
        <div class="col-xs-12" style="align-items: center;  padding: 8px; font-size: 1.8rem">Payroll & Expenses</div>
        <div class="col-xs-6" style="align-items: center; padding: 8px; padding-top: 0px">
          <div class="p-3" style="padding: 5px; background-color: white; difsplay: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center; justify-content:center;">
              <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Current Period Payroll</span>
                <div id="id_finance_current_period_payroll" style="font-weight: bold; font-size: 1.4em;">$ </div>
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
                <div id="id_finance_firm_expenses_this_month" style="font-weight: bold; font-size: 1.4em;">$ </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center;  padding: 8px; font-size: 1.8rem">Revenue Snapshot</div>
        <div class="col-xs-4" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); display: flex; align-items:center; justify-content: center; color: white;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center">This Month</span>
                <div id="id_finance_this_month_revenue" style="text-align: center; font-weight: bold; font-size: 1.4em">$ 0.00</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-4" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Same Month Last Year</span>
                <div id="id_finance_same_month_last_year_revenue" style="text-align: center; font-weight: bold; font-size: 1.4em; color: #333">$ 0.00</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-xs-4" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Last Month</span>
                <div id="id_finance_last_month" style="text-align: center; font-weight: bold; font-size: 1.4em; color: #333">$ 0.00</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Current Month Projection</span>
                <div id="id_finance_current_month_projection" style="text-align: center; font-weight: bold; font-size: 1.4em;">$ 0.00</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Average Daily Revenur</span>
                <div id="id_finance_average_daily_revenue" style="text-align: center; font-weight: bold; font-size: 1.4em;">$ 0.00</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center;  padding-right: 8px; font-size: 1.8rem">Current Month Stats</div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Total Referals</span>
                <div id="id_finance_total_referrals" style="text-align: center; font-weight: bold; font-size: 1.4em;">69</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Firm Expenses this Month</span>
                <div id="id_finance_total_minus_referrals" style="text-align: center; font-weight: bold; font-size: 1.4em;">0</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">New Clients this Month</span>
                <div id="id_finance_new_clients_this_month" style="text-align: center; font-weight: bold; font-size: 1.4em;">0</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Existing Clients this Month</span>
                <div id="id_finance_existing_clients_this_month" style="text-align: center; font-weight: bold; font-size: 1.4em;">0</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class ="col-xs-4" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center; padding: 8px; font-size: 1.8rem;">Staff Incentives Report</div>
        <div class="col-xs-12" style="align-items: center; background-color: white; margin-bottom: 15px; display: flex;">
          <div class="col-xs-8" style="align-items: center; margin-bottom: 15px; display: flex; padding-top:15px">
            <div id="id_finance_period"></div>
          </div>
          <div class="col-xs-8" style="align-items: center; background-color: white; margin-bottom: 15px;">
            <div id="id_finance_staff_incentives_report"></div>
          </div>
        </div>
      </div>
    </div>
    <div class ="col-xs-12" style="justify-content: center; padding: 0px;">
      <div class="col-xs-6" style="align-items: center;  padding: 8px; padding-top: 2px; font-size: 1.8rem">Current Month Revenue by Day</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; padding-top: 2px; font-size: 1.8rem">Revenue by Month</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; padding-top: 2px">
        <div style="background-color: white;" id="id_finance_current_month_revenue_by_day">Current Month Revenue by Day</div>
      </div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; padding-top: 2px">
        <div style="background-color: white;" id="id_finance_revenue_by_month">Revenue by Month</div>
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
      <div class="col-xs-6" style="align-items: center;  padding: 8px; font-size: 1.8rem; margin-bottom: 4px">Staff vs Hourly</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; font-size: 1.8rem; margin-bottom: 4px">Staff vs Salary</div>
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
      <div class="col-xs-6" style="align-items: center;  padding: 8px; margin-bottom: 4px; font-size: 1.8rem">Gender Demographics</div>
      <div class="col-xs-6" style="align-items: center;  padding: 8px; margin-bottom: 4px; font-size: 1.8rem">Race Demographics</div>
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
      <div class ="col-xs-6" style="justify-content: center; padding: 0px; padding-top: 34px">
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); color: white; difsplay: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center; justify-content:center;">
              <i class="fa-thin fa-money-check-dollar-pen" aria-hidden="true" style="margin-right: 8px; font-size: 2em;"></i>
              <div>
                <span style="margin-right: 4px">Average Value of Open Leads</span>
                <div id="id_lead_average_value_of_open_leads" style="font-weight: bold; font-size: 1.4em;">$ </div>
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
                <div id="id_lead_average_value_of_won_leads" style="font-weight: bold; font-size: 1.4em;">$ </div>
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
                <div id="id_average_value_of_lost_leads" style="font-weight: bold; font-size: 1.4em;">$</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class ="col-xs-6" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center;  padding: 8px; font-size: 1.8rem;">Oepn Deals by Stage</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px; padding-top: 0px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 206px">
            <div style="color: white" id="id_lead_open_deals_by_stage"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-8" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center;  padding-left: 8px; font-size: 1.8rem;">Lead Source vs Status</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 400px">
            <div id="id_lead_lead_source_vs_status"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-4" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center;  padding-left: 8px; font-size: 1.8rem;">Conversion Rate</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: rgb(39, 45, 131); color: white; sdisplay: flex; align-items:center; justify-content: center; height: 180px">
            <div style="color: white" id="id_lead_conversion_rate"></div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center;  padding-left: 8px; font-size: 1.8rem;">Conversions by Stage</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
            <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 180px">
            <div id="id_lead_conversions_by_stage"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-4" style="justify-content: center; padding: 0px; padding-top: 26px">
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Total Won Leads</span>
                <div id="id_finance_existing_clients_this_month" style="text-align: center; font-weight: bold; font-size: 1.4em;">0</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-6" style="align-items: center; padding: 8px">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center;">
            <div style="display:flex; align-items:center;">
              <div>
                <span style="text-align: center;">Total Lost Leads</span>
                <div id="id_finance_existing_clients_this_month" style="text-align: center; font-weight: bold; font-size: 1.4em;">0</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xs-12" style="align-items: center;  padding-left: 8px; font-size: 1.8rem;">Lost Reasons</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 260px">
            <div id="id_lead_lost_reasons"></div>
          </div>
        </div>
      </div>
      <div class ="col-xs-8" style="justify-content: center; padding: 0px;">
        <div class="col-xs-12" style="align-items: center;  padding-left: 8px; font-size: 1.8rem;">Value of Deals Won vs Lost</div>
        <div class="col-xs-12" style="align-items: center; padding: 8px;">
          <div class="p-3" style="padding: 5px; background-color: white; display: flex; align-items:center; justify-content: center; height: 360px">
            <div id="id_lead_value_of_deals_won_vs_lost"></div>
          </div>
        </div>
      </div>
    </div>
    '''
      
    return ret_html


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
    elif selected_index == 5 and not self.staffTabInitialized:
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
    # dropdown_period = ej.dropdowns.DropDownList({
    #   'dataSource': PM_AV_PERIOD,
    #   'placeholder': "Select a Period",
    #   'value': "This Month",
    # }, "#id_total_time")
    
    # dropdown_period.addEventListener('change', self.dropdown_period_change)

    # # append time entry data to init_time_entry_activity list
    # all_time_entries = TimeEntry.search()
    # for time_entries in all_time_entries:
    #   new_timeentry_activity = {}
    #   if time_entries['activity'] is not None:
    #     new_timeentry_activity['date'] = time_entries['date']
    #     new_timeentry_activity['activity'] = time_entries['activity'].name
    #     new_timeentry_activity['timeentry'] = time_entries['duration']
    #     if time_entries['case'] is not None:
    #       new_timeentry_activity['case'] = time_entries['case'].case_name
    #     else:
    #       new_timeentry_activity['case'] = None
    #     init_time_entry_activity.append(new_timeentry_activity)
    # # append expenses data to the init_expenses list
    # all_Expenses = Expense.search()
    # for Expenses in all_Expenses:
    #   new_expenses = {}
    #   new_expenses['date'] = Expenses['date']
    #   new_expenses['total'] = Expenses['total']
    #   init_expenses.append(new_expenses)
    # # append staff and time data to the init_time_staff
    # all_staff_time = Staff.search()
    # for staff_time in all_staff_time:
    #   new_staff_time = {}
    #   new_staff_time['name'] = staff_time['first_name']
    #   new_staff_time['time'] = staff_time['intake_performance_incentive']
    #   init_time_staff.append(new_staff_time)
    # # append case and timeentry data to the init_case_timeentry
    # all_cases = Case.search()
    # for cases in all_cases:
    #   new_case = {}
    #   total_period = 0
    #   new_case['date'] = cases['incident_date']
    #   new_case['case'] = cases['case_name']
    #   for casetimeentry in init_time_entry_activity:
    #     if casetimeentry['case'] == cases['case_name']:
    #       if casetimeentry['timeentry'] is not None:
    #         total_period += casetimeentry['timeentry']
    #       else:
    #         total_period += 0
    #   new_case['total_period'] = total_period
    #   init_case_timeentry.append(new_case)
    
    # # initialize billing page
    # total_time_entry = 0
    # time_entry_activity = []
    # for time_entries in init_time_entry_activity:
    #   new_timeentry_activity = {}
    #   date = time_entries['date']
    #   current_date = datetime.date.today()
    #   if date.year == current_date.year and date.month == current_date.month:
    #     total_time_entry += time_entries['timeentry']
    #     new_timeentry_activity['activity'] = time_entries['activity']
    #     new_timeentry_activity['timeentry'] = time_entries['timeentry']
    #     time_entry_activity.append(new_timeentry_activity)
    # time_entry = float(total_time_entry)
    # formatted_time_entry = "{:.2f}".format(time_entry)
    # ret_time_entry_html = f'''
    #   {formatted_time_entry}
    # '''
    # jQuery("#id_time_entry").empty().append(ret_time_entry_html)

    # Case_Expenses = 0
    # for Expenses in init_expenses:
    #   date = Expenses['date']
    #   current_date = datetime.date.today()
    #   if date.year == current_date.year and date.month == current_date.month:
    #     Case_Expenses += Expenses['total']
    # Case_Expense = float(Case_Expenses)
    # formatted_Case_Expense = "{:.2f}".format(Case_Expense)
    # ret_case_expense_html = f'''
    #   $ {formatted_Case_Expense}
    # '''
    # jQuery("#id_case_expense").append(ret_case_expense_html)
    
    # chartData_time_staff = []
    # for staff_time in init_time_staff:
    #   new_staff_time = {}
    #   new_staff_time['name'] = staff_time['name']
    #   new_staff_time['time'] = staff_time['time']
    #   chartData_time_staff.append(new_staff_time)
    # print(chartData_time_staff)
    # chart_time_staff = ej.charts.Chart({
    #   'primaryXAxis': {
    #       'valueType': 'Category'
    #   },
    #   'primaryYAxis': {
    #       'minimum': 0, 'maximum': 0.1, 'interval': 0.02
    #   },
    #   'series':[{
    #       'dataSource': chartData_time_staff,
    #       'xName': 'name', 'yName': 'time',
    #       'type': 'Column'
    #   }],
    #   # 'isTransposed': True,
    # }, '#id_time_staff')
    # ret_time_staff_html = f'''
    #   {chart_time_staff}
    # '''
    # jQuery("#id_time_staff").append(ret_time_staff_html)
    
    # chartData_time_activity = []
    # for temp_timeentry_activity in time_entry_activity:
    #   new_time_activity = {}
    #   new_time_activity['timeentry'] = temp_timeentry_activity['timeentry']
    #   new_time_activity['activity'] = temp_timeentry_activity['activity']
    #   chartData_time_activity.append(new_time_activity)
    # chart_time_activity = ej.charts.AccumulationChart({
    #   'series': [
    #     {
    #         'dataSource': chartData_time_activity, 
    #         'innerRadius': '40%',
    #         'xName': 'time_entry',
    #         'yName': 'activity'
    #     }
    #   ]
    # }, '#id_time_activity')
    # ret_time_activity_html = f'''
    #   {chart_time_activity}
    # '''
    # jQuery("#id_time_activity").append(ret_time_activity_html)
    
    # Case_Timeentry = [{'case': 'Case', 'total_period':'Period Total'}]
    # for cases in init_case_timeentry:
    #   new_case = {}
    #   date = cases['date']
    #   current_date = datetime.date.today()
    #   if date.year == current_date.year and date.month == current_date.month:
    #     new_case['case'] = cases['case']
    #     new_case['total_period'] = cases['total_period']
    #     Case_Timeentry.append(new_case)
    
    # ret_case_time_html = ""
    # ret_case_time_html += """<table style="width: 100%;border-collapse: collapse;table-layout: fixed;">"""
    # for item in Case_Timeentry:
    #   if item['case'] == "Case":
    #     ret_case_time_html += '''<colgroup><col span="1" style="width:80%"><col span="1" style="width:20%"></colgroup>'''
    #     ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">'''+item['case'] + '''</th><th style="border: 1px solid #dddddd; background-color: #f2f2f2; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</th></tr>"
    #   else:
    #     ret_case_time_html += '''<tr style="border: 1px solid #dddddd; text-align: left; padding: 8px;"><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">'''+item['case'] + '''</td><td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">''' + str(item['total_period']) + "</td></tr>"
    # ret_case_time_html += "</table>"
    # jQuery("#id_case_time").append(ret_case_time_html)

    # <div class="col-xs-12">{activity['address']}</div>
    pass
  
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
    jQuery("#id_case_open_cases").append(ret_open_cases_html)
    # Closed Cases
    ret_closed_cases_html = f'''
      {closed_case_count}
    '''
    jQuery("#id_case_closed_cases").append(ret_closed_cases_html)
    # Total Clients
    ret_total_clients_html = f'''
      {len(unique_total_client_count)}
    '''
    jQuery("#id_case_total_clients").append(ret_total_clients_html)

    # Open Tasks
    ret_open_tasks_html = f'''
      {open_task_count}
    '''
    jQuery("#id_case_open_tasks").append(ret_open_tasks_html)
    
    ret_open_total_staff_html = f'''
      {staff_count}
    '''
    jQuery("#id_case_total_staffs").append(ret_open_total_staff_html)
    
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
    all_payments = Payment.search()
    total_payroll = 0
    for temp_payments in all_payments:
      date = temp_payments['payment_time']
      current_date = datetime.date.today()
      print("payroll  ", date.year)
      if date.year == current_date.year and date.month == current_date.month:
        total_payroll += temp_payments['amount']
    float_total_payroll = float(total_payroll)
    formatted_total_payroll = "{:.2f}".format(float_total_payroll)
    ret_current_period_payroll_html = f'''
      {formatted_total_payroll}
    '''
    jQuery("#id_finance_current_period_payroll").empty().append(ret_current_period_payroll_html)

    # Firm Expenses this Month
    all_expenses = Expense.search()
    total_expenses_this_month = 0
    for temp_expenses in all_expenses:
      date = temp_expenses['date']
      current_date = datetime.date.today()
      print("expenses  ", date.year)
      if date.year == current_date.year and date.month == current_date.month:
        total_expenses_this_month += temp_expenses['total']
    float_total_expenses_this_month = float(total_expenses_this_month)
    formatted_total_expenses = "{:.2f}".format(float_total_expenses_this_month)
    ret_total_expenses_this_month_html = f'''
      {formatted_total_expenses}
    '''
    jQuery("#id_finance_firm_expenses_this_month").empty().append(ret_total_expenses_this_month_html)

    # Revenue Snapshot this month

    # Total Referrals
    all_leads = Lead.search()
    total_referrals_count = 0
    total_minus_referrals_count = 0
    for temp_leads in all_leads:
      date = temp_leads['incident_date']
      current_date = datetime.date.today()
      if date is not None:
        if date.year == current_date.year and date.month == current_date.month:
          if len(temp_leads['referred_by']) == 0:
            total_minus_referrals_count += 1
          else:
            total_referrals_count += 1
    ret_total_referrals__html = f'''
      {total_referrals_count}
    '''
    jQuery("#id_finance_total_referrals").empty().append(ret_total_referrals__html)    
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
    jQuery("#id_finance_new_clients_this_month").append(ret_new_clients_html)
    ret_exist_clients_html = f'''
      {exist_clients_count}
    '''
    jQuery("#id_finance_existing_clients_this_month").append(ret_exist_clients_html)



  def dropdown_finance_staff_incentives_report_period_change(self, args):
    pass
  
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
    jQuery("#id_firm_total_staff").append(ret_total_staff_html)
    
    ret_employee_devices_html = f'''
      {employee_device_count}
    '''
    jQuery("#id_firm_employee_devices").append(ret_employee_devices_html)
    
    ret_office_device_html = f'''
      {office_device_count}
    '''
    jQuery("#id_firm_office_devices").append(ret_office_device_html)

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
    pass

  
  def init_staff_tab(self):
    pass

  
  
  def destroy(self):
    if self.container_el:
      self.container_el.innerHTML = ''