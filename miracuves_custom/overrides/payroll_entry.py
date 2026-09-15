import frappe
from hrms.payroll.doctype.payroll_entry.payroll_entry import (
	set_fields_to_select,
	set_filter_conditions,
	set_match_conditions,
	set_searchfield,
)


def get_filtered_employees(
	sal_struct,
	filters,
	searchfield=None,
	search_string=None,
	fields=None,
	as_dict=False,
	limit=None,
	offset=None,
	ignore_match_conditions=False,
) -> list:
	"""Same as hrms' get_filtered_employees, except the Employee status filter is
	controlled by Miracuves Settings instead of being hardcoded to exclude everyone
	other than "Inactive" employees.
	"""
	SalaryStructureAssignment = frappe.qb.DocType("Salary Structure Assignment")
	Employee = frappe.qb.DocType("Employee")

	excluded_statuses = ["Inactive"]
	if not frappe.db.get_single_value(
		"Miracuves Settings", "allow_suspended_employees_in_payroll"
	):
		excluded_statuses.append("Suspended")

	query = (
		frappe.qb.from_(Employee)
		.join(SalaryStructureAssignment)
		.on(Employee.name == SalaryStructureAssignment.employee)
		.where(
			(SalaryStructureAssignment.docstatus == 1)
			& (Employee.status.notin(excluded_statuses))
			& (Employee.company == filters.company)
			& ((Employee.date_of_joining <= filters.end_date) | (Employee.date_of_joining.isnull()))
			& ((Employee.relieving_date >= filters.start_date) | (Employee.relieving_date.isnull()))
			& (SalaryStructureAssignment.salary_structure.isin(sal_struct))
			& (SalaryStructureAssignment.payroll_payable_account == filters.payroll_payable_account)
			& (filters.end_date >= SalaryStructureAssignment.from_date)
		)
	)

	query = set_fields_to_select(query, fields)
	query = set_searchfield(query, searchfield, search_string, qb_object=Employee)
	query = set_filter_conditions(query, filters, qb_object=Employee)

	if not ignore_match_conditions:
		query = set_match_conditions(query=query, qb_object=Employee)

	if limit:
		query = query.limit(limit)

	if offset:
		query = query.offset(offset)

	return query.run(as_dict=as_dict)


def apply():
	from hrms.payroll.doctype.payroll_entry import payroll_entry

	payroll_entry.get_filtered_employees = get_filtered_employees
