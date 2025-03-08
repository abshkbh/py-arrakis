"""
py-arrakis - A Python SDK for Arrakis.

This package provides a Python interface to the Arrakis VM sandbox system.
"""

__version__ = "0.0.1"

# Import main classes to make them available at the package level
from .sandbox import Sandbox
from .sandbox_manager import SandboxManager

# Define public API
__all__ = ["Sandbox", "SandboxManager"]
