import anvil.secrets
import anvil.email
import anvil.users
import anvil.http
import anvil.media
import base64
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfWriter, PdfReader
import io

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_events_filter(start_time, end_time, case_ids, staff_ids, activity_ids):
    if case_ids:
        cases = [case for case in app_tables.cases.search(uid=q.any_of(*case_ids))]
    else:
        cases = [case for case in app_tables.cases.search()]
    if staff_ids:
        staffs = [[staff] for staff in app_tables.staff.search(uid=q.any_of(*staff_ids))]
    else:
        staffs = [[staff] for staff in app_tables.staff.search()]
    if activity_ids:
        activities = [activity for activity in app_tables.activities.search(uid=q.any_of(*activity_ids))]
    else:
        activities = [activity for activity in app_tables.activities.search()]
    events = app_tables.events.search(
        case=q.any_of(*cases),
        staff=q.any_of(*staffs),
        activity=q.any_of(*activities),
        start_time=q.greater_than(start_time),
        end_time=q.less_than(end_time)
    )
    return events

@anvil.server.callable
def get_tasks_filter(case_ids, staff_ids, activity_ids, start_time, end_time, completed = [True, False, None]):
    cases = []
    staffs = []
    activities = []
    if case_ids:
        cases = [case for case in app_tables.cases.search(uid=q.any_of(*case_ids))]
    if staff_ids:
        staffs = [[staff] for staff in app_tables.staff.search(uid=q.any_of(*staff_ids))]
    if activity_ids:
        activities = [activity for activity in app_tables.activities.search(uid=q.any_of(*activity_ids))]

    kwargs = {
        'completed': q.any_of(*completed)
    }
    if start_time and end_time:
        kwargs['due_date'] = q.all_of(q.greater_than_or_equal_to(start_time.date()), q.less_than_or_equal_to(end_time.date()))
    if cases:
        kwargs['case'] = q.any_of(*cases)
    if staffs:
        kwargs['assigned_staff'] = q.any_of(*staffs)
    if activities:
        kwargs['activity'] = q.any_of(*activities)
    tasks = app_tables.tasks.search(q.all_of(**kwargs))
    return tasks

@anvil.server.callable
def get_case_updates():
    cases = [case for case in app_tables.cases.search()]
    activities = [activity for activity in app_tables.activities.search()]
    case_updates = app_tables.case_updates.search(
        case=q.any_of(*cases),
        next_activity=q.any_of(*activities)
    )
    return case_updates

@anvil.server.http_endpoint('/sign/:sign_name')
def get_sign(sign_name):
  return app_tables.signature.get(name=sign_name)['file']

@anvil.server.callable
def load_signature(sign_name):
  url = f"{anvil.server.get_api_origin()}/sign/{sign_name}" 
  return url

@anvil.server.http_endpoint('/doc/:doc_uid')
def get_doc(doc_uid):
  return app_tables.documents.get(uid=doc_uid)['media']

@anvil.server.callable
def load_doc(doc_name):
  url = f"{anvil.server.get_api_origin()}/doc/{doc_name}" 
  return url

@anvil.server.callable
def add_image_to_pdf(doc_uid, signature_name, page_info, x, y):
    page_width = page_info[0]
    page_height = page_info[1]
    page_num = page_info[2] - 1
    # Retrieve the image from the data table
    image_row = app_tables.signature.get(name=signature_name)
    image = image_row['file']
    with anvil.media.TempFile(image) as image_path:
      image_reader = ImageReader(image_path)
      width, height = image_reader.getSize()
      draw_x = x
      draw_y = page_height - y - height
  
      # Retrieve the PDF from the data table
      pdf_row = app_tables.documents.get(uid=doc_uid)
      pdf = pdf_row['media']
      with anvil.media.TempFile(pdf) as pdf_path:
        # Read the existing PDF
        existing_pdf = PdfReader(pdf_path)
        output_pdf = PdfWriter()
        
        # Create a mask that specifies the transparent part of the image
        # Assuming that your image uses full transparency, where 0 is fully transparent and 255 is fully opaque
        # [x, y, x, y, x, y] where x and y repeats for the range of RGB values to be masked out (0-255 for fully transparent)
        transparency_mask = [0, 0, 0, 0, 0, 0]
        # Create a new PDF with the image using ReportLab
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        c.drawImage(image_reader, draw_x, draw_y, width, height, mask=transparency_mask, preserveAspectRatio=True)  # specify image position and size
        c.save()
        
        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        
        # Merge the image PDF with each page of the existing PDF
        # 0 - page_num-1: raw, page_num: with sign, page_num+1 - last: raw
        for i in range(0, page_num):
            page = existing_pdf.pages[i]
            output_pdf.add_page(page)
        
        page = existing_pdf.pages[page_num]
        page.merge_page(new_pdf.pages[0])
        output_pdf.add_page(page)
        
        for i in range(page_num+1, len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            output_pdf.add_page(page)
        
        
        # Buffer to store the output
        output_stream = io.BytesIO()
        output_pdf.write(output_stream)
        output_stream.seek(0)
        
        # Create a new media object for the merged PDF
        final_pdf = anvil.BlobMedia('application/pdf', output_stream.read(), name='merged_with_image.pdf')
        
        # Example of saving the merged PDF to a data table (optional)
        # app_tables.docs.add_row(name='merged_with_image.pdf', file=final_pdf)
        
        return final_pdf

