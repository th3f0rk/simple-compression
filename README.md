# simple-compression

`simple-compression` is a small Python library that implements classic byte-oriented compression algorithms with an explicit and composable API.

The library is designed to operate directly on `bytearray` data and provides both manual and automatic compression pipelines. All encoded outputs are self-describing and can be decoded without external metadata.

Current version: **v0.2.0**

---

## Scope and goals

This project focuses on:

- Correct, deterministic implementations of classic compression algorithms
- Explicit encoding formats that are easy to inspect and reason about
- A simple API for chaining multiple compression stages
- Safe and strict decoding

This library does **not** attempt to compete with production compressors in performance. It is intended for correctness, clarity, and control. 
**BECAUSE OF PYTHON OVERHEAD THIS IS VERY SLOW AND NOT PRACTICAL FOR PRODUCTION USE**
**AS OF RIGHT NOW THIS LIBRARY IS BEST DESIGNED FOR LEARNING ABOUT COMPRESSION EVENTUALLY IT WILL BE REWRITTEN IN C AND OPTIMIZED FOR PERFORMANCE**

---

## Implemented algorithms

- Run-Length Encoding (RLE)
- LZ77
- Huffman

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
[HUFFMAN Format](documentation/huffman_format.md)

---

## Road Map

Currently the library is functional. It has a composable pipeline of basic compression algorithms. 
The probe for the `auto=True` argument has been redesigned to be more tunable and collect more metrics. 
In testing it does better at avoiding using algorithms when the data doesn't fit their use case.
The next part of development will be focused on rewritting the library in C so it can be usable outside of an educational setting.

---

## License 

**MIT**
