"""Peopleware tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
from typing_extensions import override

from tap_peopleware import streams


class TapPeopleware(Tap):
    """Peopleware tap class."""

    name = "tap-peopleware"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Auth Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType(nullable=True),
            description="The earliest record date to sync",
        ),
    ).to_dict()

    @override
    def discover_streams(self):
        return [
            streams.ActivityStream(self),
            streams.ContractStream(self),
            streams.PlanningUnitStream(self),
            streams.EmployeeStream(self),
            streams.EmployeeContractStream(self),
            streams.EmployeePlanningUnitStream(self),
            streams.EmployeeScheduleStream(self),
        ]


if __name__ == "__main__":
    TapPeopleware.cli()
