import anvil.server
from AnvilFusion.datamodel.particles import model_type, Attribute, Relationship, Computed
from AnvilFusion.datamodel import types
from datetime import date
import math

# Model list for enumerations
ENUM_MODEL_LIST = {
	'Activity': {'model': 'Activity', 'text_field': 'name'},
	'BankAccount': {'model': 'BankAccount', 'text_field': 'account_type.name'},
	'BankAccountType': {'model': 'BankAccountType', 'text_field': 'name'},
	'Branch': {'model': 'Branch', 'text_field': 'name'},
	'CaseStage': {'model': 'CaseStage', 'text_field': 'name'},
	'CaseStatus': {'model': 'CaseStatus', 'text_field': 'name'},
	'CauseOfAction': {'model': 'CauseOfAction', 'text_field': 'cause_of_action'},
	'ContactGroup': {'model': 'ContactGroup', 'text_field': 'name'},
	'ContactRole': {'model': 'ContactRole', 'text_field': 'name'},
	'EntityType': {'model': 'EntityType', 'text_field': 'name'},
	'FeeType': {'model': 'FeeType', 'text_field': 'name'},
	'LeadSource': {'model': 'LeadSource', 'text_field': 'name'},
	'PracticeArea': {'model': 'PracticeArea', 'text_field': 'name'},
	'StaffGroup': {'model': 'StaffGroup', 'text_field': 'name'},
	'StaffPayType': {'model': 'StaffPayType', 'text_field': 'name'},
	'TypeOfAction': {'model': 'TypeOfAction', 'text_field': 'name'},
}


# --------------------------------
# Application object model classes
# --------------------------------
@model_type
class Tenant:
	_model_type = types.ModelTypes.SYSTEM
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class User:
	_model_type = types.ModelTypes.SYSTEM
	_title = 'email'
	email = Attribute(field_type=types.FieldTypes.EMAIL)
	enabled = Attribute(field_type=types.FieldTypes.BOOLEAN)
	last_login = Attribute(field_type=types.FieldTypes.DATETIME)
	password_hash = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	n_password_failures = Attribute(field_type=types.FieldTypes.NUMBER)
	confirmed_email = Attribute(field_type=types.FieldTypes.BOOLEAN)
	signed_up = Attribute(field_type=types.FieldTypes.DATETIME)
	permissions = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class UserProfile:
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	title = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class AppAuditLog:
	_model_type = types.ModelTypes.SYSTEM
	table_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	record_uid = Attribute(field_type=types.FieldTypes.UID)
	action_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	action_time = Attribute(field_type=types.FieldTypes.DATETIME)
	action_by = Attribute(field_type=types.FieldTypes.UID)
	previous_state = Attribute(field_type=types.FieldTypes.OBJECT)
	new_state = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class AppErrorLog:
	_model_type = types.ModelTypes.SYSTEM
	component = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	action = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	error_message = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	error_time = Attribute(field_type=types.FieldTypes.DATETIME)
	user_uid = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
# class AppGridView:
#     name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
#     config = Attribute(field_type=types.FieldTypes.OBJECT)
#     permissions = Attribute(field_type=types.FieldTypes.OBJECT)
class AppGridView:
	_title = "name"
	model_type = types.ModelTypes.SYSTEM
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	model = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	columns = Attribute(field_type=types.FieldTypes.OBJECT)
	config = Attribute(field_type=types.FieldTypes.OBJECT)
	permissions = Attribute(field_type=types.FieldTypes.OBJECT)
	owner = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class File:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	mime_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	size = Attribute(field_type=types.FieldTypes.NUMBER)
	meta_info = Attribute(field_type=types.FieldTypes.OBJECT)
	content = Attribute(field_type=types.FieldTypes.MEDIA)
	case_uid = Attribute(field_type=types.FieldTypes.UID)
	link_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	link_uid = Attribute(field_type=types.FieldTypes.UID)


