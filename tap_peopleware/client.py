"""REST client handling, including PeoplewareStream base class."""

from __future__ import annotations

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.streams import RESTStream
from typing_extensions import override


class PeoplewareStream(RESTStream):
    """Peopleware stream class."""

    url_base = "https://legacy-api.peopleware.com/v1"

    @override
    @property
    def authenticator(self):
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token", ""),
        )
