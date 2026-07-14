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
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
