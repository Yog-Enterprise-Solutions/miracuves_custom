__version__ = "0.0.1"

try:
	from miracuves_custom.overrides.payroll_entry import apply as _apply_payroll_entry_overrides

	_apply_payroll_entry_overrides()
except ImportError:
	# hrms is not installed on this bench/site
	pass
