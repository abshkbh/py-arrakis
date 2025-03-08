"""
Sandbox module for managing VM instances.
"""

import datetime

from .client import APIClient


class Sandbox:
    """Represents a single sandbox VM instance."""

    def __init__(self, api_client: APIClient, name: str):
        self._api = api_client
        self.name = name

    def list(self) -> dict:
        """Get details of this sandbox VM.

        Returns:
            dict: Details of the VM including status, IP, tap device name, and port forwards.

        Raises:
            Exception: If the API request fails.
        """
        response = self._api.get(f"/vms/{self.name}")

        port_forwards = []
        for pf in response.get("portForwards", []):
            port_forwards.append(
                {
                    "host_port": pf.get("hostPort"),
                    "guest_port": pf.get("guestPort"),
                    "description": pf.get("description"),
                }
            )

        result = {
            "name": response.get("vmName"),
            "status": response.get("status"),
            "ip": response.get("ip"),
            "tap_device_name": response.get("tapDeviceName"),
        }

        if port_forwards:
            result["port_forwards"] = port_forwards
        return result

    def update_state(self, status: str) -> None:
        """Update the state of this sandbox VM.

        Args:
            status: New state for the VM. Must be either 'stopped' or 'paused'.

        Raises:
            ValueError: If status is not 'stopped' or 'paused'.
            Exception: If the API request fails.
        """
        if status not in ["stopped", "paused"]:
            raise ValueError("Status must be either 'stopped' or 'paused'")

        self._api.patch(f"/vms/{self.name}", {"status": status})

    def destroy(self) -> None:
        """Destroy this sandbox VM.

        This permanently destroys the VM and frees all associated resources.

        Raises:
            Exception: If the API request fails.
        """
        self._api.delete(f"/vms/{self.name}")

    def snapshot(self, snapshot_id: str = "") -> str:
        """Create a snapshot of this sandbox VM.

        Args:
            snapshot_id: Unique identifier for the snapshot. If not provided,
                        a default ID will be generated based on the VM name and timestamp.

        Returns:
            str: The ID of the created snapshot.

        Raises:
            Exception: If the API request fails.
        """
        # Generate default snapshot ID if not provided
        if not snapshot_id:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            snapshot_id = f"snapshot-{self.name}-{timestamp}"

        response = self._api.post(
            f"/vms/{self.name}/snapshots", {"snapshotId": snapshot_id}
        )
        return response.get("snapshotId", snapshot_id)

    def run_cmd(self, cmd: str) -> dict[str, str]:
        """Execute a command in the VM.

        Args:
            cmd: Command to execute in the VM.

        Returns:
            dict: Dictionary containing 'output' and/or 'error' keys with command results.

        Raises:
            Exception: If the API request fails.
        """
        response = self._api.post(f"/vms/{self.name}/cmd", {"cmd": cmd})
        return {
            "output": response.get("output", ""),
            "error": response.get("error", ""),
        }

    def upload_files(self, files: List[Dict[str, str]]) -> None:
        """Upload files to the VM.

        Args:
            files: List of dictionaries, each containing 'path' and 'content' keys.
                  'path' is the destination path in the VM
                  'content' is the file content as a string

        Raises:
            Exception: If the API request fails.
        """
        self._api.post(f"/vms/{self.name}/files", {"files": files})

    def download_files(self, paths: List[str]) -> List[Dict[str, str]]:
        """Download files from the VM.

        Args:
            paths: List of file paths to download from the VM.

        Returns:
            List of dictionaries containing file information:
            - 'path': Path of the file
            - 'content': Content of the file if successful
            - 'error': Error message if download failed

        Raises:
            Exception: If the API request fails.
        """
        # API expects comma-separated paths
        paths_str = ",".join(paths)
        response = self._api.get(f"/vms/{self.name}/files?paths={paths_str}")
        return response.get("files", [])

    def __enter__(self) -> "Sandbox":
        """Enter the context manager.

        Returns:
            Sandbox: This sandbox instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager and destroy the sandbox.

        The sandbox will be destroyed even if an exception occurred within the context.
        """
        self.destroy()
