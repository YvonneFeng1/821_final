"""Some utility functions."""

from tkinter import ttk


def clear_entries(entries: list[ttk.Entry]):
    """Clear all the selected entries."""
    for entry in entries:
        entry.delete(0, "end")
    return
