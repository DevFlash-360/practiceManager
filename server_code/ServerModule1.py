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