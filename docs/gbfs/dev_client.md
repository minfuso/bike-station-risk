# GBFS Client Development Roadmap

## 1. Initialize the client

Implement the constructor.

**Goals**
- Store the base URL.
- Remove any trailing slash from the base URL.
- Store the HTTP timeout.

**Tests**
- Stores the base URL correctly.
- Removes the trailing slash.
- Uses the default timeout.
- Accepts a custom timeout.

---

## 2. Validate constructor arguments

Validate the inputs provided to the constructor.

**Goals**
- Reject an empty base URL.
- Reject a non-positive timeout.
- Optionally validate the URL scheme (`http://` or `https://`).

**Tests**
- Empty base URL raises an error.
- Zero timeout raises an error.
- Negative timeout raises an error.

---

## 3. Build endpoint URLs

Create a helper method to build complete URLs from endpoints.

**Goals**
- Join the base URL and endpoint safely.
- Avoid duplicate slashes.

**Tests**
- Works with and without a leading slash.
- Produces the expected URL.

---

## 4. Add an HTTP client

Choose the HTTP library (`requests` or `httpx`) and implement the first request.

**Goals**
- Perform a GET request.
- Apply the configured timeout.

---

## 5. Implement a generic GET method

Create a method that retrieves JSON from any GBFS endpoint.

**Goals**
- Build the request URL.
- Send the request.
- Return the parsed JSON response.

**Tests**
- Returns the expected JSON payload.

---

## 6. Handle HTTP errors

Handle unsuccessful HTTP responses.

**Goals**
- Raise an exception for 4xx and 5xx responses.

**Tests**
- Successful responses are accepted.
- 404 responses raise an error.
- 500 responses raise an error.

---

## 7. Handle network errors

Handle failures that occur before receiving an HTTP response.

**Goals**
- Handle timeouts.
- Handle connection errors.
- Expose meaningful exceptions.

**Tests**
- Timeout is handled correctly.
- Connection errors are handled correctly.

---

## 8. Validate JSON responses

Ensure the response contains valid JSON.

**Goals**
- Reject invalid JSON payloads.
- Raise a meaningful exception.

**Tests**
- Valid JSON is accepted.
- Invalid JSON raises an error.

---

## 9. Improve type hints

Use precise return types.

**Goals**
- Return `dict[str, Any]`.
- Keep the public API well typed.

---

## 10. Use an HTTP session

Reuse HTTP connections instead of creating a new one for every request.

**Goals**
- Create a reusable session.
- Improve performance.
- Simplify future configuration.

---

## 11. Support dependency injection

Allow a custom HTTP session to be provided.

**Goals**
- Improve testability.
- Decouple the client from the HTTP implementation.

---

## 12. Add GBFS-specific methods

Expose methods dedicated to GBFS endpoints.

**Examples**
- `get_station_information()`
- `get_station_status()`
- `get_system_information()`

---

## 13. Validate the GBFS structure

Verify that the returned JSON follows the GBFS specification.

**Goals**
- Check required top-level fields.
- Validate the `data` section.

---

## 14. Introduce typed models

Convert raw dictionaries into typed Python objects.

**Goals**
- Improve readability.
- Improve type safety.
- Reduce parsing logic elsewhere in the project.

---

## 15. Complete the unit test suite

Cover every important behavior.

**Tests**
- Constructor
- Argument validation
- URL building
- Successful requests
- HTTP errors
- Network errors
- Invalid JSON
- GBFS-specific methods

---

## 16. Add integration tests

Test the client against a real GBFS feed.

**Goals**
- Verify end-to-end behavior.
- Keep these tests separate from unit tests.

---

## 17. Expose the public API

Export `GbfsClient` from the package.

**Goal**
- Allow users to write:

```python
from bike_station_risk.gbfs import GbfsClient
```

---

## 18. Final quality checks

Before each commit:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run pytest
```