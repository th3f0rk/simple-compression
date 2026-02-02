# simple-compression

`simple-compression` is a small Python library that implements classic byte-oriented compression algorithms with an explicit and composable API.

The library is designed to operate directly on `bytearray` data and provides both manual and automatic compression pipelines. All encoded outputs are self-describing and can be decoded without external metadata.

Current version: **v0.1.0**

---

## Scope and goals

This project focuses on:

- Correct, deterministic implementations of classic compression algorithms
- Explicit encoding formats that are easy to inspect and reason about
- A simple API for chaining multiple compression stages
- Safe and strict decoding

This library does **not** attempt to compete with production compressors in performance. It is intended for correctness, clarity, and control.

---

## Implemented algorithms

- Run-Length Encoding (RLE)
- LZ77

Each algorithm has a fully defined binary format and a strict decoder.

---

## Installation

```bash
pip install simple-compression
```

---

## Basic Usage

**Both of these features are expected to improve in effectiveness with more testing and tuning as well as the future implementation of a Huffman Algorithm**
The first usage uses the `auto=True` argument does a quick pass on the data to gather metrics to automatically select the algorithms and their sequence.
The second usage passes the algorithm name as arguments to manually select algorithms and determine their sequence.

```python
from simple_compression.compression import SimpleCompression

compress = SimpleCompression()

data = bytearray(b"AAAAAABBBBBCCDSADDDDDSSSCVZCSSSSWEEEFWEWAFZCVAGQWTQL")

encoded = compress.encode(data, auto=True)
decoded = compress.decode(encoded)

encoded = compress.encode(data, sequence=["RLE", "LZ77"])
decoded = compress.decode(encoded)
```
The decoder reads header tokens embedded at the start of the bitstream to determine which algorithms were applied and in which order.
This allows for a really robust decoder which when combined with the spec documentation for each algorithm can be helpful in implementing decoders in other languages.

---

## Algorithm Formatting

Detailed binary formats for each algorithm are documented below.
[RLE Format](documentation/rle_format.md)
[LZ77 Format](documentation/lz77_format.md)

---

## Road Map

First is implementing a Huffman algorithm to really take advantage of the sequencing ability of this library.
As features are added the automatic sequencing feature will be continuously tuned to ensure that rle is only enabled when it doesn't infalte the input. 
As algorithms are added sequencing logic and metrics will develop alongside.

---

## License 

**MIT**
