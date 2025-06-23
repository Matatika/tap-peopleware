"""Schema definitions for planning unit objects."""

from singer_sdk import typing as th

PlanningUnitObject = th.PropertiesList(
    th.Property("color", th.IntegerType),
    th.Property("deleted", th.BooleanType),
    th.Property("planning_unit_id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("name_short", th.StringType),
    th.Property("parent_planning_unit_id", th.IntegerType),
    th.Property("planning_raster", th.IntegerType),
    th.Property("time_zone_id", th.IntegerType),
)
