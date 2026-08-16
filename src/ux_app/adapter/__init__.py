"""Adapter boundary.

This package is the only place that may import ux_channel or cek_*.
Submodules lazy-import those cores so a cold `import ux_app` stays clean.
The in-process runtime in runtime.py does not import the cores.
"""
