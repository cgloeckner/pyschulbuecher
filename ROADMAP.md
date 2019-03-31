replace hardcoded voluntary subjects (admin.py, demand_form.tpl)
	--> Subject.voluntary : bool

convert demand.json stuff to separate class
	with getter and setter handling type conversions (grade as int, not as str)

unittest ./ db / loans.py -> countWorstCase()

unittest ./ classes.py -> *


Write Queries as Usecase Functions
	db/loans.py --> loaning stuff (all about loans)

Unit Test Usecase Functions
	(actual ORM needs only minimal test referring DB-Creation)

Web API (further milestones tba)
