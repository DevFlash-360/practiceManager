from AnvilFusion.components.FormBase import FormBase, SubformGrid
from AnvilFusion.components.FormInputs import *
from .. import Forms


class CaseWorkflowForm(FormBase):
    def __init__(self, **kwargs):
        print('CaseWorkflowForm')
        
        self.name = TextInput(name='name', label='Name')
        self.practice_area = LookupInput(name='practice_area', label='Practice Area', model='PracticeArea', 
                                         on_change=self.update_workflow_name)
        
        workflow_item_view = {
            
        }
        self.items = SubformGrid(name='items', label='Items', model='CaseWorkflowItem')
        
        
        
        fields = [self.name, self.practice_area, self.items]
        
        super().__init__(model='CaseWorkflow', fields=fields, **kwargs)
        
        
    def update_workflow_name(self, args):
        if args['value'] is None:
            self.name.value = None
        else:
            self.name.value = self.practice_area.value['name']
