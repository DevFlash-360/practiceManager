import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from .. import Forms


class ContactForm(FormBase):

    def __init__(self, **kwargs):
        print('ContactForm')
        kwargs['model'] = 'Contact'
        self.first_name = TextInput(name='name', label='First Name', save=False)
        self.last_name = TextInput(name='last_name', label='Last Name', save=False)
        self.contact_group = LookupInput(model='ContactGroup', name='contact_group', label='Contact Group')
        self.entity = LookupInput(name='entity', label='Entity', model='Entity', text_field='name')
        self.email = TextInput(name='email', label='Email')
        self.mobile_phone = TextInput(name='mobile_phone', label='Mobile Phone', input_type='tel')
        self.work_phone = TextInput(name='work_phone', label='Work Phone', input_type='tel')
        self.title_position = TextInput(name='title_position', label='Title / Position')
        self.department = TextInput(name='department', label='Department')
        self.courtroom = TextInput(name='courtroom', label='Courtroom')

        self.personal_details = MultiFieldInput(name='personal_details', model='Contact')
        self.address = MultiFieldInput(name='address', model='Contact')
        self.employment = MultiFieldInput(name='employment', model='Contact')
        self.criminal_history = MultiFieldInput(name='criminal_history', model='Contact', cols=2)
        self.additional_info = MultiFieldInput(name='additional_info', label='Additional Information', model='Contact')

        sections = [
            {'name': '_', 'rows': [
                [self.first_name, self.last_name],
                [self.email, self.contact_group],
                [self.mobile_phone, self.entity],
                [self.work_phone, self.title_position],
                [self.department, self.courtroom],
                [self.personal_details, self.address],
                [self.employment, self.additional_info],
                [self.criminal_history]
            ]}
        ]

        super().__init__(sections=sections, **kwargs)
        self.fullscreen = True
