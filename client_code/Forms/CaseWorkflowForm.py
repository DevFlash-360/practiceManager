from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.components.FormInputs import *


class CaseWorkflowForm(FormBase):
    def __init__(self, **kwargs):
        print('CaseWorkflowForm')
        kwargs['model'] = 'CaseWorkflow'
        
        self.name = TextInput(name='name', label='Name')
        self.practice_area = LookupInput(name='practice_area', label='Practice Area', model='PracticeArea', 
                                         on_change=self.update_workflow_name)
        workflow_items_view = {
            'model': 'CaseWorkflowItem',
            'columns': [
                {'name': 'type', 'label': 'Type', 'width': '10%'},
                {'name': 'activity.name', 'label': 'Activity', 'width': '25%'},
                {'name': 'notes', 'label': 'Notes', 'width': '40%'},
                {'name': 'assigned_to.full_name', 'label': 'Assigned To', 'width': '25%'},
            ],
        }
        self.items = SubformGrid(name='items', label='Tasks and Activities', model='CaseWorkflowItem',
                                 link_model='CaseWorkflow', link_field='case_workflow', 
                                 form_container_id=kwargs.get('target'),
                                 # form_data={'practice_area': self.practice_area.value},
                                 view_config=workflow_items_view,
                                 )
        
        sections = [
            {
                'name': '_', 'rows': [
                    [ self.practice_area, self.name, None],
                    [self.items]
                ]
            }
        ]
        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
        self.fullscreen = True
        
        
    def form_open(self, args):
        super().form_open(args)
    
    
    def update_workflow_name(self, args):
        # if args['value'] is None and self.name.value == self.practice_area.value['name']:
        print('update_workflow_name', args)
        if args['value'] is None:
            print(self.name.value, self.practice_area.value, args['value'])
            self.name.value = None
            self.items.hide()
        else:
            self.name.value = self.practice_area.value['name']
            self.items.show()
        # self.items.form_data={'practice_area': self.practice_area.value}
