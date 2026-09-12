#!/usr/bin/env python3
"""Crop an 8-bit RGBA, non-interlaced PNG using only the Python stdlib."""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path


def chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def unfilter_rows(raw: bytes, width: int, height: int) -> list[bytearray]:
    bytes_per_pixel = 4
    stride = width * bytes_per_pixel
    rows: list[bytearray] = []
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        row = bytearray(raw[offset : offset + stride])
        offset += stride
        for index in range(stride):
            left = row[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            above = previous[index]
            upper_left = previous[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            if filter_type == 1:
                row[index] = (row[index] + left) & 255
            elif filter_type == 2:
                row[index] = (row[index] + above) & 255
            elif filter_type == 3:
                row[index] = (row[index] + (left + above) // 2) & 255
            elif filter_type == 4:
                estimate = left + above - upper_left
                pa = abs(estimate - left)
                pb = abs(estimate - above)
                pc = abs(estimate - upper_left)
                predictor = left if pa <= pb and pa <= pc else above if pb <= pc else upper_left
                row[index] = (row[index] + predictor) & 255
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type}")
        rows.append(row)
        previous = row
    return rows


def main() -> None:
    if len(sys.argv) != 7:
        raise SystemExit("usage: crop_png.py input.png output.png x0 y0 x1 y1")
    source, destination = map(Path, sys.argv[1:3])
    x0, y0, x1, y1 = map(int, sys.argv[3:])
    payload = source.read_bytes()
    position = 8
    width = height = depth = color = interlace = None
    image_data = bytearray()
    while position < len(payload):
        length = struct.unpack(">I", payload[position : position + 4])[0]
        kind = payload[position + 4 : position + 8]
        data = payload[position + 8 : position + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color, _, _, interlace = struct.unpack(">IIBBBBB", data)
        elif kind == b"IDAT":
            image_data.extend(data)
        position += length + 12
    if (depth, color, interlace) != (8, 6, 0):
        raise ValueError("expected an 8-bit RGBA, non-interlaced PNG")
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError("crop rectangle is outside the source image")
    rows = unfilter_rows(zlib.decompress(image_data), width, height)
    cropped = bytearray()
    for row in rows[y0:y1]:
        cropped.append(0)
        cropped.extend(row[x0 * 4 : x1 * 4])
    output = bytearray(b"\x89PNG\r\n\x1a\n")
    output.extend(chunk(b"IHDR", struct.pack(">IIBBBBB", x1 - x0, y1 - y0, 8, 6, 0, 0, 0)))
    output.extend(chunk(b"IDAT", zlib.compress(bytes(cropped), 9)))
    output.extend(chunk(b"IEND", b""))
    destination.write_bytes(output)


if __name__ == "__main__":
    main()
