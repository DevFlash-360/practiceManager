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
        created_by = Contact.get(item['created_by']) if item['created_by'] else None
        if created_by:
            created_by = created_by['email']
        updated_by = Contact.get(item['updated_by']) if item['updated_by'] else None
        if updated_by:
            updated_by = updated_by['email']

        address = ""
        if item['address']:
            if item['address']['address_line_1']:
                address += item['address']['address_line_1']
            if item['address']['address_line_2']:
                address += f", {item['address']['address_line_2']}"
            if item['address']['city_district']:
                address += f", {item['address']['city_district']}"
            if item['address']['state_province']:
                address += f", {item['address']['state_province']}"
            if item['address']['postal_code']:
                address += f", {item['address']['postal_code']}"
            if address:
                address += ", United States"

        content = "<div class='details_title'>Overview</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Name</div>\
                <div class='details_record_data'>{item['full_name']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Group</div>\
                <div class='details_record_data'>{item['contact_group']['name']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Contact Details</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Email</div>\
                <div class='details_record_data'>{item['email']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Mobile Phone</div>\
                <div class='details_record_data'>{item['mobile_phone']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Alternate Phone</div>\
                <div class='details_record_data'>{item['alternate_phone']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Work Phone</div>\
                <div class='details_record_data'>{item['work_phone']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Address</div>\
                <div class='details_record_data'>{address}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Department</div>\
                <div class='details_record_data'>{item['department']}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Courtroom</div>\
                <div class='details_record_data'>{item['courtroom']}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Biographical Details</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>DOB</div>\
                <div class='details_record_data'>{item['personal_details']['dob'] if item['personal_details'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>SSN</div>\
                <div class='details_record_data'>{item['personal_details']['ssn'] if item['personal_details'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Country of Citizenship</div>\
                <div class='details_record_data'>{item['personal_details']['country_of_citizenship'] if item['personal_details'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Native Language</div>\
                <div class='details_record_data'>{item['personal_details']['native_language'] if item['personal_details'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Education</div>\
                <div class='details_record_data'>{item['personal_details']['education'] if item['personal_details'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Employment</div>\
                <div class='details_record_data'>{item['employment']['employment'] if item['employment'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Current Employer</div>\
                <div class='details_record_data'>{item['employment']['current_employer'] if item['employment'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Time with current employer</div>\
                <div class='details_record_data'>{item['employment']['time_with_current_employer'] if item['employment'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Community Service</div>\
                <div class='details_record_data'>{item['additional_info']['community_service'] if item['additional_info'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Family Support</div>\
                <div class='details_record_data'>{item['additional_info']['family_support'] if item['additional_info'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Source of Funds</div>\
                <div class='details_record_data'>{item['additional_info']['source_of_funds'] if item['additional_info'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Criminal History</div>\
                <div class='details_record_data'>{item['criminal_history']['criminal_history'] if item['criminal_history'] else ''}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Description of Criminal History</div>\
                <div class='details_record_data'>{item['criminal_history']['description'] if item['criminal_history'] else ''}</div>\
            </div>\
        </div>"
        content += "<div class='details_title'>Record Data</div>"
        content += f"<div class='details_table'>\
            <div class='details_record'>\
                <div class='details_record_label'>Added User</div>\
                <div class='details_record_data'>{created_by}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Added Time</div>\
                <div class='details_record_data'>{item['created_time'].strftime('%m/%d/%Y %I:%M %p')}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Modified User</div>\
                <div class='details_record_data'>{updated_by}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>Modified Time</div>\
                <div class='details_record_data'>{item['updated_time'].strftime('%m/%d/%Y %I:%M %p')}</div>\
            </div>\
            <div class='details_record'>\
                <div class='details_record_label'>ID</div>\
                <div class='details_record_data'>{contact['uid']}</div>\
            </div>\
        <div>"
        return content