# -------------------------
# Data object model classes
# -------------------------
@model_type
class Activity:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Assistant:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	openai_id = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class BankAccount:
	_title = 'account_type'

	account_type = Relationship('BankAccountType')
	bank_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	routing_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	account_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	account_balance = Attribute(field_type=types.FieldTypes.CURRENCY)
	payment_link = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	"""Hidden Fields"""
	fractional_routing_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	check_start_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class BankAccountType:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Branch:
	_title = 'name'

	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	address = Attribute(field_type=types.FieldTypes.MULTI_LINE)


@model_type
class Case:
	_title = 'case_name'

	case_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	assigned_attorneys = Relationship('Staff', with_many=True)
	practice_area = Relationship('PracticeArea')
	case_stage = Relationship('CaseStage')
	cause_of_action = Relationship('CauseOfAction', with_many=True)
	close_date = Attribute(field_type=types.FieldTypes.DATE)
	"""Hidden Fields (should be displayed on Case Dashboard - in order of Case Dashboard template - not the order listed below)"""
	case_status = Relationship('CaseStatus')
	statute_of_limitations = Attribute(field_type=types.FieldTypes.DATE)
	court = Relationship('Entity')
	department = Relationship('Contact')
	case_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	incident_date = Attribute(field_type=types.FieldTypes.DATE)
	incident_location = Attribute(field_type=types.FieldTypes.ADDRESS)
	case_description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	next_case_search = Attribute(field_type=types.FieldTypes.DATE)
	clients = Relationship('Client', with_many=True)
	contacts = Relationship('Contact', with_many=True)
	staff = Relationship('Staff', with_many=True)
	share_case_information_with = Relationship('Contact')
	lead = Relationship('Lead')
	# billing
	fee_type = Relationship('FeeType')
	flat_fee_retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	hourly_retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	pre_litigation_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	litigation_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	trial_included = Attribute(field_type=types.FieldTypes.BOOLEAN)
	retainer_hours_limit = Attribute(field_type=types.FieldTypes.NUMBER)
	investigator = Attribute(field_type=types.FieldTypes.BOOLEAN)
	investigator_budget = Attribute(field_type=types.FieldTypes.CURRENCY)
	record_seal_expungement = Attribute(field_type=types.FieldTypes.BOOLEAN)
	# open date - date from created_time field
	"""
  The fields below should be relational to Clients - in Creator this information gets populated based on the 
  Group selection of each contact. I don't think we need actual need the fields below - we just need to fetch
  the data to display on the case dashboard.
  """
	# client_in_custody = Attribute(field_type=types.FieldTypes.BOOLEAN)
	# jail_prison = Relationship('Entity')
	# inmate_id = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	# bail_status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class CaseContact:
	_title = 'contact'

	case = Relationship('Case')
	contact = Relationship('Contact')
	role = Relationship('ContactRole')


@model_type
class CaseRequirement:
	_title = 'name'

	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	case = Relationship('Case')
	notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	url = Attribute(field_type=types.FieldTypes.HYPERLINK)
	due_date = Attribute(field_type=types.FieldTypes.DATE)
	completed = Attribute(field_type=types.FieldTypes.BOOLEAN)


@model_type
class CaseStage:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class CaseStatus:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class CaseUpdate:
	_title = 'name'

	case = Relationship('Case')
	next_activity = Relationship('Activity')
	next_date = Attribute(field_type=types.FieldTypes.DATETIME)
	todays_update = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	client_attendance_required = Attribute(field_type=types.FieldTypes.BOOLEAN)
	client_update = Attribute(field_type=types.FieldTypes.BOOLEAN)


@model_type
class CaseWorkflow:
	_title = 'name'
	
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	practice_area = Relationship('PracticeArea')
	
	# @staticmethod
	# def get_items(args):
	#     print('get_items', args)
	#     if args['uid']:
	#         items = [item['activity']['name'] for item in CaseWorkflowItem.search(case_workflow=args['uid'])]
	#     else:
	#         items = []
	#     return items
	# items = Computed(('uid',), 'get_items')


