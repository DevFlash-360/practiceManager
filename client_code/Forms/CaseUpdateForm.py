from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL1
from AnvilFusion.components.FormInputs import *
from .. import Forms
from datetime import datetime, timedelta


class CaseUpdateForm(FormBase):

    def __init__(self, **kwargs):

        print('CaseUpdateForm')
        kwargs['model'] = 'CaseUpdate'
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.next_activity = LookupInput(model='Activity', name='activity', label='Next Activity')
        self.next_date = DateTimeInput(name='start_time', label='Next Date')
        self.todays_update = MultiLineInput(name='notes', label="Today's Update", rows=4)
        self.client_attendance_required = CheckboxInput(name='client_attendance_required',
                                                        label='Client attendance required')
        self.client_update = CheckboxInput(name='client_update', label='Client Update')

        sections = [
            {'name': '_', 'rows': [
                [self.case],
                # [self.no_case],
                [self.next_activity],
                [self.next_date],
                [self.todays_update],
                [self.client_attendance_required]
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL1, **kwargs)
