"""Compatibility alias for the registered Dev lifecycle source path."""
import sys

from otto import lifecycle as _lifecycle

# Keep only the registered source path and the shared module patch target.
sys.modules[__name__] = _lifecycle
