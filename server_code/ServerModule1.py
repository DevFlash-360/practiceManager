import anvil.secrets
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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
def get_events_filter(start_time, end_time, case_ids, staff_ids):
    if case_ids:
        cases = [case for case in app_tables.cases.search(uid=q.any_of(*case_ids))]
    else:
        cases = [case for case in app_tables.cases.search()]
    if staff_ids:
        staffs = [[staff] for staff in app_tables.staff.search(uid=q.any_of(*staff_ids))]
    else:
        staffs = [[staff] for staff in app_tables.staff.search()]
    events = app_tables.events.search(
        case=q.any_of(*cases),
        staff=q.any_of(*staffs),
        start_time=q.greater_than(start_time),
        end_time=q.less_than(end_time)
    )
    return events

@anvil.server.callable
def get_tasks_filter(start_time, end_time, case_ids, staff_ids, completed = [True, False, None]):
    if case_ids:
        cases = [case for case in app_tables.cases.search(uid=q.any_of(*case_ids))]
    else:
        cases = [case for case in app_tables.cases.search()]
    if staff_ids:
        staffs = [[staff] for staff in app_tables.staff.search(uid=q.any_of(*staff_ids))]
    else:
        staffs = [[staff] for staff in app_tables.staff.search()]
    # case_ids.append(None)
    # staff_ids.append([None])   
    tasks = app_tables.tasks.search(
        case=q.any_of(*cases),
        assigned_staff=q.any_of(*staffs),
        due_date=q.all_of(q.greater_than_or_equal_to(start_time.date()), q.less_than_or_equal_to(end_time.date())),
        completed=q.any_of(*completed)
    )
    return tasks