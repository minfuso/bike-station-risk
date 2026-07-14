"""GBFS feed discovery client."""


class GbfsClient:
    """Synchronous client for discovering GBFS feeds."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
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

    def _build_url(self, endpoint: str) -> str:
        if not endpoint.strip():
            raise ValueError("Endpoint must not be empty.")

        endpoint = endpoint.strip()

        return f"{self._base_url}/{endpoint.lstrip('/')}"
