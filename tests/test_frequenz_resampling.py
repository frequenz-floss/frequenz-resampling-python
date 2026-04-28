# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests to verify that the resampler can be used successfully from Python."""

import datetime as dt
from typing import Literal

import pandas as pd
import pytest

from frequenz.resampling import Closed, Label, Resampler, ResamplingFunction, resample


def test_resampler_resampling_function_average() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → avg = 3.0
    # Interval [5, 10): t=5,6,7,8,9 with values 6,7,8,9,10 → avg = 8.0
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 3.0),
        (start + 10 * step, 8.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampler_resampling_function_sum() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.SUM,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → sum = 15.0
    # Interval [5, 10): t=5,6,7,8,9 with values 6,7,8,9,10 → sum = 40.0
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 15.0),
        (start + 10 * step, 40.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampler_resampling_function_max() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.MAX,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → max = 5.0
    # Interval [5, 10): t=5,6,7,8,9 with values 6,7,8,9,10 → max = 10.0
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 5.0),
        (start + 10 * step, 10.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampler_resampling_function_min() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.MIN,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → min = 1.0
    # Interval [5, 10): t=5,6,7,8,9 with values 6,7,8,9,10 → min = 6.0
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 1.0),
        (start + 10 * step, 6.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampler_resampling_function_first() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.FIRST,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → first = 1.0
    # Interval [5, 10): t=5,6,7,8,9 with values 6,7,8,9,10 → first = 6.0
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 1.0),
        (start + 10 * step, 6.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampler_resampling_function_last() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.LAST,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → last = 5.0
    # Interval [5, 10): t=5,6,7,8,9 with values 6,7,8,9,10 → last = 10.0
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 5.0),
        (start + 10 * step, 10.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampler_resampling_function_coalesce() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.COALESCE,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10, but t=5 is None
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → coalesce = 1.0
    # Interval [5, 10): t=5,6,7,8,9 with values None,7,8,9,10 → coalesce = 7.0
    for i in range(10):
        if i == 5:
            resampler.push_sample(timestamp=start + i * step, value=None)
        else:
            resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 1.0),
        (start + 10 * step, 7.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampler_resampling_function_count() -> None:
    """Test the resampler."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.COUNT,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 → count = 5.0
    # Interval [5, 10): t=5,6,7,8,9 → count = 5.0
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 5 * step, 5.0),
        (start + 10 * step, 5.0),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_resampling_none() -> None:
    """Test resampling with None values."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # All values are None
    for i in range(10):
        resampler.push_sample(timestamp=start + i * step, value=None)

    expected = [
        (start + 5 * step, None),
        (start + 10 * step, None),
    ]

    resampled = resampler.resample(start + 10 * step)

    assert resampled == expected


def test_enum_values() -> None:
    """Test the ResamplingFunction enum."""
    assert ResamplingFunction.values() == [0, 1, 2, 3, 4, 5, 6, 7]


def test_enum_members() -> None:
    """Test the ResamplingFunction enum."""
    assert ResamplingFunction.members() == [
        ("AVERAGE", 0),
        ("SUM", 1),
        ("MAX", 2),
        ("MIN", 3),
        ("LAST", 4),
        ("COUNT", 5),
        ("FIRST", 6),
        ("COALESCE", 7),
    ]


def test_enum_str_repr() -> None:
    """Test the ResamplingFunction enum."""
    assert str(ResamplingFunction.AVERAGE) == "ResamplingFunction.AVERAGE"
    assert repr(ResamplingFunction.AVERAGE) == "<ResamplingFunction.AVERAGE: 0>"
    assert str(ResamplingFunction.SUM) == "ResamplingFunction.SUM"
    assert repr(ResamplingFunction.SUM) == "<ResamplingFunction.SUM: 1>"
    assert str(ResamplingFunction.MAX) == "ResamplingFunction.MAX"
    assert repr(ResamplingFunction.MAX) == "<ResamplingFunction.MAX: 2>"
    assert str(ResamplingFunction.MIN) == "ResamplingFunction.MIN"
    assert repr(ResamplingFunction.MIN) == "<ResamplingFunction.MIN: 3>"
    assert str(ResamplingFunction.LAST) == "ResamplingFunction.LAST"
    assert repr(ResamplingFunction.LAST) == "<ResamplingFunction.LAST: 4>"
    assert str(ResamplingFunction.COUNT) == "ResamplingFunction.COUNT"
    assert repr(ResamplingFunction.COUNT) == "<ResamplingFunction.COUNT: 5>"
    assert str(ResamplingFunction.FIRST) == "ResamplingFunction.FIRST"
    assert repr(ResamplingFunction.FIRST) == "<ResamplingFunction.FIRST: 6>"
    assert str(ResamplingFunction.COALESCE) == "ResamplingFunction.COALESCE"
    assert repr(ResamplingFunction.COALESCE) == "<ResamplingFunction.COALESCE: 7>"


def test_resampling_function_name_value() -> None:
    """Test the ResamplingFunction name and value interface."""
    assert ResamplingFunction.AVERAGE.name == "AVERAGE"
    assert ResamplingFunction.AVERAGE.value == 0
    assert ResamplingFunction.SUM.name == "SUM"
    assert ResamplingFunction.SUM.value == 1
    assert ResamplingFunction.MAX.name == "MAX"
    assert ResamplingFunction.MAX.value == 2
    assert ResamplingFunction.MIN.name == "MIN"
    assert ResamplingFunction.MIN.value == 3
    assert ResamplingFunction.LAST.name == "LAST"
    assert ResamplingFunction.LAST.value == 4
    assert ResamplingFunction.COUNT.name == "COUNT"
    assert ResamplingFunction.COUNT.value == 5
    assert ResamplingFunction.FIRST.name == "FIRST"
    assert ResamplingFunction.FIRST.value == 6
    assert ResamplingFunction.COALESCE.name == "COALESCE"
    assert ResamplingFunction.COALESCE.value == 7


def test_resampling_function_init() -> None:
    """Test the ResamplingFunction init."""
    assert ResamplingFunction(0) == ResamplingFunction.AVERAGE
    assert ResamplingFunction(1) == ResamplingFunction.SUM
    assert ResamplingFunction(2) == ResamplingFunction.MAX
    assert ResamplingFunction(3) == ResamplingFunction.MIN
    assert ResamplingFunction(4) == ResamplingFunction.LAST
    assert ResamplingFunction(5) == ResamplingFunction.COUNT
    assert ResamplingFunction(6) == ResamplingFunction.FIRST
    assert ResamplingFunction(7) == ResamplingFunction.COALESCE


def test_resampler_label_left() -> None:
    """Test the resampler with the left interval label."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=0.5)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    for i in range(0, 20):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 0 * step, 5.5),
        (start + 10 * step, 15.5),
    ]

    resampled = resampler.resample(start + 20 * step)

    assert resampled == expected


def test_resampler_last_timestamp() -> None:
    """Test the resampler with the right interval label."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=0.5)
    resampler = Resampler(
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        max_age_in_intervals=1,
        start=start,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    # Data starts at t=0, step=0.5s, 20 samples
    # Interval [0, 5): t=0,0.5,1,1.5,2,2.5,3,3.5,4,4.5 → values 1-10 → avg = 5.5
    # Interval [5, 10): t=5,5.5,6,6.5,7,7.5,8,8.5,9,9.5 → values 11-20 → avg = 15.5
    for i in range(20):
        resampler.push_sample(timestamp=start + i * step, value=i + 1)

    expected = [
        (start + 10 * step, 5.5),
        (start + 20 * step, 15.5),
    ]

    resampled = resampler.resample(start + 20 * step)

    assert resampled == expected


# Tests for the one-shot resample function


def test_resample_function_basic() -> None:
    """Test the resample function with basic usage."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)

    # Data: t=0,1,2,3,4,5,6,7,8,9 with values 1-10
    # Interval [0, 5): t=0,1,2,3,4 with values 1,2,3,4,5 → avg = 3.0
    # Interval [5, 10): t=5,6,7,8,9 with values 6,7,8,9,10 → avg = 8.0
    data = [(start + i * step, float(i + 1)) for i in range(10)]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    assert len(result) == 2
    assert result[0] == (start, 3.0)
    assert result[1] == (start + 5 * step, 8.0)


def test_resample_function_label_right() -> None:
    """Test the resample function with label='right'."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)

    data = [(start + i * step, float(i + 1)) for i in range(10)]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        closed=Closed.LEFT,
        label=Label.RIGHT,
    )

    assert len(result) == 2
    # With label='right', timestamps are at end of interval
    assert result[0] == (start + 5 * step, 3.0)
    assert result[1] == (start + 10 * step, 8.0)


def test_resample_function_closed_right() -> None:
    """Test the resample function with right-closed intervals."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    data = [
        (start, 10.0),
        (start + 5 * step, 20.0),
    ]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.SUM,
        closed=Closed.RIGHT,
        label=Label.RIGHT,
    )

    assert result == [
        (start, 10.0),
        (start + 5 * step, 20.0),
    ]


@pytest.mark.parametrize(
    ("closed", "label", "pandas_closed", "pandas_label"),
    [
        (Closed.LEFT, Label.LEFT, "left", "left"),
        (Closed.LEFT, Label.RIGHT, "left", "right"),
        (Closed.RIGHT, Label.LEFT, "right", "left"),
        (Closed.RIGHT, Label.RIGHT, "right", "right"),
    ],
)
def test_resample_function_matches_pandas(
    closed: Closed,
    label: Label,
    pandas_closed: Literal["left", "right"],
    pandas_label: Literal["left", "right"],
) -> None:
    """Test the one-shot API against pandas with matching closed/label settings."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)
    data = [(start + i * step, float(i + 1)) for i in range(10)]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        closed=closed,
        label=label,
    )

    pandas_series = pd.Series(
        [value for _, value in data],
        index=pd.DatetimeIndex([timestamp for timestamp, _ in data]),
        dtype="float64",
    )
    pandas_result = pandas_series.resample(
        "5s", closed=pandas_closed, label=pandas_label
    ).mean()
    expected = [
        (timestamp.to_pydatetime(), float(value))
        for timestamp, value in zip(
            pandas_result.index, pandas_result.to_list(), strict=True
        )
    ]

    assert result == expected


