import anvil.server
from DevFusion.components.GridView2 import GridView2
from AnvilFusion.tools.utils import AppEnv
from anvil.js.window import ej, jQuery
from ..app.models import Contact


class ContactListView(GridView2):
    def __init__(self, **kwargs):
        view_config = {
            'model': 'Contact',
            'columns': [
                {'name': 'full_name', 'label': 'Name'},
                {'name': 'contact_group.name', 'label': 'Group'},
                {'name': 'email', 'label': 'Email'},
                {'name': 'mobile_phone', 'label': 'Mobile Phone'},
                {'name': 'work_phone', 'label': 'Work Phone'},
            ]
        }
        super().__init__(model='Contact', view_config=view_config, **kwargs)

    def row_selected(self, args):
        jQuery(f"#details_content")[0].innerHTML = self.details_content(args)
        super().row_selected(args)

    def details_content(self, args):
        print("----------")
        print(args)

        contact = args['data']
        item = Contact.get(contact['uid'])

        content = "<div class='details_title'>Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Name</div>\
                <div class='details_record_data'>{item['full_name']}</div>\
            </div>\
        </div>"
        return content
