"""Disk performance benchmarking tool.

This module provides a simple command line interface to measure sequential
write and read throughput on the current filesystem. The tool writes a test
file and measures how long it takes to write and read the data using a chosen
block size.
"""
from __future__ import annotations

import argparse
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class BenchmarkResult:
    """Container for benchmark results."""

    write_seconds: float
    read_seconds: float
    total_bytes: int

    @property
    def write_speed(self) -> float:
        """Return the write throughput in MB/s."""

        return self._bytes_per_second(self.write_seconds) / (1024 ** 2)

    @property
    def read_speed(self) -> float:
        """Return the read throughput in MB/s."""

        return self._bytes_per_second(self.read_seconds) / (1024 ** 2)

    def _bytes_per_second(self, seconds: float) -> float:
        return self.total_bytes / seconds if seconds > 0 else float("inf")


def _write_test_file(path: Path, total_bytes: int, block_size: int) -> float:
    """Write ``total_bytes`` random bytes to ``path`` using ``block_size`` chunks."""

    data_block = os.urandom(block_size)
    written = 0
    start = time.perf_counter()

    with path.open("wb", buffering=0) as fh:
        full_blocks, remainder = divmod(total_bytes, block_size)
        for _ in range(full_blocks):
            fh.write(data_block)
            written += block_size
        if remainder:
            fh.write(data_block[:remainder])
            written += remainder
        fh.flush()
        os.fsync(fh.fileno())

    end = time.perf_counter()
    if written != total_bytes:
        raise IOError(f"Expected to write {total_bytes} bytes but wrote {written}")
    return end - start


def _read_test_file(path: Path, block_size: int) -> float:
    """Read ``path`` sequentially using ``block_size`` chunks."""

    start = time.perf_counter()
    with path.open("rb", buffering=0) as fh:
        while fh.read(block_size):
            pass
    end = time.perf_counter()
    return end - start


def run_benchmark(
    *,
    directory: Optional[Path],
    filename: Optional[str],
    total_size_mb: float,
    block_size_kb: int,
    keep_file: bool,
) -> BenchmarkResult:
    """Run a disk benchmark and return the measured result."""

    if total_size_mb <= 0:
        raise ValueError("total_size_mb must be positive")
    if block_size_kb <= 0:
        raise ValueError("block_size_kb must be positive")

    total_bytes = int(total_size_mb * 1024 ** 2)
    block_size = block_size_kb * 1024

    if filename:
        test_path = (directory or Path.cwd()) / filename
    else:
        handle = tempfile.NamedTemporaryFile(prefix="disk-benchmark-", delete=False, dir=directory)
        test_path = Path(handle.name)
        handle.close()

    try:
        write_seconds = _write_test_file(test_path, total_bytes, block_size)
        read_seconds = _read_test_file(test_path, block_size)
    finally:
        if not keep_file and test_path.exists():
            try:
                test_path.unlink()
            except OSError:
                pass

    return BenchmarkResult(
        write_seconds=write_seconds,
        read_seconds=read_seconds,
        total_bytes=total_bytes,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple disk throughput benchmark")
    parser.add_argument(
        "--size",
        type=float,
        default=100.0,
        help="Size of the test file in MB (default: 100 MB)",
    )
    parser.add_argument(
        "--block-size",
        type=int,
        default=1024,
        help="Block size in KB for read/write operations (default: 1024 KB)",
    )
    parser.add_argument(
        "--directory",
        type=Path,
        default=None,
        help="Directory to store the test file. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="Optional filename for the test file. If omitted, a temporary file is used.",
    )
    parser.add_argument(
        "--keep-file",
        action="store_true",
        help="Keep the test file after the benchmark completes.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = run_benchmark(
        directory=args.directory,
        filename=args.filename,
        total_size_mb=args.size,
        block_size_kb=args.block_size,
        keep_file=args.keep_file,
    )

    print(f"Disk benchmark completed for {args.size:.2f} MB file")
    print(f"Write: {result.write_speed:.2f} MB/s (time: {result.write_seconds:.3f}s)")
    print(f"Read: {result.read_speed:.2f} MB/s (time: {result.read_seconds:.3f}s)")


if __name__ == "__main__":
    main()
