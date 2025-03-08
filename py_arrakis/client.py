"""
REST API client module for interacting with Arrakis server.
"""

from __future__ import annotations

import requests


class APIClient:
    """Simple REST API client using requests."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, endpoint: str, params: dict[str, any] = None) -> dict[str, any]:
        """Make a GET request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict[str, any] = None) -> dict[str, any]:
        """Make a POST request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def patch(self, endpoint: str, data: dict[str, any] = None) -> dict[str, any]:
        """Make a PATCH request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> dict[str, any]:
        """Make a DELETE request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
