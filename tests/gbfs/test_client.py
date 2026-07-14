import json
from typing import Never

import httpx
import pytest

from bike_station_risk.gbfs import GbfsClient


def test_client_removes_trailing_slash_from_base_url() -> None:
    client = GbfsClient("https://example.com/")

    assert client._base_url == "https://example.com"

    client.close()


def test_client_uses_default_timeout() -> None:
    client = GbfsClient("https://example.com/")

    assert client._timeout == 10.0

    client.close()


def test_client_uses_custom_timeout() -> None:
    client = GbfsClient(base_url="https://example.com/", timeout=30.0)

    assert client._timeout == 30.0

    client.close()


def test_client_rejects_empty_base_url() -> None:
    with pytest.raises(ValueError):
        GbfsClient(base_url="")


def test_client_rejects_blank_base_url() -> None:
    with pytest.raises(ValueError):
        GbfsClient(base_url=" ")


def test_client_rejects_non_positive_timeout() -> None:
    with pytest.raises(ValueError):
        GbfsClient(base_url="https://example.com/", timeout=-10)
    with pytest.raises(ValueError):
        GbfsClient(base_url="https://example.com/", timeout=0)


def test_client_builds_url_from_endpoint_without_leading_slash() -> None:
    client = GbfsClient(base_url="https://example.com/")

    assert (
        client._build_url("station_information.json")
        == "https://example.com/station_information.json"
    )

    client.close()


def test_client_builds_url_from_endpoint_with_leading_slash() -> None:
    client = GbfsClient(base_url="https://example.com/")

    assert (
        client._build_url("/station_information.json")
        == "https://example.com/station_information.json"
    )

    client.close()


def test_client_rejects_empty_endpoint() -> None:
    client = GbfsClient(base_url="https://example.com/")

    with pytest.raises(ValueError):
        client._build_url("")
    with pytest.raises(ValueError):
        client._build_url("  ")

    client.close()


def test_client_returns_json_response(monkeypatch) -> None:
    client = GbfsClient(
        base_url="https://example.com/",
        timeout=30.0,
    )

    expected_data = {"stations": {}}
    called = {}

    request = httpx.Request(
        "GET",
        "https://example.com/station_information.json",
    )

    response = httpx.Response(
        status_code=200,
        request=request,
        json=expected_data,
    )

    def fake_get(url: str) -> httpx.Response:
        called["url"] = url
        return response

    monkeypatch.setattr(client._http_client, "get", fake_get)

    data = client.get("station_information.json")

    assert called["url"] == "https://example.com/station_information.json"
    assert data == expected_data

    client.close()


@pytest.mark.parametrize("status_code", [400, 404, 500, 503])
def test_client_raises_error_for_unsuccessful_response(monkeypatch, status_code: int) -> None:
    client = GbfsClient(base_url="https://example.com/")

    request = httpx.Request(
        method="GET",
        url="https://example.com/station_information.json",
    )
    response = httpx.Response(
        status_code=status_code,
        request=request,
    )

    def fake_get(url: str) -> httpx.Response:
        return response

    monkeypatch.setattr(client._http_client, "get", fake_get)

    with pytest.raises(httpx.HTTPStatusError):
        client.get("station_information.json")

    client.close()


def test_client_raises_network_exception(monkeypatch) -> None:
    client = GbfsClient(base_url="https://example.com/")

    request = httpx.Request(
        method="GET",
        url="https://example.com/station_information.json",
    )

    def fake_get(url: str) -> Never:
        raise httpx.TimeoutException(message="TimeoutException for testing", request=request)

    monkeypatch.setattr(client._http_client, "get", fake_get)

    with pytest.raises(httpx.TimeoutException):
        client.get("station_information.json")

    client.close()


def test_client_raises_error_for_invalid_json(monkeypatch) -> None:
    client = GbfsClient(base_url="https://example.com/")

    request = httpx.Request(
        method="GET",
        url="https://example.com/station_information.json",
    )
    response = httpx.Response(
        status_code=200,
        request=request,
        content=b"This is not valid JSON",
    )

    def fake_get(url: str) -> httpx.Response:
        return response

    monkeypatch.setattr(client._http_client, "get", fake_get)

    with pytest.raises(json.JSONDecodeError):
        client.get("station_information.json")

    client.close()


def test_client_closes_http_client(monkeypatch) -> None:
    client = GbfsClient(
        base_url="https://example.com/",
        timeout=30.0,
    )

    called = {"close": False}

    def fake_close() -> None:
        called["close"] = True

    monkeypatch.setattr(client._http_client, "close", fake_close)

    client.close()

    assert called["close"] is True


def test_client_uses_provided_http_client() -> None:
    http_client = httpx.Client()

    client = GbfsClient(
        base_url="https://example.com/",
        http_client=http_client,
    )

    assert client._http_client is http_client

    http_client.close()


def test_client_uses_injected_http_client() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://example.com/station_information.json"

        return httpx.Response(
            status_code=200,
            json={"stations": []},
        )

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport)

    client = GbfsClient(
        base_url="https://example.com/",
        http_client=http_client,
    )

    data = client.get("station_information.json")

    assert data == {"stations": []}

    http_client.close()


def test_client_does_not_close_injected_http_client(monkeypatch) -> None:
    http_client = httpx.Client()
    real_close = http_client.close

    client = GbfsClient(
        base_url="https://example.com/",
        http_client=http_client,
    )

    called = {"close": False}

    def fake_close() -> None:
        called["close"] = True

    monkeypatch.setattr(http_client, "close", fake_close)

    client.close()

    assert called["close"] is False

    real_close()
