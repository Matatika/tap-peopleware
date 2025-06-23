"""Schema definitions for employee objects."""

from singer_sdk import typing as th

EmployeeObject = th.PropertiesList(
    th.Property("birth_date", th.DateType),
    th.Property("birth_place", th.StringType),
    th.Property("color", th.IntegerType),
    th.Property("current_identification", th.StringType),
    th.Property("deleted", th.BooleanType),
    th.Property("employee_id", th.IntegerType),
    th.Property("first_name", th.StringType),
    th.Property("last_name", th.StringType),
    th.Property("personnel_number", th.StringType),
    th.Property("schedule_position", th.IntegerType),
    th.Property("automated_shift_assignment", th.BooleanType),
    th.Property("user_id", th.IntegerType),
)

EmployeeContractObject = th.PropertiesList(
    th.Property("employees_contract_id", th.IntegerType),
    th.Property("employee_id", th.IntegerType),
    th.Property("contract_id", th.IntegerType),
    th.Property("start_date", th.DateType),
    th.Property("end_date", th.DateType),
)

EmployeePlanningUnitObject = th.PropertiesList(
    th.Property("employees_membership_id", th.IntegerType),
    th.Property("employee_id", th.IntegerType),
    th.Property("planning_unit_id", th.IntegerType),
    th.Property("start_date", th.DateType),
    th.Property("end_date", th.DateType),
    th.Property("priority", th.IntegerType),

)

EmployeeScheduleObject = th.PropertiesList(
    th.Property("booking_date", th.DateType),
    th.Property("employee_id", th.IntegerType),
    th.Property(
        "level",
        th.StringType,
        allowed_values=(
            "plan",
            "wishes",
            "alternative_wishes",
            "absence_wishes",
            "final",
            "time_recording",
            "correction",
            "acd",
            "availabilities",
            "on_call",
            "productivity",
            "backup",
            "backup_version_2",
            "backup_version_3",
            "overtime",
        ),
    ),
    th.Property("planning_unit_id", th.IntegerType),
    th.Property(
        "schedule_blocks",
        th.ArrayType(
            th.ObjectType(
                th.Property("activity_id", th.IntegerType),
                th.Property("time_end", th.DateTimeType),
                th.Property("time_start", th.DateTimeType),
                th.Property("type", th.StringType),
            )
        ),
    ),
)
