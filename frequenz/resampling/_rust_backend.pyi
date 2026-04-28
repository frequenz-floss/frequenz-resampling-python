# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Type stubs for the Rust-backed Python extension module."""

# Stub files mirror the exported Python API and signature-only declarations.
# pylint: disable=too-many-arguments,unused-argument

__all__ = "Closed", "Label", "Resampler", "ResamplingFunction", "resample"

from datetime import datetime, timedelta
from enum import Enum, unique
from typing import Optional, Sequence

@unique
class ResamplingFunction(Enum):
    """
    The ResamplingFunction enum represents the different resampling functions
    that can be used to resample a time series.
    """

    AVERAGE = 0
    """Calculates the average of all samples in the time step (ignoring None values)"""
    SUM = 1
    """Calculates the sum of all samples in the time step (ignoring None values)"""
    MAX = 2
    """Calculates the maximum of all samples in the time step"""
    MIN = 3
    """Calculates the minimum of all samples in the time step"""
    LAST = 4
    """Returns the last sample in the time step"""
    COUNT = 5
    """Counts the number of samples in the time step"""
    FIRST = 6
    """Returns the first sample in the time step"""
    COALESCE = 7
    """Returns the first non-None sample in the time step"""

    @staticmethod
    def values() -> list[int]:
        """
        Returns a list of all values of the enum.

        Returns:
            A list of all values of the enum.
        """

    @staticmethod
    def members() -> list[tuple[str, int]]:
        """
        Returns a list of all members of the enum.

        Returns:
            A list of all members of the enum.
        """

@unique
class Closed(Enum):
    """Controls which edge of an interval is closed for sample membership."""

    LEFT = 0
    """Left-closed, right-open intervals: `[start, end)`"""
    RIGHT = 1
    """Left-open, right-closed intervals: `(start, end]`"""

    @staticmethod
    def values() -> list[int]:
        """Returns a list of all values of the enum."""

    @staticmethod
    def members() -> list[tuple[str, int]]:
        """Returns a list of all members of the enum."""

@unique
class Label(Enum):
    """Controls which edge of an interval is used as the output timestamp."""

    LEFT = 0
    """Use the interval start as the output timestamp"""
    RIGHT = 1
    """Use the interval end as the output timestamp"""

    @staticmethod
    def values() -> list[int]:
        """Returns a list of all values of the enum."""

    @staticmethod
    def members() -> list[tuple[str, int]]:
        """Returns a list of all members of the enum."""

class Resampler:
    """
    The Resampler class is used to resample a time series of samples.

    It stores the samples in a buffer and resamples the samples in the buffer when the
    resample method is called.
    A resampler can be configured with a resampling function and a resampling interval.
    """

    def __init__(
        self,
        interval: timedelta,
        resampling_function: ResamplingFunction,
        *,
        max_age_in_intervals: int,
        start: datetime,
        closed: Closed,
        label: Label,
    ):
        """
        Initializes a new Resampler object.

        Args:
            interval: The resampling interval.
            resampling_function: The resampling function.
            max_age_in_intervals: The maximum age of a sample in intervals.
            start: The start time of the resampling.
            closed: Which interval edge is closed for sample membership. Use
                `"left"` for left-closed, right-open intervals `[start, end)`
                and `"right"` for right-closed, left-open intervals
                `(start, end]`.
            label: Which interval edge to use for output timestamps. Use
                `"left"` for the left bin edge and `"right"` for the right
                bin edge.
        """

    def push_sample(self, *, timestamp: datetime, value: Optional[float]) -> None:
        """
        Pushes a new sample into the resampler buffer.

        Args:
            timestamp: The timestamp of the sample.
            value: The value of the sample.
        """

    def resample(
        self, end: datetime | None = None
    ) -> list[tuple[datetime, Optional[float]]]:
        """
        Resamples the samples in the buffer until the given end time.

        Args:
            end: The end time of the resampling. If `None` the samples in the buffer will be
                resampled until the current date/time.

        Returns:
            A list of tuples with the resampled samples.
        """

def resample(
    data: Sequence[tuple[datetime, Optional[float]]],
    interval: timedelta,
    method: ResamplingFunction,
    *,
    closed: Closed,
    label: Label,
) -> list[tuple[datetime, Optional[float]]]:
    """
    Resamples a list of timestamp/value pairs in a single call.

    This is a convenience function for one-shot resampling without needing to
    manage a `Resampler` instance.

    Args:
        data: A list of (timestamp, value) tuples to resample. Must be sorted by timestamp.
        interval: The resampling interval.
        method: The resampling function to use for aggregating values within each interval.
        closed: Which interval edge is closed for sample membership. Use
            `"left"` for left-closed, right-open intervals `[start, end)`
            and `"right"` for right-closed, left-open intervals `(start, end]`.
        label: Which interval edge to use for output timestamps. Use `"left"`
            for the left bin edge and `"right"` for the right bin edge.

    Returns:
        A list of (timestamp, value) tuples representing the resampled data.
    """