def test_label_init_invalid_value() -> None:
    """Test the Label enum rejects invalid values."""
    with pytest.raises(ValueError, match="Invalid label"):
        Label(99)


def test_closed_init_invalid_value() -> None:
    """Test the Closed enum rejects invalid values."""
    with pytest.raises(ValueError, match="Invalid closed"):
        Closed(99)


def test_label_values_members() -> None:
    """Test the Label enum helpers."""
    assert Label.values() == [0, 1]
    assert Label.members() == [("LEFT", 0), ("RIGHT", 1)]


def test_closed_values_members() -> None:
    """Test the Closed enum helpers."""
    assert Closed.values() == [0, 1]
    assert Closed.members() == [("LEFT", 0), ("RIGHT", 1)]


def test_resample_function_empty_data() -> None:
    """Test the resample function with empty data."""
    data: list[tuple[dt.datetime, float | None]] = []

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    assert result == []


def test_resample_function_with_none_values() -> None:
    """Test the resample function with None values."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)

    # First value in each interval is None
    data: list[tuple[dt.datetime, float | None]] = [
        (start + i * step, None if i in (0, 5) else float(i + 1)) for i in range(10)
    ]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    assert len(result) == 2
    # Interval [0, 5): values 2,3,4,5 → avg = 3.5
    # Interval [5, 10): values 7,8,9,10 → avg = 8.5
    assert result[0] == (start, 3.5)
    assert result[1] == (start + 5 * step, 8.5)


def test_resample_function_interval_with_only_none() -> None:
    """Test a bucket that contains only None values."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)

    data: list[tuple[dt.datetime, float | None]] = [
        (start + i * step, None if i < 5 else float(i + 1)) for i in range(10)
    ]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    assert len(result) == 2
    assert result[0] == (start, None)
    assert result[1] == (start + 5 * step, 8.0)


