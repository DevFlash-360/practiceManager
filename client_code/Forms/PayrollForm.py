import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1, POPUP_WIDTH_COL3
import anvil.tables.query as q
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from DevFusion.tools.utils import workdays_between, next_monday
from ..app.models import Timesheet, PerformanceIncentive, ReimbursementRequest, PayrollTotal, Staff
from datetime import timedelta


class PayrollForm(FormBase):
    def __init__(self, **kwargs):
        kwargs['model'] = 'Payroll'
        
        payroll_totals_view = {
            'model': 'PayrollTotal',
            'columns': [
                {'name': 'staff.full_name', 'label': 'Staff', 'width': '25%'},
                {'name': 'total_base_pay', 'label': 'Total Base Pay', 'width': '25%'},
                {'name': 'total_overtime_pay', 'label': 'Total Overtime Pay', 'width': '25%'},
                {'name': 'total_incentive_pay', 'label': 'Total Incentive Pay', 'width': '25%'},
                {'name': 'total_reimbursement_pay', 'label': 'Total Reimbursement Pay', 'width': '25%'},
                {'name': 'total_pay', 'label': 'Total Pay', 'width': '25%'},
            ],
        }
        self.payroll_totals = SubformGrid(name='payroll_totals', label='Payroll Totals', model='PayrollTotal',
                                           link_model='Payroll', link_field='payroll', 
                                           form_container_id=kwargs.get('target'),
                                           view_config=payroll_totals_view,
                                           add_edit_form=PayrollTotalForm)
        self.staffs = LookupInput(name='staffs', label='Staffs', model='Staff', text_field='full_name', select='multi')
        self.select_all_staff = CheckboxInput(name='select_all_staff', label='Select All Staff', on_change=self.change_all_staff)
        self.start = DateInput(name='start', label='Start')
        self.end = DateInput(name='end', label='End')
        self.total_payroll = NumberInput(name='total_payroll', label='Total Payroll')
        self.total_payroll.enabled = False
        self.payroll_totals.enabled = False
        self.select_all_staff.save = False

        sections = [
            {'name': '_', 'rows': [
                [self.start, self.end],
                [self.staffs],
                [self.select_all_staff],
                [self.payroll_totals],
                [self.total_payroll]
            ]},
        ]
        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
        self.fullscreen = True

    def form_save(self, args):
        total_payroll = 0.0
        staff_vals = self.staffs.value
        staff_uids = [member.uid for member in staff_vals]
        staffs = Staff.search(uid=q.any_of(*staff_uids))
        
        payroll_totals = []
        timesheets_save = []
        incentives_save = []
        reimburesements_save = []

        for staff in staffs:
            total_base_pay = 0
            if staff.pay_type == 'hourly':
                timesheets = Timesheet.search(
                    staff=staff,
                    clock_in_time=q.greater_than_or_equal_to(self.start.value),
                    clock_out_time=q.less_than_or_equal_to(self.end.value)
                )
                for timesheet in timesheets:
                    total_base_pay += timesheet.earned_pay
            else:
                total_base_pay = round(staff.pay_rate / 260.0 * workdays_between(self.start.value, self.end.value), 2)
            
            weekStart = self.start.value
            total_overtime_pay = 0.0
            endLoop = False
            while not endLoop:
                nextWeekStart = next_monday(weekStart)
                if nextWeekStart >= self.end.value:
                    nextWeekStart = self.end.value + timedelta(days=1)
                    endLoop = True
                overtime_timesheets = Timesheet.search(
                    staff=staff,
                    clock_in_time=q.greater_than_or_equal_to(weekStart),
                    clock_out_time=q.less_than_or_equal_to(nextWeekStart)
                )
                weekPay = 0
                for timesheet in overtime_timesheets:
                    weekPay += timesheet.hours_worked
                    timesheet.save()
                    timesheets_save.append(timesheet)

                currentOvertime = 0
                week_base_hours = (staff.weekly_base_hours if staff.weekly_base_hours else 40)
                if weekPay > week_base_hours:
                    currentOvertime = (weekPay - week_base_hours) * staff.pay_rate * staff.overtime_rate
                total_overtime_pay += currentOvertime
                weekStart = nextWeekStart
            total_incentive_pay = 0.0
            incentives = PerformanceIncentive.search(
                staff=staff,
                payment_date=q.between(min=self.start.value, max=self.end.value)
            )
            for incentive in incentives:
                total_incentive_pay += incentive.amount
                incentive.save()
                incentives_save.append(incentive)
            
            total_reimbursement_pay = 0.0
            reimbursements = ReimbursementRequest.search(
                staff=staff,
                date=q.between(min=self.start.value, max=self.end.value),
            )
            for reimbursement in reimbursements:
                total_reimbursement_pay += reimbursement.total
                reimbursement.save()
                reimburesements_save.append(reimbursement)

            total_pay = total_base_pay + total_overtime_pay + total_incentive_pay + total_reimbursement_pay
            total_payroll += total_pay
            if self.action == 'add':
                payroll_total = PayrollTotal(
                    staff=staff,
                    total_base_pay=total_base_pay,
                    total_overtime_pay=total_overtime_pay,
                    total_incentive_pay=total_incentive_pay,
                    total_reimbursement_pay=total_reimbursement_pay,
                    total_pay=total_pay
                )
                payroll_totals.append(payroll_total)
            elif self.action == 'edit':
                payroll_totals = PayrollTotal.search(
                    payroll=self.data,
                    staff=staff
                )
                for payroll_total in payroll_totals:
                    payroll_total.total_base_pay = total_base_pay
                    payroll_total.total_overtime_pay = total_overtime_pay
                    payroll_total.total_incentive_pay = total_incentive_pay
                    payroll_total.total_reimbursement_pay = total_reimbursement_pay
                    payroll_total.total_pay = total_pay
                    payroll_total.save()
        self.total_payroll.value = total_payroll

        super().form_save(args)

        if self.action == 'add':
            for payroll_total in payroll_totals:
                payroll_total.payroll = self.data
                payroll_total.save()
            for timesheet_save in timesheets_save:
                timesheet_save.payroll = self.data
                timesheet_save.save()
            for incentive_save in incentives_save:
                incentive_save.payroll = self.data
                incentive_save.save()
            for reimbursement_save in reimburesements_save:
                reimbursement_save.payroll = self.data
                reimbursement_save.save()

    def change_all_staff(self, args):
        if self.select_all_staff.value == True:
            all_staffs = Staff.search()
            self.staffs.value = all_staffs
        elif self.select_all_staff.value == False:
            self.staffs.value = None

class PayrollTotalForm(FormBase):
    def __init__(self, **kwargs):
        kwargs['model'] = 'PayrollTotal'

        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name')
        self.total_base_pay = NumberInput(name='total_base_pay', label='Total Base Pay')
        self.total_overtime_pay = NumberInput(name='total_overtime_pay', label='Total Overtime Pay')
        self.total_incentive_pay = NumberInput(name='total_incentive_pay', label='Total Incentive Pay')
        self.total_reimbursement_pay = NumberInput(name='total_reimbursement_pay', label='Total Reimbursement Pay')
        self.total_pay = NumberInput(name='total_pay', label='Total Pay')
        
        sections = [
            {'name': '_', 'cols': [
                [
                    self.staff, self.total_base_pay, 
                    self.total_overtime_pay, 
                    self.total_incentive_pay, 
                    self.total_reimbursement_pay, 
                    self.total_pay
                ],
            ]}
        ]
        super().__init__(sections=sections, width=POPUP_WIDTH_COL1, **kwargs)
