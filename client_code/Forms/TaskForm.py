import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Staff
import datetime


class TaskForm(FormBase):
    def __init__(self, **kwargs):

        print('TaskForm')
        kwargs['model'] = 'Task'

        self.activity = LookupInput(model='Activity', name='activity', label='Task Name')
        self.notes = MultiLineInput(name='notes', label='Notes', rows=5)
        self.priority = DropdownInput(name='priority', label='Priority', options=['Normal', 'High'])
        self.assigned_staff = LookupInput(name='assigned_staff', label='Assigned Staff', select='multi',
                                          model='Staff', text_field='full_name')
        self.case = LookupInput(name='case', label='Case', select='single',
                                model='Case', text_field='case_name')
        self.documents = FileUploadInput(name='documents', label='Documents', float_label=True, save=False)
        self.due_date = DateInput(name='due_date', label='Due Date', value=datetime.date.today(), string_format='MMM dd, yyyy')
        self.no_due_date = CheckboxInput(name='no_due_date', label='No due date', save=False,
                                         on_change=self.no_due_date_toggle)
        self.no_case = CheckboxInput(name='no_case', label='Task is not related to case', save=False,
                                     on_change=self.no_case_toggle)
        # self.completed = CheckboxInput(name='completed', label='Task is completed')

        sections = [
            {'name': '_', 'rows': [
                [self.case],
                [self.no_case],
            ]},
            {'name': '_', 'cols': [
                [
                    self.activity,
                    self.priority
                ],
                [
                    self.notes
                ]
            ]},
            {'name': '_', 'rows': [
                [self.due_date, self.assigned_staff],
                [self.no_due_date],
                [self.documents]
                # [self.completed]
            ]},
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        logged_staff = Staff.get_by('work_email', AppEnv.logged_user.get('email')) if AppEnv.logged_user else None
        self.assigned_staff.value = [logged_staff]
        if self.priority.value is None:
            self.priority.value = 'Normal'
        if self.activity.value is not None:
            if self.case.value is None:
                self.case.enabled = False
                self.no_case.value = True
            if self.due_date.value is None:
                self.due_date.enabled = False
                self.no_due_date = True

    def no_due_date_toggle(self, args):
        if self.no_due_date.value is True:
            self.due_date.value = None
            self.due_date.enabled = False
        else:
            self.due_date.enabled = True

    def no_case_toggle(self, args):
        if self.no_case.value is True:
            self.case.value = None
            self.case.enabled = False
        else:
            self.case.enabled = True
