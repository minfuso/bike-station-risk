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