@model_type
class CaseWorkflowItem:
	_title = 'item_name'
	
	case_workflow = Relationship('CaseWorkflow')
	type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
	activity = Relationship('Activity')
	related_task = Relationship('CaseWorkflowItem')
	due_date_base = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
	duration = Attribute(field_type=types.FieldTypes.NUMBER)
	assigned_to = Relationship('Staff', with_many=True)
	priority = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
	notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	documents = Attribute(field_type=types.FieldTypes.FILE_UPLOAD)
	
	@staticmethod
	def get_item_name(args):
		print('get_item_name', args)
		workflow = args['case_workflow'].get('name', '') if args.get('case_workflow', None) else ''
		activity = args['activity'].get('name', '') if args.get('activity', None) else ''
		return f"{workflow} - {activity}"
	item_name = Computed(('case_workflow', 'activity'), 'get_item_name')


@model_type
class CauseOfAction:
	_title = 'cause_of_action'
	_table_name = 'causes_of_action'

	type_of_action = Relationship('TypeOfAction')
	statute_id = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	cause_of_action = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	penalty = Attribute(field_type=types.FieldTypes.MULTI_LINE)


@model_type
class Check:
	_title = 'check_number'

	check_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	date = Attribute(field_type=types.FieldTypes.DATE)
	payee = Relationship('Contact')
	amount = Attribute(field_type=types.FieldTypes.CURRENCY)
	memo = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	reference = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	"""Hidden Fields and or detail view"""
	bank_account = Relationship('BankAccount')


@model_type
class Client:
	_title = 'client_name'

	client_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	# need to display group as "Client" if all clients and contacts will be on same report
	# email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	# mobile_phone= Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	# work_phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	# cases = Relationship('Case')
	"""Hidden Fields and or detail view"""
	is_individual = Attribute(field_type=types.FieldTypes.BOOLEAN)
	contact = Relationship('Contact')
	entity = Relationship('Entity')


@model_type
class Contact:
	_title = 'full_name'

	contact_group = Relationship('ContactGroup')
	entity = Relationship('Entity')
	first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	mobile_phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	work_phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	alternate_phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	title_position = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	"""Hidden Fields and or detail view"""

	personal_details_schema = {
		'dob': Attribute(field_type=types.FieldTypes.DATE),
		'ssn': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'country_of_citizenship': Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
		'native_language': Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
		'education': Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
	}
	personal_details = Attribute(field_type=types.FieldTypes.OBJECT, schema=personal_details_schema)

	address_schema = {
		'address_line_1': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'address_line_2': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'city_district': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'state_province': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'postal_code': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
	}
	address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)

	employment_schema = {
		'employment': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'current_employer': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'time_with_current_employer': Attribute(field_type=types.FieldTypes.SINGLE_LINE,
												label='Time with Current Employer'),
	}
	employment = Attribute(field_type=types.FieldTypes.OBJECT, schema=employment_schema)

	criminal_history_schema = {
		'criminal_history': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'description': Attribute(field_type=types.FieldTypes.MULTI_LINE),
	}
	criminal_history = Attribute(field_type=types.FieldTypes.OBJECT, schema=criminal_history_schema)

	additional_info_schema = {
		'family_support': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
		'source_of_funds': Attribute(field_type=types.FieldTypes.SINGLE_LINE, label='Source of Funds'),
		'community_service': Attribute(field_type=types.FieldTypes.SINGLE_LINE),
	}
	additional_info = Attribute(field_type=types.FieldTypes.OBJECT, schema=additional_info_schema)

	department = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	courtroom = Attribute(field_type=types.FieldTypes.SINGLE_LINE)

	@staticmethod
	def get_full_name(args):
		return f"{args['first_name']} {args['last_name']}"
	
	@staticmethod
	def get_department_desc(args):
		return f"{args['department']}/{args['courtroom']} - {args['last_name']}"
	full_name = Computed(('first_name', 'last_name'), 'get_full_name')
	department_desc = Computed(('department', 'courtroom', 'last_name'), 'get_department_desc')


