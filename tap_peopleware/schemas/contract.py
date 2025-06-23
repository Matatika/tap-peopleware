"""Schema definitions for contract objects."""

from singer_sdk import typing as th

_AmountType = th.ObjectType(
    th.Property("minimum", th.IntegerType),
    th.Property("target", th.IntegerType),
    th.Property("maximum", th.IntegerType),
)

ContractObject = th.PropertiesList(
    th.Property("deleted", th.BooleanType),
    th.Property("employment_type", th.StringType),  # employed, unknown
    th.Property("color", th.IntegerType),
    th.Property("contract_id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("name_short", th.StringType),
    th.Property(
        "working_amount",
        th.ObjectType(
            th.Property("per_day", _AmountType),
            th.Property("per_week", _AmountType),
            th.Property("per_month", _AmountType),
            th.Property("per_year", _AmountType),
        ),
    ),
    th.Property(
        "working_hours",
        th.ObjectType(
            th.Property("monday", th.IntegerType),
            th.Property("tuesday", th.IntegerType),
            th.Property("wednesday", th.IntegerType),
            th.Property("thursday", th.IntegerType),
            th.Property("friday", th.IntegerType),
            th.Property("saturday", th.IntegerType),
            th.Property("sunday", th.IntegerType),
        ),
    ),
    th.Property("working_days_per_week", th.NumberType),
)
