import anvil.server
# Application navigation
from anvil.js.window import ej, jQuery
import sys
import time
from AnvilFusion.tools.utils import AppEnv
from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormBase import FormBase
from ... import Forms
from ..models import Lead

# Sidebar control CSS
PMAPP_SIDEBAR_CSS = 'e-inherit e-caret-hide pm-sidebar-menu'
PMAPP_SIDEBAR_WIDTH = 200
PMAPP_SIDEBAR_POPUP_OFFSET = 1

# Appbar menu item list
PMAPP_APPBAR_MENU = [
    {'id': 'case_menu', 'text': 'Case Management', 'items': []},
    {'id': 'intake_menu', 'text': 'Intake', 'items': []},
    {'id': 'tools_menu', 'text': 'Tools', 'items': []},
    {'id': 'staff_menu', 'text': 'Staff', 'items': []},
    {'id': 'finance_menu', 'text': 'Finance', 'items': []},
    {'id': 'admin_menu', 'text': 'Admin', 'items': []},
    # {'id': 'settings_menu', 'text': 'Settings', 'items': []},
]

# Sidebar menu item list
PMAPP_SIDEBAR_MENUS = {
    'case_menu': [
        {'nodeId': 'case_agenda', 'nodeText': 'Agenda', 'nodeChild': []},
        {'nodeId': 'case_dashboard', 'nodeText': 'Case Dashboard', 'nodeChild': [
            {'nodeId': 'case_dashboard_events', 'nodeText': 'Events', 'nodeChild': []},
            {'nodeId': 'case_dashboard_tasks', 'nodeText': 'Tasks', 'nodeChild': []},
            {'nodeId': 'case_dashboard_documents', 'nodeText': 'Documents', 'nodeChild': []},
            {'nodeId': 'case_dashboard_time_entries', 'nodeText': 'Time Entries', 'nodeChild': []},
            {'nodeId': 'case_dashboard_expenses', 'nodeText': 'Expenses', 'nodeChild': []},
            {'nodeId': 'case_dashboard_invoices', 'nodeText': 'Invoices', 'nodeChild': []},
            {'nodeId': 'case_dashboard_contacts', 'nodeText': 'Contacts', 'nodeChild': []},
            {'nodeId': 'case_dashboard_updates', 'nodeText': 'Updates', 'nodeChild': []},
            {'nodeId': 'case_dashboard_requirements', 'nodeText': 'Requirements', 'nodeChild': []},
        ]},
        {'nodeId': 'case_reports', 'nodeText': 'Reports', 'nodeChild': [
            {'nodeId': 'case_reports_events', 'nodeText': 'Events', 'nodeChild': []},
            {'nodeId': 'case_reports_cases', 'nodeText': 'Cases', 'nodeChild': []},
            {'nodeId': 'case_reports_tasks', 'nodeText': 'Tasks', 'nodeChild': []},
            {'nodeId': 'case_reports_contacts', 'nodeText': 'Contacts', 'nodeChild': []},
            {'nodeId': 'case_reports_documents', 'nodeText': 'Documents', 'nodeChild': []},
            {'nodeId': 'case_reports_time_entries', 'nodeText': 'Time Entries', 'nodeChild': []},
            {'nodeId': 'case_reports_expenses', 'nodeText': 'Expenses', 'nodeChild': []},
            {'nodeId': 'case_reports_invoices', 'nodeText': 'Invoices', 'nodeChild': []},
            # {'nodeId': 'case_reports_payments', 'nodeText': 'Payments', 'nodeChild': []},
            # {'nodeId': 'case_reports_clients', 'nodeText': 'Clients', 'nodeChild': []},
            # {'nodeId': 'case_reports_entities', 'nodeText': 'Entities', 'nodeChild': []},
            # {'nodeId': 'case_reports_updates', 'nodeText': 'Updates', 'nodeChild': []},
            # {'nodeId': 'case_reports_requirements', 'nodeText': 'Requirements', 'nodeChild': []},
        ]},
        {'nodeId': 'case_activity_feed', 'nodeText': 'Activity Feed', 'nodeChild': []},
        {'nodeId': 'case_analytics', 'nodeText': 'Analytics', 'nodeChild': []},
    ],
    'intake_menu': [
        {'nodeId': 'intake_leads', 'nodeText': 'Leads', 'nodeChild': []},
        {'nodeId': 'intake_lead_analytics', 'nodeText': 'Lead Analytics', 'nodeChild': []},
    ],
    'tools_menu': [
        {'nodeId': 'tools_date_calculator', 'nodeText': 'Date Calculator', 'nodeChild': []},
        {'nodeId': 'tools_probation_calculator', 'nodeText': 'Probation Calculator', 'nodeChild': []},
        {'nodeId': 'tools_settlement_calculator', 'nodeText': 'Settlement Calculator', 'nodeChild': []},
        {'nodeId': 'tools_statute_search', 'nodeText': 'Statute Search', 'nodeChild': []},
        {'nodeId': 'tools_warrant_search', 'nodeText': 'Warrant Search', 'nodeChild': []},
        {'nodeId': 'tools_analytics', 'nodeText': 'Analytics', 'nodeChild': []},
        {'nodeId': 'tools_admin', 'nodeText': 'System Admin', 'nodeChild': [
            {'nodeId': 'tools_admin_activity', 'nodeText': 'Activity', 'nodeChild': []},
            {'nodeId': 'tools_admin_bank_account_type', 'nodeText': 'Bank Account Type', 'nodeChild': []},
            {'nodeId': 'tools_admin_branch', 'nodeText': 'Branch', 'nodeChild': []},
            {'nodeId': 'tools_admin_case_stage', 'nodeText': 'Case Stage', 'nodeChild': []},
            {'nodeId': 'tools_admin_case_status', 'nodeText': 'Case Status', 'nodeChild': []},
            {'nodeId': 'tools_admin_case_workflow', 'nodeText': 'Case Worflow', 'nodeChild': []},
            # {'nodeId': 'tools_admin_case_workflow_item', 'nodeText': 'Case Worflow Items', 'nodeChild': []},
            {'nodeId': 'tools_admin_cause_of_action', 'nodeText': 'Cause of Action', 'nodeChild': []},
            {'nodeId': 'tools_admin_contact_group', 'nodeText': 'Contact Group', 'nodeChild': []},
            {'nodeId': 'tools_admin_contact_role', 'nodeText': 'Contact Role', 'nodeChild': []},
            {'nodeId': 'tools_admin_entity_type', 'nodeText': 'Entity Type', 'nodeChild': []},
            {'nodeId': 'tools_admin_fee_type', 'nodeText': 'Fee Type', 'nodeChild': []},
            {'nodeId': 'tools_admin_lead_source', 'nodeText': 'Lead Source', 'nodeChild': []},
            {'nodeId': 'tools_admin_practice_area', 'nodeText': 'Practice Area', 'nodeChild': []},
            {'nodeId': 'tools_admin_type_of_action', 'nodeText': 'Type of Action', 'nodeChild': []},
            {'nodeId': 'tools_admin_staff_group', 'nodeText': 'Staff Group', 'nodeChild': []},
            {'nodeId': 'tools_admin_staff_pay_type', 'nodeText': 'Staff Pay Type', 'nodeChild': []},
            # {'nodeId': 'tools_admin_', 'nodeText': '', 'nodeChild': []},
        ]},
    ],
    'staff_menu': [
        {'nodeId': 'staff_my_timesheets', 'nodeText': 'My Timesheets', 'nodeChild': []},
        {'nodeId': 'staff_my_reimbursement', 'nodeText': 'My Reimbursement Requests', 'nodeChild': []},
        {'nodeId': 'staff_my_timeoff', 'nodeText': 'My Time-Off Requests', 'nodeChild': []},
        {'nodeId': 'staff_my_incentives', 'nodeText': 'My Performance Incentives', 'nodeChild': []},
        {'nodeId': 'staff_directory', 'nodeText': 'Staff Directory', 'nodeChild': []},
    ],
    'finance_menu': [
        {'nodeId': 'finance_checks', 'nodeText': 'Checks', 'nodeChild': []},
        {'nodeId': 'finance_payments', 'nodeText': 'Payments', 'nodeChild': []},
        {'nodeId': 'finance_ledger', 'nodeText': 'Master Ledger', 'nodeChild': []},
        {'nodeId': 'finance_bank_accounts', 'nodeText': 'Bank Accounts', 'nodeChild': []},
        {'nodeId': 'finance_incentives', 'nodeText': 'Performance Incentives', 'nodeChild': []},
        {'nodeId': 'finance_timeoff', 'nodeText': 'Time-Off Requests', 'nodeChild': []},
        {'nodeId': 'finance_reimbursement', 'nodeText': 'Reimbursement Requests', 'nodeChild': []},
        {'nodeId': 'finance_timesheets', 'nodeText': 'Timesheets', 'nodeChild': []},
        {'nodeId': 'finance_payrolls', 'nodeText': 'Payrolls', 'nodeChild': []},
    ],
    'admin_menu': [
        {'nodeId': 'admin_staffs', 'nodeText': 'Manage Staff', 'nodeChild': []},
    ]
    # 'settings_menu': [
    #     {'nodeId': 'settings_user', 'nodeText': 'User', 'nodeChild': []},
    #     {'nodeId': 'settings_security', 'nodeText': 'Security', 'nodeChild': []},
    #     {'nodeId': 'settings_notification', 'nodeText': 'Notification', 'nodeChild': []},
    # ]
}