@model_type
class ContactGroup:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class ContactRole:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Document:
	_title = 'title'
	title = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	case = Relationship('Case')
	folder = Relationship('DocumentFolder')
	type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
	discovery = Attribute(field_type=types.FieldTypes.BOOLEAN)
	reviewed_by = Relationship('Staff')
	notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	file = Attribute(field_type=types.FieldTypes.FILE_UPLOAD)
	media = Attribute(field_type=types.FieldTypes.MEDIA)

@model_type
class DocumentFolder:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	case = Relationship('Case')
	# parent_folder = Relationship('DocumentFolder')


@model_type
class Entity:
	_title = 'name'

	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	entity_type = Relationship('EntityType')
	phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	address = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	website = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	primary_contact = Relationship('Contact')


@model_type
class EntityType:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Event:
	_title = 'activity'

	start_time = Attribute(field_type=types.FieldTypes.DATETIME)
	end_time = Attribute(field_type=types.FieldTypes.DATETIME)
	case = Relationship('Case')
	activity = Relationship('Activity')
	staff = Relationship('Staff', with_many=True)
	location = Relationship('Entity')
	department = Relationship('Contact')
	client_attendance_required = Attribute(field_type=types.FieldTypes.BOOLEAN)
	"""Hidden Fields and or detail view"""
	no_case = Attribute(field_type=types.FieldTypes.BOOLEAN)
	notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	documents = Attribute(field_type=types.FieldTypes.FILE_UPLOAD)
	contact = Relationship('Contact', with_many=True)
	client_update = Attribute(field_type=types.FieldTypes.BOOLEAN)


@model_type
class Expense:
	_title = 'description'

	date = Attribute(field_type=types.FieldTypes.DATE)
	activity = Relationship('Activity')
	description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	amount = Attribute(field_type=types.FieldTypes.CURRENCY)
	quantity = Attribute(field_type=types.FieldTypes.NUMBER)
	total = Attribute(field_type=types.FieldTypes.CURRENCY)
	staff = Relationship('Staff')
	case = Relationship('Case')
	invoice = Relationship('Invoice')
	"""Hidden Fields and or detail view"""
	billable = Attribute(field_type=types.FieldTypes.BOOLEAN)
	reduction = Attribute(field_type=types.FieldTypes.NUMBER)
	receipt_invoice = Attribute(field_type=types.FieldTypes.FILE_UPLOAD)
	
	@staticmethod
	def get_status(args):
		try:
			if args['invoice']['uid']:
				status = 'Invoiced'
			else:
				status = 'Open'
		except Exception:
			status = 'Open'
		return status
	status = Computed(['invoice'], 'get_status')


@model_type
class FeeType:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Invoice:
	_title = 'invoice_number'

	invoice_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	case = Relationship('Case')
	bill_to = Relationship('Contact')
	total = Attribute(field_type=types.FieldTypes.CURRENCY)
	balance_due = Attribute(field_type=types.FieldTypes.CURRENCY)
	status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	"""Theses fields should be relational to the case and displayed on the invoice template"""
	adjustments = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class Lead:
	_title = 'case_name'

	"""We need Kanban style report for leads - I've separated the
  fields below based on a 'card view' and 'detail view' on kanban"""
	"""Card View"""
	case_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	"""Detail View"""
	lead_status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	intake_staff = Relationship('Staff', with_many=True)
	lead_source = Relationship('LeadSource')
	referred_by = Relationship('Contact', with_many=True)
	fee_type = Relationship('FeeType')
	trial_included = Attribute(field_type=types.FieldTypes.BOOLEAN)
	retainer_hour_limit = Attribute(field_type=types.FieldTypes.DECIMAL)
	investigator_budget = Attribute(field_type=types.FieldTypes.CURRENCY)
	record_seal_expungement_included = Attribute(field_type=types.FieldTypes.BOOLEAN)
	practice_area = Relationship('PracticeArea')
	case_stage = Relationship('CaseStage')
	cause_of_action = Relationship('CauseOfAction', with_many=True)
	statute_of_limitations = Attribute(field_type=types.FieldTypes.DATE)
	court = Relationship('Entity')
	department = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	case_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	incident_date = Attribute(field_type=types.FieldTypes.DATE)
	incident_location = Attribute(field_type=types.FieldTypes.ADDRESS)
	case_description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	contacts = Relationship('Contact', with_many=True)
	# billing
	fee_type = Relationship('FeeType')
	flat_fee_retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	hourly_retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	pre_litigation_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	litigation_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	trial_included = Attribute(field_type=types.FieldTypes.BOOLEAN)
	retainer_hours_limit = Attribute(field_type=types.FieldTypes.NUMBER)
	investigator = Attribute(field_type=types.FieldTypes.BOOLEAN)
	investigator_budget = Attribute(field_type=types.FieldTypes.CURRENCY)
	record_seal_expungement = Attribute(field_type=types.FieldTypes.BOOLEAN)


