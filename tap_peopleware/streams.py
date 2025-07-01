"""Stream type classes for tap-peopleware."""

from __future__ import annotations

from datetime import date
from http import HTTPStatus

import requests
from typing_extensions import override

from tap_peopleware.client import PeoplewareStream
from tap_peopleware.schemas.activity import ActivityObject
from tap_peopleware.schemas.contract import ContractObject
from tap_peopleware.schemas.employee import (
    EmployeeContractObject,
    EmployeeObject,
    EmployeePlanningUnitObject,
    EmployeeScheduleObject,
)
from tap_peopleware.schemas.planning_unit import PlanningUnitObject

API_MIN_DATE = date(1900, 1, 1)
API_MAX_DATE = date(4000, 1, 1)


class ResumableAPIError(Exception):
    def __init__(self, message: str, response: requests.Response) -> None:
        super().__init__(message)
        self.response = response


# https://legacy-api.peopleware.com/#tag/Activities/operation/getV1Activities
class ActivityStream(PeoplewareStream):
    """Define activity stream."""

    name = "activities"
    schema = ActivityObject.to_dict()
    primary_keys = ("activity_id",)
    path = "/activities"
    records_jsonpath = "$.activities[*]"


# https://legacy-api.peopleware.com/#tag/Contracts/operation/getV1Contracts
class ContractStream(PeoplewareStream):
    """Define contract stream."""

    name = "contracts"
    schema = ContractObject.to_dict()
    primary_keys = ("contract_id",)
    path = "/contracts"
    records_jsonpath = "$.contracts[*]"


# https://legacy-api.peopleware.com/#tag/Planning-Units/operation/getV1PlanningUnits
class PlanningUnitStream(PeoplewareStream):
    """Define planning unit stream."""

    name = "planning_units"
    schema = PlanningUnitObject.to_dict()
    primary_keys = ("planning_unit_id",)
    path = "/planning_units"
    records_jsonpath = "$.planning_units[*]"


# https://legacy-api.peopleware.com/#tag/Employees/operation/getV1Employees
class EmployeeStream(PeoplewareStream):
    """Define employee stream."""

    name = "employees"
    schema = EmployeeObject.to_dict()
    primary_keys = ("employee_id",)
    path = "/employees"
    records_jsonpath = "$.employees[*]"

    @override
    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        params["include_userid"] = "true"

        return params

    @override
    def post_process(self, row, context=None):
        if row["birth_date"] == "":
            row["birth_date"] = None

        return row

    @override
    def get_child_context(self, record, context):
        return {"employee_id": record["employee_id"]}


class _EmployeeReportStream(PeoplewareStream):
    parent_stream_type = EmployeeStream

    @override
    def get_records(self, context):
        try:
            yield from super().get_records(context)
        except ResumableAPIError as e:
            self.logger.warning(e)

    @override
    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        params["end_date"] = API_MAX_DATE

        return params

    @override
    def validate_response(self, response):
        if response.status_code == HTTPStatus.NOT_FOUND:
            msg = f"No data for employee {self.context['employee_id']}"
            raise ResumableAPIError(msg, response)

        super().validate_response(response)

    def _get_start_date(self):
        return self.get_starting_replication_key_value(self.context) or API_MIN_DATE


# https://legacy-api.peopleware.com/#tag/Employees/operation/getV1EmployeesEmployeeIdContractsStartDate
class EmployeeContractStream(_EmployeeReportStream):
    """Define employee contract stream."""

    parent_stream_type = EmployeeStream
    name = "employee_contracts"
    schema = EmployeeContractObject.to_dict()
    primary_keys = ("employee_id", "contract_id")
    replication_key = "start_date"
    records_jsonpath = "$.employee_contracts[*]"

    @property
    def path(self):
        return "/employees/{employee_id}/contracts/{start_date}".format(
            employee_id=self.context["employee_id"],
            start_date=self._get_start_date(),
        )


# https://legacy-api.peopleware.com/#tag/Employees/operation/getV1EmployeesEmployeeIdPlanningUnitsStartDate
class EmployeePlanningUnitStream(_EmployeeReportStream):
    """Define employee planning unit stream."""

    parent_stream_type = EmployeeStream
    name = "employee_planning_units"
    schema = EmployeePlanningUnitObject.to_dict()
    primary_keys = ("employee_id", "planning_unit_id")
    replication_key = "end_date"
    records_jsonpath = "$.employee_planning_units[*]"

    @property
    def path(self):
        return "/employees/{employee_id}/planning_units/{start_date}".format(
            employee_id=self.context["employee_id"],
            start_date=self._get_start_date(),
        )


# https://legacy-api.peopleware.com/#tag/Employees/operation/getV1EmployeesEmployeeIdScheduleStartDate
class EmployeeScheduleStream(_EmployeeReportStream):
    """Define employee schedule stream."""

    parent_stream_type = EmployeeStream
    name = "employee_schedules"
    schema = EmployeeScheduleObject.to_dict()
    primary_keys = ("booking_date", "employee_id")
    replication_key = "booking_date"
    records_jsonpath = "$.schedules[*]"

    @property
    def path(self):
        return "/employees/{employee_id}/schedule/{start_date}".format(
            employee_id=self.context["employee_id"],
            start_date=self._get_start_date(),
        )
