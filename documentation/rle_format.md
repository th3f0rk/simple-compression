# RLE Formatting

---

## Input / Output

This RLE module operates exclusively on `bytearray` objects.

It assumes the caller is responsible for extracting raw bytes from files or other sources.
The format is designed to compose cleanly with LZ77 and future entropy coders.

---

## Global Parameters

- Minimum match length: configurable (default: 3)
- Count encoding: unsigned 8-bit integer (1–255)
- Value encoding: single raw byte

---

## Token Stream Overview

The compressed output is a linear stream of tokens. Each token begins with a single control byte,
followed by a fixed-size payload determined by the token type.

There are two token types:

- Literal token
- Run token

### Literal Token

A literal token encodes a single byte with no compression.

```
[control_byte = 0x00] [literal_value]
```

Total size: 2 bytes

### Run Token

A run token encodes a repeated byte sequence.

```
[control_byte = 0x01] [count] [value]
```

- `count` is the number of repetitions (1–255)
- `value` is the byte to repeat

Total size: 3 bytes

---

## Run Splitting Behavior

Because `count` is stored as an unsigned 8-bit integer, the maximum representable run length
in a single token is 255.

If an input run exceeds this length, the encoder **must split the run** into multiple consecutive
run tokens. Each token encodes up to 255 repetitions of the same value.

This splitting is transparent to the decoder and does not affect correctness.

---

## Validity Rules

A run token is invalid if:

- `count == 0`
- `count` exceeds 255
- `count < min_run_length` (encoder-side invariant)

Invalid data must cause the decoder to raise an error and abort decoding. This prevents silent corruption
and guards against malformed or malicious streams.

---

## Stream Termination

The stream ends when all bytes are consumed.
There is no padding and no sentinel token.

The decoder must not read past the end of the input buffer.

---

## Example

Original data:

```python
bytearray(b"A" * 300)
```

Conceptual tokens:

```
Run('A', 255)
Run('A', 45)
```

Serialized output:

```python
bytearray([
    0x01, 0xFF, 0x41,
    0x01, 0x2D, 0x41
])
```

---

## Decoder Behavior

Decoding is strictly sequential.

1. Read one control byte
2. If control is `0x00`, read one byte and append it
3. If control is `0x01`, read count and value, then append value `count` times

Decoding completes when the input buffer is exhausted.
