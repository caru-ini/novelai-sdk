"""
Copyright (c) 2025 caru-ini

This file includes code from https://github.com/NovelAI/novelai-image-metadata,
which is licensed under the MIT License:

Copyright (c) 2023 NovelAI
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import gzip
import json
from typing import Any, TypeAlias

import numpy as np
from numpy.typing import NDArray
from PIL import Image

AlphaChannel: TypeAlias = NDArray[np.uint8]
PackedBytes: TypeAlias = NDArray[np.uint8]
ImageArray: TypeAlias = NDArray[np.uint8]


def byteize(alpha: AlphaChannel) -> PackedBytes:
    alpha = alpha.T.reshape((-1,))
    alpha = alpha[: (alpha.shape[0] // 8) * 8]
    alpha = np.bitwise_and(alpha, 1)
    alpha = alpha.reshape((-1, 8))
    alpha = np.packbits(alpha, axis=1)
    return alpha


class LSBExtractor:
    def __init__(self, data: ImageArray) -> None:
        self.data: PackedBytes = byteize(data[..., -1])
        self.pos: int = 0

    def get_one_byte(self) -> PackedBytes:
        byte = self.data[self.pos]
        self.pos += 1
        return byte

    def get_next_n_bytes(self, n: int) -> bytearray:
        n_bytes = self.data[self.pos : self.pos + n].reshape(-1)
        self.pos += n
        return bytearray(n_bytes)

    def read_32bit_integer(self) -> int | None:
        bytes_list = self.get_next_n_bytes(4)
        if len(bytes_list) == 4:
            integer_value = int.from_bytes(bytes_list, byteorder="big")
            return integer_value
        else:
            return None


def extract_image_metadata(
    image: Image.Image | NDArray[np.uint8], get_fec: bool = False
) -> dict[str, Any] | tuple[dict[str, Any], bytearray | None]:
    if isinstance(image, Image.Image):
        np_image = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    else:
        np_image = np.asarray(image, dtype=np.uint8)

    if not (np_image.shape[-1] == 4 and np_image.ndim == 3):
        raise ValueError("Invalid image format")

    reader = LSBExtractor(np_image)
    magic = "stealth_pngcomp"
    read_magic = reader.get_next_n_bytes(len(magic)).decode("utf-8")
    assert magic == read_magic, "magic number"
    read_len_bits = reader.read_32bit_integer()
    if read_len_bits is None:
        raise ValueError("Failed to read metadata length")
    read_len = read_len_bits // 8
    json_data_bytes = reader.get_next_n_bytes(read_len)
    json_data = json.loads(gzip.decompress(json_data_bytes).decode("utf-8"))
    if "Comment" in json_data and isinstance(json_data["Comment"], str):
        json_data["Comment"] = json.loads(json_data["Comment"])

    if not get_fec:
        return json_data

    fec_len_bits = reader.read_32bit_integer()
    if fec_len_bits is None:
        raise ValueError("Failed to read FEC length")
    fec_len = fec_len_bits
    fec_data = None
    if fec_len != 0xFFFFFFFF:
        fec_data = reader.get_next_n_bytes(fec_len // 8)

    return json_data, fec_data
