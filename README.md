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
manager = SandboxManager("http://localhost:8080")

# List all VMs
vms = manager.list_all()

# Start a new VM
new_vm = manager.start_sandbox("my-vm")

# Run a command in the VM
result = new_vm.run_cmd("echo hello world")
print(result["output"])

# Create a snapshot
snapshot_id = new_vm.take_snapshot("my-snapshot")

# Destroy the VM when done
new_vm.destroy()
```

For more examples, check out the [cookbook.py](examples/cookbook.py) file which demonstrates:

- Basic VM operations
- VM lifecycle management
- Working with snapshots
- Setting up port forwarding

## License

MIT