@model_type
class LeadActivity:
	_title = 'activity'

	lead = Relationship('Lead')
	activity = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	due_time = Attribute(field_type=types.FieldTypes.DATETIME)
	status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Settings:
	_title = 'case_name'

	"""We need Kanban style report for leads - I've separated the
  fields below based on a 'card view' and 'detail view' on kanban"""
	"""Card View"""
	case_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	"""Detail View"""
	lead_status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	intake_staff = Relationship('Staff', with_many=True)
	lead_source = Relationship('LeadSource')
	referred_by = Relationship('Contact', with_many=True)
	fee_type = Relationship('FeeType')
	trial_included = Attribute(field_type=types.FieldTypes.BOOLEAN)
	retainer_hour_limit = Attribute(field_type=types.FieldTypes.DECIMAL)
	investigator_budget = Attribute(field_type=types.FieldTypes.CURRENCY)
	record_seal_expungement_included = Attribute(field_type=types.FieldTypes.BOOLEAN)
	practice_area = Relationship('PracticeArea')
	case_stage = Relationship('CaseStage')
	cause_of_action = Relationship('CauseOfAction', with_many=True)
	statute_of_limitations = Attribute(field_type=types.FieldTypes.DATE)
	court = Relationship('Entity')
	department = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	case_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	incident_date = Attribute(field_type=types.FieldTypes.DATE)
	incident_location = Attribute(field_type=types.FieldTypes.ADDRESS)
	case_description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	contacts = Relationship('Contact', with_many=True)
	# billing
	fee_type = Relationship('FeeType')
	flat_fee_retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	hourly_retainer = Attribute(field_type=types.FieldTypes.CURRENCY)
	pre_litigation_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	litigation_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	trial_included = Attribute(field_type=types.FieldTypes.BOOLEAN)
	retainer_hours_limit = Attribute(field_type=types.FieldTypes.NUMBER)
	investigator = Attribute(field_type=types.FieldTypes.BOOLEAN)
	investigator_budget = Attribute(field_type=types.FieldTypes.CURRENCY)
	record_seal_expungement = Attribute(field_type=types.FieldTypes.BOOLEAN)


@model_type
class SettingsUserlist:
	_title = 'activity'

	settings = Relationship('Settings')
	activity = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	due_time = Attribute(field_type=types.FieldTypes.DATETIME)
	status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class LeadSource:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Ledger:
	_title = 'transaction_time'
	_table_name = 'ledger'
	transaction_time = Attribute(field_type=types.FieldTypes.DATETIME)


