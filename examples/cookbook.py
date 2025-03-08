#!/usr/bin/env python3
"""
Py-Arrakis Cookbook

This cookbook demonstrates common use cases and examples for the py-arrakis SDK.
It provides practical examples of how to use the library to interact with Arrakis
sandbox VMs through the REST API.
"""

import time
import requests
from py_arrakis import SandboxManager

# Set the base URL for the Arrakis REST server
BASE_URL = "http://localhost:7000"

# TODO: Remove this after the boot up synchronization is implemented.
VM_START_WAIT_TIME_SECONDS = 3


def basic_usage_example():
    """Basic usage example showing core functionality."""
    print("=== Basic Usage Example ===")

    # Initialize the sandbox manager
    sandbox_manager = SandboxManager(BASE_URL)

    # List all existing VMs
    print("Listing all VMs:")
    sandboxes = sandbox_manager.list_all()
    for sandbox in sandboxes:
        print(f"  - {sandbox.name}")

    # Start a new VM if none exist
    if not sandboxes:
        print("Starting a new VM...")
        new_sandbox = sandbox_manager.start_sandbox("example-vm")
        print(f"Started VM: {new_sandbox.name}")

        # Wait a moment for the VM to initialize
        print("Waiting for VM to initialize...")
        time.sleep(VM_START_WAIT_TIME_SECONDS)
    else:
        # Use the first VM if any exist
        new_sandbox = sandboxes[0]


def vm_management_example():
    """Examples of VM lifecycle management."""
    print("=== VM Management Example ===")

    sandbox_manager = SandboxManager(BASE_URL)

    # Start a VM with a specific name
    print("Starting a new VM...")
    sandbox = sandbox_manager.start_sandbox("lifecycle-example")
    print(f"Started VM: {sandbox.name}")

    # Give the VM time to start up
    print("Waiting for VM to initialize...")
    time.sleep(VM_START_WAIT_TIME_SECONDS)

    # Get VM details
    print("Getting VM details:")
    details = sandbox.list()
    print(f"  Status: {details.get('status')}")
    print(f"  IP: {details.get('ip')}")
    print(f"  Tap Device: {details.get('tap_device_name')}")

    # List port forwards if available
    if "port_forwards" in details:
        print("  Port Forwards:")
        for pf in details["port_forwards"]:
            print(
                f"    Host:{pf['host_port']} → Guest:{pf['guest_port']} ({pf['description']})"
            )

    # Clean up - remove the VM
    print("Destroying the VM...")
    sandbox.destroy()
    print("VM destroyed")


def snapshot_example():
    """Example of working with VM snapshots."""
    print("=== Snapshot Example ===")

    sandbox_manager = SandboxManager(BASE_URL)
    sandbox_name = "snapshot-example"

    # Start a test VM
    print("Starting a test VM for snapshots...")
    sandbox = sandbox_manager.start_sandbox(sandbox_name)

    # Wait for the VM to initialize
    print("Waiting for VM to initialize...")
    time.sleep(VM_START_WAIT_TIME_SECONDS)

    # Run a command to modify the VM state before snapshot
    print("Modifying VM state before snapshot...")
    result = sandbox.run_cmd("echo 'test data before snapshot' > /tmp/testfile")
    print(f"Command output: {result.get('output', '')}")

    # Create a snapshot
    print("Creating a snapshot...")
    snapshot_id = sandbox.snapshot("initial-state")
    print(f"Created snapshot with ID: {snapshot_id}")

    # Run a command to modify the VM state after snapshot
    print("Modifying VM state after snapshot...")
    result = sandbox.run_cmd("echo 'test data after snapshot' > /tmp/testfile")
    print(f"Command output: {result.get('output', '')}")

    # Verify the file exists
    print("Verifying file was created...")
    result = sandbox.run_cmd("cat /tmp/testfile")
    print(f"File content: {result.get('output', '')}")

    # Destroy the sandbox
    print("Destroying the sandbox...")
    sandbox.destroy()

    # Restore from snapshot
    print("Restoring from snapshot...")
    sandbox = sandbox_manager.restore(sandbox_name, snapshot_id)
    print("Snapshot restored")

    # Verify the file no longer exists
    print("Verifying file state after restore...")
    result = sandbox.run_cmd("cat /tmp/testfile")
    if result["output"] == "test data before snapshot\n":
        print("File content is correct after restore (as expected)")
    else:
        print(f"Unexpected result: {result}")

    # Clean up
    print("Cleaning up...")
    sandbox.destroy()
    print("VM destroyed")


def context_manager_example():
    """Example of using a sandbox with context manager for automatic cleanup."""
    print("=== Context Manager Example ===")

    sandbox_manager = SandboxManager(BASE_URL)

    print("Starting a VM using context manager (will auto-destroy when done)...")
    # The 'with' statement automatically calls __enter__ and __exit__ methods
    # The __exit__ method on Sandbox will automatically destroy the VM
    with sandbox_manager.start_sandbox("auto-cleanup-example") as sandbox:
        print(f"Started VM: {sandbox.name}")

        # Wait for the VM to initialize
        print("Waiting for VM to initialize...")
        time.sleep(VM_START_WAIT_TIME_SECONDS)

        # Run some commands in the VM
        print("Running commands in the VM...")
        result = sandbox.run_cmd("echo 'Hello from sandbox context manager'")
        print(f"Command output: {result.get('output', '')}")

        # The sandbox will be automatically destroyed when exiting the 'with' block
        print("Exiting context - VM will be destroyed automatically")

    # At this point, the VM has been destroyed automatically
    print("VM has been destroyed automatically")


def wrap_with_error_handling(func):
    """Wrapper that executes a function with standardized error handling.

    Args:
        func: The function to execute with error handling

    Returns:
        Any value returned by the wrapped function, if successful

    Note:
        This wrapper catches and handles exceptions in a standardized way,
        which is particularly useful for examples and scripts.
    """
    # ANSI color codes
    RED = "\033[91m"
    RESET = "\033[0m"

    try:
        return func()
    except requests.HTTPError as e:
        response = e.response
        error_data = response.json()
        print(f"{RED}API Error: {error_data['error']['message']}{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        print(
            f"{RED}Make sure the Arrakis server is running and accessible at {BASE_URL}{RESET}"
        )


if __name__ == "__main__":
    print("Py-Arrakis SDK Cookbook")
    print("======================")
    print(
        "This script demonstrates how to use the py-arrakis SDK to interact with Arrakis VMs."
    )
    print("Make sure the Arrakis server is running at", BASE_URL)

    # Call each example individually with error handling
    print("Running Basic Usage Example...")
    wrap_with_error_handling(basic_usage_example)

    print("Running VM Management Example...")
    wrap_with_error_handling(vm_management_example)

    print("Running Snapshot Example...")
    wrap_with_error_handling(snapshot_example)

    print("Running Context Manager Example...")
    wrap_with_error_handling(context_manager_example)

    print("All examples completed.")