def test_resample_function_sum() -> None:
    """Test the resample function with Sum method."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)

    data = [(start + i * step, float(i + 1)) for i in range(10)]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.SUM,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    assert len(result) == 2
    # Interval [0, 5): sum(1,2,3,4,5) = 15.0
    # Interval [5, 10): sum(6,7,8,9,10) = 40.0
    assert result[0] == (start, 15.0)
    assert result[1] == (start + 5 * step, 40.0)


def test_resample_function_min_max() -> None:
    """Test the resample function with Min and Max methods."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)

    data = [(start + i * step, float(i + 1)) for i in range(10)]

    min_result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.MIN,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )
    max_result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.MAX,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    assert min_result[0] == (start, 1.0)
    assert min_result[1] == (start + 5 * step, 6.0)
    assert max_result[0] == (start, 5.0)
    assert max_result[1] == (start + 5 * step, 10.0)


def test_resample_function_single_sample() -> None:
    """Test the resample function with a single sample."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)

    data = [(start, 42.0)]

    result = resample(
        data,
        dt.timedelta(seconds=5),
        ResamplingFunction.AVERAGE,
        closed=Closed.LEFT,
        label=Label.LEFT,
    )

    assert len(result) == 1
    assert result[0] == (start, 42.0)


def test_resample_function_all_methods() -> None:
    """Test the resample function with all resampling methods."""
    start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    step = dt.timedelta(seconds=1)

    data = [(start + i * step, float(i + 1)) for i in range(5)]

    # Test all methods work without errors
    for method in [
        ResamplingFunction.AVERAGE,
        ResamplingFunction.SUM,
        ResamplingFunction.MIN,
        ResamplingFunction.MAX,
        ResamplingFunction.FIRST,
        ResamplingFunction.LAST,
        ResamplingFunction.COUNT,
        ResamplingFunction.COALESCE,
    ]:
        result = resample(
            data,
            dt.timedelta(seconds=5),
            method,
            closed=Closed.LEFT,
            label=Label.LEFT,
        )
        assert len(result) == 1
        assert result[0][0] == start