PMAPP_DEFAULT_NAV_ITEMS = {
    'case_menu': 'case_agenda',
    'intake_menu': 'intake_leads',
    'tools_menu': 'tools_date_calculator',
    'staff_menu': 'staff_my_timesheets',
    'finance_menu': 'finance_payments',
    'admin_menu': 'admin_staffs',
    # 'settings_menu': 'settings_user',
}

# Navigation items/actions
PMAPP_NAV_ITEMS = {
    'case_agenda': {'class': 'CaseAgendaView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_activity_feed': {'class': 'CaseActivityFeedView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_analytics': {'class': 'AnalyticsView', 'type': 'custom', 'action': 'open', 'props': {}},
    # 'tools_date_calculator': {'class': 'DateCalculatorView', 'type': 'custom', 'action': 'open', 'props': {}},
    # 'tools_admin_activity': {'model': 'Activity', 'type': 'view', 'action': 'open', 'props': {}},

    'case_dashboard_old': {'name': 'CaseDashboardOldPage', 'type': 'page', 'action': 'open',
                           'subcomponent': 'case_dashboard_events', 'props': {}},
    'case_dashboard': {'name': 'CaseDashboardPage', 'type': 'page', 'action': 'open', 'config': '', 'props': {}},
    'case_dashboard_events': {'class': 'EventScheduleView', 'type': 'custom', 'action': 'open', 'props': {'dashboard': True}},
    'case_dashboard_tasks': {'class': 'TaskListView', 'type': 'custom', 'action': 'open', 'props': {'dashboard': True}},
    'case_dashboard_documents': {'class': 'CaseDocumentsView', 'type': 'custom', 'action': 'open', 'props': {'dashboard': True}},
    'case_dashboard_time_entries': {'class': 'TimeEntryView', 'type': 'custom', 'action': 'open', 'props': {'dashboard': True}},
    'case_dashboard_expenses': {'class': 'ExpenseView', 'type': 'custom', 'action': 'open', 'props': {'dashboard': True}},
    'case_dashboard_invoices': {'class': 'InvoiceListView', 'type': 'custom', 'action': 'open', 'props': {'dashboard': True}},
    'case_dashboard_contacts': {'model': 'CaseContact', 'type': 'view', 'action': 'open', 'props': {}},
    'case_dashboard_updates': {'class': 'CaseUpdatesView', 'type': 'custom', 'action': 'open', 'props': {'dashboard': True}},
    'case_dashboard_requirements': {'model': 'CaseRequirement', 'type': 'view', 'action': 'open', 'props': {}},

    'case_reports_events': {'class': 'EventScheduleView', 'type': 'custom', 'action': 'open', 'props': {}},
    # 'case_reports_cases': {'class': 'CaseListView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_reports_cases': {'class': 'CaseListView', 'type': 'custom', 'action': 'open', 'config': 'CaseListView', 'props': {}},
    'case_reports_tasks': {'class': 'TaskListView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_reports_contacts': {'class': 'ContactListView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_reports_documents': {'class': 'CaseDocumentsView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_reports_time_entries': {'class': 'TimeEntryView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_reports_expenses': {'class': 'ExpenseView', 'type': 'custom', 'action': 'open', 'props': {}},
    'case_reports_invoices': {'class': 'InvoiceListView', 'type': 'custom', 'action': 'open', 'props': {}},

    'intake_leads': {'class': 'LeadListView', 'type': 'custom', 'action': 'open', 'props': {}},
    # 'intake_lead_analytics': {'model': '', 'type': 'page|view|form', 'action': 'open|popup', 'props': {}},

    'tools_date_calculator': {'class': 'DateCalculatorView', 'type': 'custom', 'action': 'open', 'props': {}},
    'tools_probation_calculator': {'class': 'ProbationCalculatorView', 'type': 'custom', 'action': 'open', 'props': {}},
    'tools_settlement_calculator': {'class': 'SettlementCalculatorView', 'type': 'custom', 'action': 'open', 'props': {}},
    'tools_statute_search': {'class': 'StatuteListView', 'type': 'custom', 'action': 'open', 'props': {}},
    'tools_warrant_search': {'class': 'WarrantListView', 'type': 'custom', 'action': 'open', 'props': {}},
    # 'tools_analytics': {'model': '', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_activity': {'model': 'Activity', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_bank_account_type': {'model': 'BankAccountType', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_branch': {'model': 'Branch', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_case_stage': {'model': 'CaseStage', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_case_status': {'model': 'CaseStatus', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_case_workflow': {'model': 'CaseWorkflow', 'type': 'view', 'action': 'open', 'props': {}},
    # 'tools_admin_case_workflow_item': {'model': 'CaseWorkflowItem', 'type': 'view', 'action': 'open', 
    #                               'config': 'CaseWorkflowItemView', 'props': {}},
    'tools_admin_cause_of_action': {'model': 'CauseOfAction', 'type': 'view', 'action': 'open',
                                    'config': 'CauseOfActionView', 'props': {}},
    'tools_admin_contact_group': {'model': 'ContactGroup', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_contact_role': {'model': 'ContactRole', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_entity_type': {'model': 'EntityType', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_fee_type': {'model': 'FeeType', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_lead_source': {'model': 'LeadSource', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_practice_area': {'model': 'PracticeArea', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_type_of_action': {'model': 'TypeOfAction', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_staff_group': {'model': 'StaffGroup', 'type': 'view', 'action': 'open', 'props': {}},
    'tools_admin_staff_pay_type': {'model': 'StaffPayType', 'type': 'view', 'action': 'open', 'props': {}},

    'staff_my_timesheets': {'class': 'TimeSheetView', 'type': 'custom', 'action': 'open', 'props': {'only_staff': True}},
    'staff_my_reimbursement': {'class': 'ReimbursementRequestView', 'type': 'custom', 'action': 'open', 'props': {'only_staff': True}},
    'staff_my_timeoff': {'class': 'TimeOffRequestView', 'type': 'custom', 'action': 'open', 'props': {'only_staff': True}},
    'staff_my_incentives': {'class': 'PerformanceIncentiveView', 'type': 'custom', 'action': 'open', 'props': {'only_staff': True}},
    'staff_directory': {'class': 'StaffDirectoryView', 'type': 'custom', 'action': 'open', 'props': {}},

    'finance_checks': {'model': 'Check', 'type': 'view', 'action': 'open', 'config': 'CheckView', 'props': {}},
    'finance_payments': {'class': 'PaymentListView', 'type': 'custom', 'action': 'open', 'config': 'PaymentView', 'props': {}},
    'finance_ledger': {'model': 'Ledger', 'type': 'view', 'action': 'open', 'props': {}},
    'finance_bank_accounts': {'model': 'BankAccount', 'type': 'view', 'action': 'open', 'config': 'BankAccountView',
                              'props': {}},
    'finance_incentives': {'class': 'PerformanceIncentiveView', 'type': 'custom', 'action': 'open', 'props': {}},
    'finance_timeoff': {'class': 'TimeOffRequestView', 'type': 'custom', 'action': 'open', 'props': {}},
    'finance_reimbursement': {'class': 'ReimbursementRequestView', 'type': 'custom', 'action': 'open', 'props': {}},
    'finance_timesheets': {'class': 'TimeSheetView', 'type': 'custom', 'action': 'open', 'props': {}},
    'finance_payrolls': {'class': 'PayrollView', 'type': 'custom', 'action': 'open', 'props': {}},
    'admin_staffs': {'class': 'StaffManageView', 'type': 'custom', 'action': 'open', 'props': {}},
    'finance_incentives': {'model': 'PerformanceIncentive', 'type': 'view', 'action': 'open', 'props': {}},
    # 'finance_timeoff': {'model': '', 'type': 'view', 'action': 'open', 'props': {}},
    # 'finance_reimbursement': {'model': '', 'type': 'view', 'action': 'open', 'props': {}},
    'finance_timesheets': {'model': 'Timesheet', 'type': 'view', 'action': 'open', 'config': 'TimesheetView',
                           'props': {}},
    # 'finance_payrolls': {'model': '', 'type': 'view', 'action': 'open', 'props': {}},

    # 'settings_user': {'class': 'UserSettingsView', 'type': 'custom', 'action': 'open', 'props': {}},
    # 'settings_security': {'class': 'SecuritySettingsView', 'type':'custom', 'action': 'open', 'props': {}},
    # 'settings_notification': {'class': 'NotificationSettingsView', 'type': 'custom', 'action': 'open', 'props': {}},
}


# Appbar navigation class
class AppbarMenu:
    def __init__(self, container_el, sidebar, menu_items):
        self.container_el = container_el
        self.sidebar = sidebar
        self.menu_items = menu_items
        self.selected_el = None

        self.menu = ej.navigations.Menu({
            'cssClass': 'e-inherit',
            'items': self.menu_items,
            'select': self.menu_select
        })

    def show(self):
        self.menu.appendTo(jQuery(f"#{self.container_el}")[0])

    def menu_select(self, args):
        if self.selected_el is not None:
            self.selected_el.classList.remove('pm-appbar-menu-selected')
        self.selected_el = args.element
        self.selected_el.classList.add('pm-appbar-menu-selected')
        menu_id = args.item.properties.id
        self.sidebar.show_menu(menu_id)


# Sidebar navigation class
class Sidebar:
    def __init__(self,
                 target_el,
                 container_el,
                 content_id,
                 sidebar_width=PMAPP_SIDEBAR_WIDTH,
                 sections=None,
                 nav_items=None,
                 **properties):

        if sections is None:
            sections = PMAPP_SIDEBAR_MENUS
        if nav_items is None:
            nav_items = PMAPP_NAV_ITEMS
        self.target_el = target_el
        self.container_el = container_el
        self.content_id = content_id
        self.nav_target_id = None
        self.content_control = None
        self.nav_items = nav_items

        # Init sidebar menu controls
        self.control = self.sidebar = ej.navigations.Sidebar({
            'width': sidebar_width,
            'target': self.target_el,
            'mediaQuery': '(min-width: 600px)',
            'isOpen': False,
            'animate': False,
        })

        self.menu = ej.navigations.TreeView({
            'fields': {
                'cssClass': PMAPP_SIDEBAR_CSS,
                'dataSource': '',
                'id': 'nodeId',
                'text': 'nodeText',
                'child': 'nodeChild'
            },
            'loadOnDemand': False,
            'expandOn': 'Click',
            'nodeSelected': self.menu_select,
        })

    # Show sidebar menu
    def show(self, menu_id):
        self.menu.appendTo(jQuery(f"#{self.container_el}-menu")[0])
        self.control.appendTo(jQuery(f"#{self.container_el}")[0])
        self.show_menu(menu_id)

    # Sidebar toggle
    def toggle(self, args):
        self.control.toggle()

    def show_menu(self, menu_id, subcomponent=None, props=None):
        self.menu.fields.dataSource = PMAPP_SIDEBAR_MENUS[menu_id]
        self.menu_select(None, subcomponent=(subcomponent or PMAPP_DEFAULT_NAV_ITEMS[menu_id]), props=props)

    def menu_select(self, args, subcomponent=None, props=None):
        # print('menu selected !!!!!!!')
        if subcomponent is None:
            if 'e-level-1' in list(args.node.classList):
                self.menu.collapseAll()
                self.menu.expandAll([args.node])
                self.nav_target_id = None
            menu_item_id = args.nodeData.id
            component = PMAPP_NAV_ITEMS[menu_item_id] if menu_item_id in PMAPP_NAV_ITEMS else None
        else:
            component = PMAPP_NAV_ITEMS[subcomponent]
        if component is None:
            return
        if props is not None:
            component['props'] = props

        if self.content_control is not None and self.nav_target_id is None:
            self.content_control.destroy()

        nav_container_id = self.content_id if self.nav_target_id is None else self.nav_target_id
        print('debug output.')
        if component['type'] == 'custom':
            print('this is custom component!!!!!!!')
            try:
                view_class = getattr(AppEnv.views, component['class'])
                self.content_control = view_class(container_id=nav_container_id, **component['props'])
            except Exception as e:
                print(e)
        if component['type'] == 'view':
            if 'config' in component:
                self.content_control = GridView(view_name=component['config'], container_id=nav_container_id)
            elif hasattr(AppEnv.views, f"{component['model']}View"):
                view_class = getattr(AppEnv.views, f"{component['model']}View")
                self.content_control = view_class(container_id=nav_container_id)
            else:
                self.content_control = GridView(model=component['model'], container_id=nav_container_id)

        elif component['type'] == 'form':
            try:
                form_class = getattr(AppEnv.forms, f"{component['model']}Form")
                self.content_control = form_class(target=nav_container_id)
            except Exception as e:
                print(e.args)
                self.content_control = FormBase(model=component['model'], target=nav_container_id)

        elif component['type'] == 'page':
            try:
                page_class = getattr(AppEnv.pages, f"{component['name']}")
                self.content_control = page_class(container_id=nav_container_id, **component['props'])
            except Exception as e:
                print(e.args)
                # self.content_control = Pages.BaseForm(model=component['model'], target=self.content_id)

        if hasattr(self.content_control, 'target_id'):
            self.nav_target_id = self.content_control.target_id
            # print('check for sth..')

        # try:
        # print(component, self.content_control)
        
        self.content_control.form_show()
        # except Exception as e:
        #     print(e)
        if self.control.isOpen:
            self.control.toggle()
            self.control.toggle()

        if 'subcomponent' in component:
            # print("check if it's wrapped component")
            time.sleep(0.5)
            self.menu_select(None, subcomponent=component['subcomponent'])

class DetailsView:
    def __init__(self):
        self.sidebar = ej.navigations.Sidebar({
            'width': '400px',
            # 'showBackdrop': True,
            'enablePersistence': True,
            'type': 'Push',
            'position': 'Right'
        })
        self.reopen_btn = ej.buttons.Button({
            'content': 'Reopen'
        })
        self.won_btn = ej.buttons.Button({
            'content': 'Won'
        })
        self.lost_btn = ej.buttons.Button({
            'content': 'Lost'
        })
        self.close_btn = ej.buttons.Button({
            'cssClass': 'e-flat',
            'iconCss': 'fa-solid fa-xmark'
        })

    def form_show(self):
        self.reopen_btn.appendTo(jQuery('#btn_details_reopen')[0])
        self.won_btn.appendTo(jQuery('#btn_details_won')[0])
        self.lost_btn.appendTo(jQuery('#btn_details_lost')[0])
        self.close_btn.appendTo(jQuery('#btn_details_close')[0])
        self.sidebar.appendTo(jQuery(f"#pm-details-sidebar")[0])

        self.close_btn.element.addEventListener('click', self.hide)
        self.reopen_btn.element.addEventListener('click', self.lead_reopen_handler)
        self.won_btn.element.addEventListener('click', self.lead_won_handler)
        self.lost_btn.element.addEventListener('click', self.lead_lost_handler)
        
        jQuery(f"#btn_details_reopen")[0].style.display = 'None'
        jQuery(f"#btn_details_won")[0].style.display = 'None'
        jQuery(f"#btn_details_lost")[0].style.display = 'None'

    def show(self):
        self.sidebar.show()
    
    def hide(self, args=None):
        self.sidebar.hide()
        
    def hide_lead_buttons(self):
        jQuery(f"#btn_details_reopen")[0].style.display = 'None'
        jQuery(f"#btn_details_won")[0].style.display = 'None'
        jQuery(f"#btn_details_lost")[0].style.display = 'None'

    def show_reopen(self):
        jQuery(f"#btn_details_reopen")[0].style.display = 'block'
        jQuery(f"#btn_details_won")[0].style.display = 'None'
        jQuery(f"#btn_details_lost")[0].style.display = 'None'

    def hide_reopen(self):
        jQuery(f"#btn_details_reopen")[0].style.display = 'None'
        jQuery(f"#btn_details_won")[0].style.display = 'block'
        jQuery(f"#btn_details_lost")[0].style.display = 'block'
    
    def lead_won_handler(self, args):
        form_invoice = Forms.InvoiceForm(target="pm-content")
        form_case = Forms.CaseForm(target="pm-content", next_form=form_invoice)
        
        lead = Lead.get(AppEnv.details_lead_uid)
        for field in [x for x in form_case.form_fields if not x.is_dependent and x not in form_case.subforms]:
            field.show()
            if field.name and getattr(lead, field.name, None):
                field.value = lead[field.name]
        for field in form_case.form_fields:
            if field.on_change is not None:
                field.on_change({'name': field.name, 'value': field.value})
        lead.update({'lead_status': 'Won'})
        lead.save()
        AppEnv.navigation.content_control.refresh()

        form_case.form_show()
    
    def lead_lost_handler(self, args):
        form_control = Forms.LeadLostForm(target="pm-content")
        form_control.form_show()
    
    def lead_reopen_handler(self, args):
        lead = Lead.get(AppEnv.details_lead_uid)
        lead.update({'lead_status': 'Open'})
        lead.save()
        AppEnv.navigation.content_control.refresh()


PMAPP_APPBAR_ADD_ITEM = {
    'Add Time Entry': {'model': 'TimeEntry', 'type': 'form'},
    'Add Event': {'model': 'Event', 'type': 'form'},
    'Add Task': {'model': 'Task', 'type': 'form'},
    'Add Document': {'model': 'Document', 'type': 'form'},
    'Add Expense': {'model': 'Expense', 'type': 'form'},
    'Add Contact': {'model': 'Contact', 'type': 'form'},
    'Add Lead': {'model': 'Lead', 'type': 'form'},
    'Add Case': {'model': 'Case', 'type': 'form'},
    'Add Invoice': {'model': 'Invoice', 'type': 'form'},
    'Add Update': {'model': 'CaseUpdate', 'type': 'form'},
    'Ask Me Anything': {'model': 'Assistant', 'type': 'form'},
}


def add_item_select(args, content_el_id):
    item = PMAPP_APPBAR_ADD_ITEM.get(args.item.text)
    if item and item['type'] == 'form':
        try:
            form_class = getattr(AppEnv.forms, f"{item['model']}Form")
            form_control = form_class(target=content_el_id)
        except Exception as e:
            print(e.args)
            form_control = FormBase(model=item['model'], target=content_el_id)
        form_control.form_show()

PMAPP_APPBAR_USER_ITEM = {
    'Account': {'model': 'Settings', 'type': 'view'},
    'Sign Out': {},
    'Test': {'model': 'ESignSettings', 'type': 'form'},
}

def user_item_select(args, content_el_id):
  print('User item selected')
  print('content id:')
  print(content_el_id)
  print('----')
  item = PMAPP_APPBAR_USER_ITEM.get(args.item.text)
  if item and item['type'] == 'view':
    try:
      view_class = getattr(AppEnv.views, f"{item['model']}View")
      # form_class = getattr(AppEnv.pages, f"SettingsPage")
      view_control = view_class(container_id=content_el_id)
    except Exception as e:
      print(e.args)
      view_control = GridView(model=item['model'], container_id=nav_container_id)
    view_control.form_show()
  if item and item['type'] == 'form':
    try:
      form_class = getattr(AppEnv.forms, f"{item['model']}Form")
      form_control = form_class(target = content_el_id)
    except Exception as e:
        print(e.args)
        form_control = FormBase(model=item['model'], target=content_el_id)
    form_control.form_show()




# def user_item_select(args, content_el_id):
#   print('User item selected')
#   item = PMAPP_APPBAR_USER_ITEM.get(args.item.text)
#   if item and item['type'] == 'form':
#     try:
#       view_class = getattr(AppEnv.views, f"{item['model']}View")
#       # form_class = getattr(AppEnv.pages, f"SettingsPage")
#       view_control = view_class(target=content_el_id)
#     except Exception as e:
#       print(e.args)
#       view_control = FormBase(model=item['model'], target=content_el_id)
#     view_control.form_show()
