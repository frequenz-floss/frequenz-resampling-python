# Frequenz Resampling

[![Build Status](https://github.com/frequenz-floss/frequenz-resampling-python/actions/workflows/ci.yaml/badge.svg)](https://github.com/frequenz-floss/frequenz-resampling-python/actions/workflows/ci.yaml)
[![PyPI Package](https://img.shields.io/pypi/v/frequenz-resampling)](https://pypi.org/project/frequenz-resampling/)
[![Docs](https://img.shields.io/badge/docs-latest-informational)](https://frequenz-floss.github.io/frequenz-resampling-python/)

## Introduction

`frequenz-resampling` provides fast, typed resampling for timestamped numeric
data in Python.

The library is backed by the Rust resampler
[`frequenz-floss/frequenz-resampling-rs`](https://github.com/frequenz-floss/frequenz-resampling-rs)
and exposed through a small Python API. It supports incremental stream
resampling through a `Resampler` object as well as one-shot resampling with the
`resample()` convenience function.

Main capabilities:

- fixed-interval resampling with timezone-aware `datetime` timestamps
- configurable interval semantics via `Closed` and `Label`
- multiple aggregation functions via `ResamplingFunction`:
  `AVERAGE`, `SUM`, `MAX`, `MIN`, `FIRST`, `LAST`, `COUNT`, `COALESCE`
- typed Python API (`py.typed`) and generated API docs

## Supported Platforms

The following platforms are officially supported (tested):

- **Python:** 3.11, 3.12, 3.13, 3.14
- **Operating System:** Ubuntu Linux 24.04, Windows, macOS
- **Architectures:** amd64, arm64

## Quick Start

### Install

```sh
python -m pip install frequenz-resampling
```

### Stream resampling with `Resampler`

```python
import datetime as dt

from frequenz.resampling import Closed, Label, Resampler, ResamplingFunction

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

for i in range(10):
    resampler.push_sample(timestamp=start + i * step, value=float(i + 1))

result = resampler.resample(start + 10 * step)
print(result)
# [(1970-01-01 00:00:05+00:00, 3.0), (1970-01-01 00:00:10+00:00, 8.0)]
```

### One-shot resampling with `resample()`

```python
import datetime as dt

from frequenz.resampling import Closed, Label, ResamplingFunction, resample

start = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
step = dt.timedelta(seconds=1)
data = [(start + i * step, float(i + 1)) for i in range(10)]

result = resample(
    data,
    dt.timedelta(seconds=5),
    ResamplingFunction.SUM,
    closed=Closed.LEFT,
    label=Label.RIGHT,
)
print(result)
```

## Documentation

- User and API documentation:
  <https://frequenz-floss.github.io/frequenz-resampling-python/>
- Changelog / releases:
  <https://github.com/frequenz-floss/frequenz-resampling-python/releases>

## Contributing

Contributions are welcome. For development setup, testing, docs, and release
workflow, see the [Contributing Guide](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
