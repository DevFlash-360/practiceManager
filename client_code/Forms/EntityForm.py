import anvil.server
from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from .. import Forms


class EntityForm(FormBase):
    def __init__(self, **kwargs):
        print('EntityForm')
        kwargs['model'] = 'Entity'
        self.name = TextInput(name='name', label='Name')
        self.entity_type = LookupInput(model='EntityType', name='entity_type', label='Entity Type')
        self.phone = TextInput(name='phone', label='Phone')
        self.email = TextInput(name='email', label='Email')
        self.address = TextInput(name='address', label='Address')
        self.website = TextInput(name='website', label='Website')
        self.primary_contact = LookupInput(name='primary_contact', label='Primary Contact', model='Contact',
                                           text_field='full_name')

        fields = [
            self.name,
            self.entity_type,
            self.phone,
            self.email,
            self.address,
            self.website,
            self.primary_contact,
        ]

        super().__init__(fields=fields, width=POPUP_WIDTH_COL2, **kwargs)
