import anvil.server
import json
import uuid
from anvil.js.window import ej, jQuery, XMLHttpRequest, Date
from AnvilFusion.tools.utils import datetime_js_to_py
from DevFusion.components.GridView2 import GridView2
from datetime import datetime, timedelta
import anvil.js
from AnvilFusion.tools.utils import AppEnv
from ..app.models import Staff, Case, Activity, Event, CaseUpdate
from ..Forms.EventForm import EventForm


class DateCalculatorView:
    def __init__(self, container_id, **kwargs):
        self.container_id = container_id or AppEnv.content_container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]

        self.date_picker_id = f"date_picker{uuid.uuid4()}"

        self.date_picker = ej.calendars.DatePicker()

    
    def form_show(self):
        self.container_el.innerHTML = f'\
            <div>
                <div id="{self.date_picker_id}">
                </div>
            </div>
            '
        self.date_picker.appendTo(jQuery(f"#{self.date_picker_id}")[0])
    
    def destroy(self):
        self.date_picker.destroy()
        if self.container_el:
            self.container_el.innerHTML = ''