from typing import Never

import httpx
import pytest

from bike_station_risk.gbfs import GbfsClient


def test_client_removes_trailing_slash_from_base_url() -> None:
    client = GbfsClient("https://example.com/")

    assert client._base_url == "https://example.com"


def test_client_uses_default_timeout() -> None:
    client = GbfsClient("https://example.com/")

    assert client._timeout == 10.0


def test_client_uses_custom_timeout() -> None:
    client = GbfsClient(base_url="https://example.com/", timeout=30.0)

    assert client._timeout == 30.0


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


def test_client_builds_url_from_endpoint_with_leading_slash() -> None:
    client = GbfsClient(base_url="https://example.com/")

    assert (
        client._build_url("/station_information.json")
        == "https://example.com/station_information.json"
    )


def test_client_rejects_empty_endpoint() -> None:
    client = GbfsClient(base_url="https://example.com/")

    with pytest.raises(ValueError):
        client._build_url("")
    with pytest.raises(ValueError):
        client._build_url("  ")


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

    def fake_get(url: str, timeout: float) -> httpx.Response:
        called["url"] = url
        called["timeout"] = timeout
        return response

    monkeypatch.setattr(httpx, "get", fake_get)

    data = client.get("station_information.json")

    assert called["url"] == "https://example.com/station_information.json"
    assert called["timeout"] == 30.0
    assert data == expected_data


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

    def fake_get(url: str, timeout: float) -> httpx.Response:
        return response

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(httpx.HTTPStatusError):
        client.get("station_information.json")


def test_client_raises_network_exception(monkeypatch) -> None:
    client = GbfsClient(base_url="https://example.com/")

    request = httpx.Request(
        method="GET",
        url="https://example.com/station_information.json",
    )

    def fake_get(url: str, timeout: float) -> Never:
        raise httpx.TimeoutException(message="TimeoutException for testing", request=request)

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(httpx.TimeoutException):
        client.get("station_information.json")
