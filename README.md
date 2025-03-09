# py-arrakis

Python SDK for [Arrakis](https://github.com/abshkbh/arrakis).

## Description

This package provides a Python SDK over the REST API exposed by [Arrakis](https://github.com/abshkbh/arrakis).

## Installation

```
pip install py-arrakis
```

## Usage

The SDK provides a simple interface to manage Arrakis sandbox VMs:

```python
from py_arrakis import SandboxManager

# Initialize the sandbox manager with the Arrakis server URL
manager = SandboxManager("http://localhost:7000")

# List all VMs
sandboxes = manager.list_all()

# Start a new VM
sandbox = manager.start_sandbox("my-sandbox")

# Run a command in the VM
result = sandbox.run_cmd("echo hello world")
print(result["output"])

# Create a snapshot
snapshot_id = sandbox.snapshot("snapshot-v1")

# Destroy the VM when done
sandbox.destroy()

# Restore from snapshot
restored_sandbox = manager.restore("my-vm", snapshot_id)
```

For more examples, check out the [cookbook.py](examples/cookbook.py) file.

## License

MIT
