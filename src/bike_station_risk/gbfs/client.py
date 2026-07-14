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
        """

        if not base_url.strip():
            raise ValueError("Base URL must not be empty.")

        if timeout <= 0:
            raise ValueError("Timeout must be a positive number.")

        self._base_url = base_url.rstrip("/")
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

    def close(self) -> None:
        if self._owns_http_client:
            self._http_client.close()
