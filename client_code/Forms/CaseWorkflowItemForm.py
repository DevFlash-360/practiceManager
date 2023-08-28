from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *


class CaseWorkflowItemForm(FormBase):
    def __init__(self, **kwargs):
        print('CaseWorkflowItemForm')
        kwargs['model'] = 'CaseWorkflowItem'
        
        # self.practice_area = LookupInput(name='practice_area', label='Practice Area', model='PracticeArea', enabled=False)
        self.type = RadioButtonInput(name='type', label='Type', options=['Task', 'Event'], value='Task')
        self.activity = LookupInput(name='activity', label='Activity', model='Activity')
        self.related_task = LookupInput(name='related_task', label='Related Task', model='CaseWorkflowItem', text_field='item_name')
        self.due_date_base = RadioButtonInput(name='due_date_base', label='Due Date Based On', 
                                              options=[
                                                  'Case Open Date',
                                                  'Completion of Previous Task',
                                                  'Case Activity',
                                                  'No Due Date',
                                              ],
                                              value='Case Open Date',
                                              on_change=self.due_date_base_change,)
        self.before_after = RadioButtonInput(name='before_after', label='When', save=False,
                                             options=['Before', 'After'], value='After')
        self.duration = NumberInput(name='duration', label='Duration')
        self.assigned_to = LookupInput(name='assigned_to', label='Assigned To', model='Staff', select='multi',
                                  text_field='full_name')
        self.priority = RadioButtonInput(name='priority', label='Priority', options=['Normal', 'High'], value='Normal')
        self.notes = MultiLineInput(name='notes', label='Notes', rows=5)
        self.documents = FileUploadInput(name='documents', label='Documents', save=False)
        
        sections = [
            {
                'name': 'task_details',
                'cols': [
                    [self.type, self.activity, self.assigned_to, self.notes, self.documents],
                    [self.due_date_base, self.related_task, self.before_after, self.duration, self.priority],
                ]
            }
        ]
        
        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
        
        
    def form_open(self, args):
        super().form_open(args)
        if self.duration.value < 0:
            self.before_after.value = 'Before'
            self.duration.value = -self.duration.value

    def from_validate(self):
        super().form_validate()
        if self.before_after.value == 'Before':
            self.duration.value = -self.duration.value


    def due_date_base_change(self, args):
        print('due_date_base_chnage', args)
        if self.due_date_base.value == 'Completion of Previous Task':
            self.related_task.show()
        elif self.due_date_base.value == 'No Due Date':
            self.related_task.hide()
            self.before_after.hide()
            self.duration.hide()
        else:
            self.related_task.hide()
            self.before_after.show()
            self.duration.show()
