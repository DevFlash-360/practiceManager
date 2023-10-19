from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import HyperlinkInput
from datetime import datetime, timedelta


class CaseRequirementForm(FormBase):

    def __init__(self, **kwargs):

        print('CaseRequirementForm')
        kwargs['model'] = 'CaseRequirement'
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.name = TextInput(name='name', label='Name', required=True)
        self.notes = MultiLineInput(name='notes', label="Notes", rows=4)
        self.url = HyperlinkInput(name='url', label='URL')
        self.due_date = DateTimeInput(name='due_date', label='Due Date')
        self.completed = CheckboxInput(name='completed', label='Completed')

        sections = [
            {'name': '_', 'cols': [
                [self.case, self.name, self.notes, self.due_date, self.url, self.completed],
            ]}
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
