import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from datetime import datetime, timedelta
from ..app.models import Staff

class TimesheetForm(FormBase):
    def __init__(self, **kwargs):
        kwargs['model'] = 'Timesheet'

        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name', on_change=self.calc_earned_pay)
        self.clock_in_time = DateTimeInput(name='clock_in_time', 
                                           label='Clock In Time', 
                                           value=datetime.now(),
                                           string_format='MMM dd, yyyy hh:mm a',
                                           on_change=self.calc_earned_pay)
        self.clock_out_time = DateTimeInput(name='clock_out_time', 
                                            label='Clock Out Time',
                                            string_format='MMM dd, yyyy hh:mm a',
                                            on_change=self.calc_earned_pay)
        self.hours_worked = NumberInput(name='hours_worked', label='Hours Worked', enabled=False)
        self.earned_pay = NumberInput(name='earned_pay', label='Earned Pay', enabled=False)
        self.approved_by = LookupInput(name='approved_by', label='Approved By', model='Staff', text_field='full_name')
        self.payroll = LookupInput(name='payroll', label='Payroll', model='Payroll', text_field='staffs.full_name')

        sections = [
            {'name': '_', 'rows': [
                [self.staff],
                [self.clock_in_time, self.hours_worked],
                [self.clock_out_time, self.earned_pay],
                [self.approved_by],
                [self.payroll]
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        self.payroll.hide()

    def calc_earned_pay(self, args):
        staff_obj = None
        if self.staff.value:
            staff_obj = Staff.get(self.staff.value['uid'])
        if self.clock_in_time.value is not None and self.clock_out_time.value is not None:
            if args['name'] == 'clock_out_time':
                if self.clock_out_time.value <= self.clock_in_time.value:
                    self.clock_out_time.value = self.clock_in_time.value + timedelta(hours=1)
            self.hours_worked.value = (self.clock_out_time.value - self.clock_in_time.value).total_seconds() / 3600
        if self.hours_worked.value is not None and staff_obj and staff_obj['pay_rate']:
            self.earned_pay.value = self.hours_worked.value * staff_obj['pay_rate']
        else:
            self.earned_pay.value = None
