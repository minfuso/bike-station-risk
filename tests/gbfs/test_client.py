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

    class FakeResponse:
        def json(self) -> dict:
            return expected_data

    def fake_get(url: str, timeout: float) -> FakeResponse:
        called["url"] = url
        called["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(httpx, "get", fake_get)

    data = client.get("station_information.json")

    assert called["url"] == "https://example.com/station_information.json"
    assert called["timeout"] == 30.0
    assert data == expected_data
