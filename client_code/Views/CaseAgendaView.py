import anvil.server
import uuid
from anvil.js.window import ej, jQuery
from DevFusion.components.GridView2 import GridView2
from datetime import datetime, date
import anvil.js
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Staff, Case, Task, Activity, User


class CaseAgendaView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.cases_element_id = f"cases_{uuid.uuid4()}"
        self.updates_element_id = f"updates_{uuid.uuid4()}"

        data = [{
                'OrderID': 10248, 'CustomerID': 'VINET', 'Role': 'Admin', 'EmployeeID': 5,
                'ShipName': 'Vins et alcools Chevalier', 'ShipCity': 'Reims', 'ShipAddress': '59 rue de l Abbaye',
                'ShipRegion': 'CJ', 'Mask': '1111','ShipPostalCode': '51100', 'ShipCountry': 'France', 'Freight': 32.38, 'Verified': 0
            },
            {
                'OrderID': 10249, 'CustomerID': 'TOMSP', 'Role': 'Employee', 'EmployeeID': 6,
                'ShipName': 'Toms Spezialitäten', 'ShipCity': 'Münster', 'ShipAddress': 'Luisenstr. 48',
                'ShipRegion': 'CJ',  'Mask': '2222', 'ShipPostalCode': '44087', 'ShipCountry': 'Germany', 'Freight': 11.61, 'Verified': 1
            }
        ]
        arts = ["Artwork", "Abstract", "Modern Painting", "Ceramics", "Animation Art", "Oil Painting"]
        self.case_list = ej.grids.Grid({
            'dataSource': data,
            'columns': [
                { 'field': 'OrderID', 'headerText': 'Order ID', 'textAlign': 'Right', 'width': 120, 'type': 'number' },
                { 'field': 'CustomerID', 'width': 140, 'headerText': 'Customer ID', 'type': 'string' },
                { 'field': 'Freight', 'headerText': 'Freight', 'textAlign': 'Right', 'width': 120, 'format': 'C' },
            ]
        })

        self.case_updates = ej.lists.ListView({
            'dataSource': arts
        })

    def form_show(self):
        self.container_el.innerHTML = f'\
            <div>\
                <div id="{self.cases_element_id}" style="display: inline-block;flex:0 0 60%; border-right-style:solid; border-width: 1px; border-color: #E9EDF2;">\
                </div>\
                <div id="{self.updates_element_id}" style="display:inline-block;">\
                </div>\
            </div>'
        self.case_list.appendTo(f"#{self.cases_element_id}")
        self.case_updates.appendTo(f"#{self.updates_element_id}")
