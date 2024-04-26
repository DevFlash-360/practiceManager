import uuid
import anvil.js

from anvil.js.window import ej, jQuery

from datetime import timedelta, datetime

from AnvilFusion.tools.utils import AppEnv, datetime_js_to_py
from AnvilFusion.components.FormInputs import *

from ..app.models import Staff, User, Contact, Activity, AppAuditLog

class AnalyticsView:
  def __init__(self, container_id, **kwargs):
    self.container_id = container_id or AppEnv.content_container_id
    self.container_el = jQuery(f"#{self.container_id}")[0]

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
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-billing-analytics">
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

  def prepare_case_html(self):
    return '''
      <div id="da-grid-container" style="height:100%;">
        <div class="" role="grid" aria-multiselectable="true" style="width: 100%; height: 100%;" tabindex="-1" aria-rowcount="2" aria-colcount="6">
          <div class="e-gridcontent e-wrap" style="height: calc(100% - 10px);">
            <div class="e-content" style="height: 100%; overflow-y: scroll; position: relative;">
              <table class="e-table">
                <tbody id="id-case-analytics">
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    '''

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

  def filter_data(self, type1, type2 = '', type3 = '', type4 = ''):
    ret_list = []
    for dict in self.activity_dict:
      if dict['table_name'] == type1 or dict['table_name'] == type2 or dict['table_name'] == type3 or dict['table_name'] == type4:
        ret_list.append(dict)
    return ret_list
  
  def init_billing_tab(self):
    chartData = [
    { 'x': '2000', 'y': 0.61, 'y1': 0.03, 'y2': 0.48},
    { 'x': '2001', 'y': 0.81, 'y1': 0.05, 'y2': 0.53 },
    { 'x': '2002', 'y': 0.91, 'y1': 0.06, 'y2': 0.57 },
    { 'x': '2003', 'y': 1, 'y1': 0.09, 'y2': 0.61 },
    { 'x': '2004', 'y': 1.19, 'y1': 0.14, 'y2': 0.63 },
    { 'x': '2005', 'y': 1.47, 'y1': 0.20, 'y2': 0.64 },
    { 'x': '2006', 'y': 1.74, 'y1': 0.29, 'y2': 0.66 },
    { 'x': '2007', 'y': 1.98, 'y1': 0.46, 'y2': 0.76 },
    { 'x': '2008', 'y': 1.99, 'y1': 0.64, 'y2': 0.77 },
    { 'x': '2009', 'y': 1.70, 'y1': 0.75, 'y2': 0.55 },
    ]
    chart = ej.charts.Chart({
      'primaryXAxis': {
          'title': 'Years',
          'valueType': 'Category',
          'majorTickLines': { 'width': 0 },
          'edgeLabelPlacement': 'Shift'
      },
      'primaryYAxis':
      {
          'title': 'Spend in Billions',
          'minimum': 0,
          'maximum': 4,
          'interval': 1,
          'majorTickLines': { 'width': 0 },
          'labelFormat': '{value}B'
      },
      'series': [
          {
              'dataSource': chartData, 'xName': 'x', 'yName': 'y',
              # // Series type as polar series
              'type' : 'Polar',
              # //Series draw type as stacked area series
              'drawType': 'StackingArea',
              'name': 'Organic',
          }, {
              'dataSource': chartData, 'xName': 'x', 'yName': 'y1',
              'type' : 'Polar',
              'drawType': 'StackingArea', 'name': 'Fair-trade',
          }, {
              'dataSource': chartData, 'xName': 'x', 'yName': 'y2',
              'type' : 'Polar',
              'drawType': 'StackingArea', 'name': 'Veg Alternatives',
          },
      ],
      'title': 'Trend in Sales of Ethical Produce'
    }, '#id-billing-analytics');
    ret_html = f'''
      <tr class="e-row">
        <td class="e-rowcell" style="text-align: left;">{chart}</td>
      </tr>
    '''
    jQuery("#id-billing-analytics").append(ret_html)

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