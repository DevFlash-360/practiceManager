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
        self.due_date_base = RadioButtonInput(name='due_date_base', label='Due Date Based On', options=['Start Date', 'End Date'])
        self.before_after = RadioButtonInput(name='before_after', label='When', options=['Before', 'After'], save=False)
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