@model_type
class Payment:
	_title = 'amount'

	case = Relationship('Case')
	invoice = Relationship('Invoice')
	bank_account = Relationship('BankAccount')
	amount = Attribute(field_type=types.FieldTypes.CURRENCY)
	payment_method = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	payment_time = Attribute(field_type=types.FieldTypes.DATETIME)
	status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class PracticeArea:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Staff:
	_title = 'full_name'
	_table_name = 'staff'

	user = Relationship('User')
	branch = Relationship('Branch')
	first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	staff_group = Relationship('StaffGroup')
	pay_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	work_phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	extension = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	mileage_reimbursement = Attribute(field_type=types.FieldTypes.CURRENCY)
	hire_date = Attribute(field_type=types.FieldTypes.DATE)
	leave_date = Attribute(field_type=types.FieldTypes.DATE)
	"""Detail View"""
	user_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	work_email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	enable_overtime = Attribute(field_type=types.FieldTypes.BOOLEAN)
	overtime_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	weekly_base_hours = Attribute(field_type=types.FieldTypes.DECIMAL)
	enable_break_time_deduction = Attribute(field_type=types.FieldTypes.BOOLEAN)
	break_time_hour_base = Attribute(field_type=types.FieldTypes.DECIMAL)
	break_time_rate = Attribute(field_type=types.FieldTypes.DECIMAL)
	enable_performance_incentives = Attribute(field_type=types.FieldTypes.BOOLEAN)
	intake_performance_incentive = Attribute(field_type=types.FieldTypes.DECIMAL)
	override_incentive = Attribute(field_type=types.FieldTypes.DECIMAL)
	manager_incentive = Attribute(field_type=types.FieldTypes.DECIMAL)
	referral_incentive = Attribute(field_type=types.FieldTypes.DECIMAL)
	employment_status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	manager = Relationship('Staff')
	bar_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	bar_state = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	bar_admission = Attribute(field_type=types.FieldTypes.DATE)
	date_of_birth = Attribute(field_type=types.FieldTypes.DATE)
	personal_phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	personal_email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	personal_address = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	personal_ssn = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	personal_gender = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	personal_race = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	bank_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	bank_routing_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	bank_account_number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	emergency_contact_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	emergency_contact_phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	emergency_contact_email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	emergency_contact_address = Attribute(field_type=types.FieldTypes.SINGLE_LINE)

	@staticmethod
	def get_full_name(args):
		return f"{args['first_name']} {args['last_name']}"

	full_name = Computed(('first_name', 'last_name'), 'get_full_name')


@model_type
class StaffGroup:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class StaffPayType:
	_title = 'name'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Task:
	_title = 'activity'

	case = Relationship('Case')
	activity = Relationship('Activity')
	due_date = Attribute(field_type=types.FieldTypes.DATE)
	priority = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	assigned_staff = Relationship('Staff', with_many=True)
	notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	"""Detail View"""
	documents = Attribute(field_type=types.FieldTypes.FILE_UPLOAD)
	completed = Attribute(field_type=types.FieldTypes.BOOLEAN)

	@staticmethod
	def get_due_date_view(args):
		if not args['due_date']: 
			due_date_view = 'No Due Date'
		elif args['due_date'] < date.today():
			due_date_view = 'OVERDUE'
		else:
			due_date = args['due_date'].strftime("%a, %b %d").replace(" 0", " ")
			due_in = (args['due_date'] - date.today()).days
			if due_in == 0:
				due_date_view = f"Due {due_date} - today"
			elif due_in == 1:
				due_date_view = f"Due {due_date} - tomorrow"
			else:
				due_date_view = f"Due {due_date} in {(args['due_date'] - date.today()).days} days"
		return due_date_view
	due_date_view = Computed(['due_date'], 'get_due_date_view')

	@staticmethod
	def get_due_date_days(args):
		if args['due_date']:
			due_date_days = (args['due_date'] - date.today()).days
		else:
			due_date_days = math.inf
		if due_date_days < 0:
			due_date_days = -100
		return due_date_days
	due_date_days = Computed(['due_date'], 'get_due_date_days')


