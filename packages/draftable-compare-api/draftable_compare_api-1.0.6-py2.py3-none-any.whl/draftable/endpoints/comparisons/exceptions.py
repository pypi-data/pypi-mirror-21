from __future__ import absolute_import

import requests
# noinspection PyUnresolvedReferences
from ..exceptions import EndpointException, InvalidArgument, BadRequest


class NotFound(BadRequest):
    pass


def raise_for(ex):
    # type: (requests.exceptions.HTTPError) -> None
    try:
        if ex.response.status_code == 404:
            wrapper = NotFound(404, ex.response.json())
        else:
            wrapper = BadRequest(ex.response.status_code, ex.response.json())
    except:
        # No JSON body? This shouldn't happen, but we'll rethrow anyway.
        wrapper = BadRequest(ex.response.status_code, ex.response)

    wrapper.__cause__ = ex
    raise wrapper
