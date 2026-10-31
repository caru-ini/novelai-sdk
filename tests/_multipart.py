from __future__ import annotations

import json
from email.parser import BytesParser
from email.policy import HTTP
from typing import Any

import httpx


def request_parts(request: httpx.Request) -> dict[str, bytes]:
    """Parts of a captured multipart request, keyed by form field name"""
    header = f"Content-Type: {request.headers['Content-Type']}\r\n\r\n".encode()
    message = BytesParser(policy=HTTP).parsebytes(header + request.content)
    return {
        str(part.get_param("name", header="content-disposition")): part.get_payload(
            decode=True
        )
        for part in message.iter_parts()
    }


def request_json(request: httpx.Request) -> dict[str, Any]:
    """JSON body sent in the `request` part"""
    return json.loads(request_parts(request)["request"])