@model_type
class TimeEntry:
	_title = 'activity'

	date = Attribute(field_type=types.FieldTypes.DATE)
	activity = Relationship('Activity')
	duration = Attribute(field_type=types.FieldTypes.DECIMAL)
	description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	rate = Attribute(field_type=types.FieldTypes.CURRENCY)
	total = Attribute(field_type=types.FieldTypes.CURRENCY)
	staff = Relationship('Staff')
	case = Relationship('Case')
	invoice = Relationship('Invoice')
	"""Detail View"""
	billable = Attribute(field_type=types.FieldTypes.BOOLEAN)
	rate_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	@staticmethod
	def get_status(args):
		try:
			if args['invoice']['uid']:
				status = 'Invoiced'
			else:
				status = 'Open'
		except Exception:
			status = 'Open'
		return status
	status = Computed(['invoice'], 'get_status')


@model_type
class Timesheet:
	_title = 'staff'

	staff = Relationship('Staff')
	clock_in_time = Attribute(field_type=types.FieldTypes.DATETIME)
	clock_out_time = Attribute(field_type=types.FieldTypes.DATETIME)
	hours_worked = Attribute(field_type=types.FieldTypes.DECIMAL)
	earned_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
	approved_by = Relationship('Staff')
	payroll = Relationship('Payroll')
	
	@staticmethod
	def get_status(args):
		try:
			if args['payroll']['uid']:
				status = 'Invoiced'
			else:
				status = 'Open'
		except Exception:
			status = 'Open'
		return status
	status = Computed(['payroll'], 'get_status')


@model_type
class TypeOfAction:
	_title = 'name'
	_table_name = 'types_of_action'
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class PerformanceIncentive:
	_title = 'Performance Incentives'
	
	staff = Relationship('Staff')
	amount = Attribute(field_type=types.FieldTypes.CURRENCY)
	payment = Relationship('Payment')
	payment_date = Attribute(field_type=types.FieldTypes.DATETIME)
	payroll = Relationship('Payroll')

	@staticmethod
	def get_status(args):
		try:
			if args['payroll']['uid']:
				status = 'Invoiced'
			else:
				status = 'Open'
		except Exception:
			status = 'Open'
		return status
	status = Computed(['payroll'], 'get_status')


@model_type
class ReimbursementRequest:
	_title = 'Request Reimbursement'

	staff = Relationship('Staff')
	quantity = Attribute(field_type=types.FieldTypes.NUMBER)
	amount = Attribute(field_type=types.FieldTypes.CURRENCY)
	total = Attribute(field_type=types.FieldTypes.CURRENCY)
	description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
	add_to_case = Attribute(field_type=types.FieldTypes.BOOLEAN)
	date = Attribute(field_type=types.FieldTypes.DATE)
	activity = Relationship('Activity')
	case = Relationship('Case')
	receipt_invoice = Relationship('Invoice')
	approved_by = Relationship('Staff')
	payroll = Relationship('Payroll')

	@staticmethod
	def get_status(args):
		try:
			if args['payroll']['uid']:
				status = 'Invoiced'
			else:
				status = 'Open'
		except Exception:
			status = 'Open'
		return status
	status = Computed(['payroll'], 'get_status')


@model_type
class TimeOffRequest:
	_title = 'Time-Off Request'
	
	staff = Relationship('Staff')
	reason = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	date_of_return = Attribute(field_type=types.FieldTypes.DATE)
	date_of_leave = Attribute(field_type=types.FieldTypes.DATE)
	status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)

	
@model_type
class Payroll:
	_title = 'staff'

	start = Attribute(field_type=types.FieldTypes.DATE)
	end = Attribute(field_type=types.FieldTypes.DATE)
	staffs = Relationship('Staff', with_many=True)
	total_payroll = Attribute(field_type=types.FieldTypes.CURRENCY)


@model_type
class PayrollTotal:
	_title = 'Payroll Total'

	payroll = Relationship('Payroll')
	staff = Relationship('Staff')
	total_base_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
	total_overtime_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
	total_incentive_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
	total_reimbursement_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
	total_pay = Attribute(field_type=types.FieldTypes.CURRENCY)


@model_type
class Signature:
	_title = "Signature"
	
	name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
	file = Attribute(field_type=types.FieldTypes.MEDIA)
