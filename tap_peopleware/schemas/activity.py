"""Schema definitions for activity objects."""

from singer_sdk import typing as th

ActivityObject = th.PropertiesList(
    th.Property("absence_coverage", th.BooleanType),
    th.Property("allow_as_fullday", th.BooleanType),
    th.Property("allow_overstaffing", th.BooleanType),
    th.Property("child_activity_ids", th.ArrayType(th.IntegerType)),
    th.Property("color", th.IntegerType),
    th.Property("comply_with_rest_period", th.BooleanType),
    th.Property("day_status", th.BooleanType),
    th.Property("deleted", th.BooleanType),
    th.Property("exchangeable", th.BooleanType),
    th.Property("activity_id", th.IntegerType),
    th.Property("importance", th.NumberType),
    th.Property("name", th.StringType),
    th.Property("name_short", th.StringType),
    th.Property("official_name", th.StringType),
    th.Property("official_name_short", th.StringType),
    th.Property("paid", th.BooleanType),
    th.Property("planable", th.BooleanType),
    th.Property("replaceable", th.BooleanType),
    th.Property("replacement_activity_id_for_holidays", th.IntegerType),
    th.Property("replacement_activity_id_for_unscheduled_days", th.IntegerType),
    th.Property("requestable", th.BooleanType),
    th.Property("scheduling_priority", th.IntegerType),
    th.Property("third_party_interface", th.StringType),
    th.Property("third_party_type", th.IntegerType),
    th.Property(
        "type",
        th.StringType,
    ),  # absence, break, holiday, illness, meeting, present
)
