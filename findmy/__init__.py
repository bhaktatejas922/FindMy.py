import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

"""A package providing everything you need to work with Apple's FindMy network."""

from . import errors, keys, reports, scanner
from .accessory import FindMyAccessory
from .keys import KeyPair

__all__ = (
    "keys",
    "reports",
    "scanner",
    "errors",
    "FindMyAccessory",
    "KeyPair",
)
