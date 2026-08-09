"""GBFS feed discovery client."""

from typing import Any

import httpx


class GbfsClient:
    """Synchronous client for discovering GBFS feeds."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        """Initialize the GBFS client.

        Args:
            base_url: Base URL of the GBFS system.
            timeout: Maximum request duration in seconds.
            http_client: Optional HTTP client to reuse.
        """

        if not base_url.strip():
            raise ValueError("Base URL must not be empty.")

        if timeout <= 0:
            raise ValueError("Timeout must be a positive number.")

        self._base_url = base_url.strip().rstrip("/")
        self._timeout = timeout
        self._owns_http_client = http_client is None

        if http_client is None:
            self._http_client = httpx.Client(timeout=timeout)
        else:
            self._http_client = http_client

    def _build_url(self, endpoint: str) -> str:
        if not endpoint.strip():
            raise ValueError("Endpoint must not be empty.")

        endpoint = endpoint.strip()

        return f"{self._base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str) -> dict[str, Any]:
        url = self._build_url(endpoint)

        response = self._http_client.get(url)
        response.raise_for_status()

        return response.json()

    def get_station_information(self) -> list[dict[str, Any]]:
        selected_keys = {
            "name",
            "capacity",
            "station_id",
            "lat",
            "lon",
        }

        data = self.get("station_information.json")
        stations = data["data"]["stations"]

        for i, station in enumerate(stations):
            filtered_station = {}

            for key, value in station.items():
                if key in selected_keys:
                    filtered_station[key] = value

            stations[i] = filtered_station

        return stations

    def get_station_status(self) -> list[dict[str, Any]]:
        selected_keys = {
            "station_id",
            "num_bikes_available",
            "num_docks_available",
            "is_installed",
            "is_renting",
            "is_returning",
            "last_reported",
        }

        data = self.get("station_status.json")
        status = data["data"]["stations"]

        for i, station_status in enumerate(status):
            filtered_status = {}

            for key, value in station_status.items():
                if key in selected_keys:
                    filtered_status[key] = value

            status[i] = filtered_status

        return status

    def close(self) -> None:
        if self._owns_http_client:
            self._http_client.close()
