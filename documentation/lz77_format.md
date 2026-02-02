# LZ77 formatting

---

## Input / Output

This LZ77 module operates exclusively on `bytearray` objects.

It assumes the caller is responsible for extracting raw bytes from files or other sources.
The format is designed to compose with RLE and future entropy coders.

The encoding implementation uses internal indexing and hashing-based acceleration
structures to achieve linear-time behavior. These structures are strictly internal
to the encoder and do not affect the serialized format, decoding semantics, or
cross-language compatibility.

---

## Global Parameters

- Window size: 4096 bytes
- Minimum match length: 3
- Maximum match length: 255
- Distance encoding: unsigned 16-bit integer

These parameters define the valid bounds for encoded tokens.
The encoder **must enforce these constraints**, regardless of the specific
match-finding strategy used.

---

## Token Stream Overview

The compressed output is a linear stream of tokens. Each token begins with a single control byte,
followed by a fixed-size payload determined by the token type.

There are two token types:

- Literal token
- Match token

### Literal Token

A literal token encodes a single raw byte.

```
[control_byte = 0x00] [literal_value]
```

Total size: 2 bytes

### Match Token

A match token encodes a backward reference into already-decoded output.

```
[control_byte = 0x01] [distance_hi] [distance_lo] [length]
```

- `distance` is how far back from the current output position to copy
- `length` is how many bytes to copy

Total size: 4 bytes

---

## Validity Rules

A match token is invalid if:

- `distance == 0`
- `distance > window_size`
- `distance > current_output_length`
- `length < min_match_length`
- `length == 0`

Invalid data must cause the decoder to raise an error and abort decoding.

---

## Stream Termination

The stream ends when all bytes are consumed.
There is no padding and no sentinel token.

The decoder must not read past the end of the input buffer.

---

## Example

Original data:

```python
bytearray(b"ABABABABX")
```

Conceptual tokens:

```
Literal('A')
Literal('B')
Match(distance=2, length=6)
Literal('X')
```

Serialized output:

```python
bytearray([
    0x00, 0x41,
    0x00, 0x42,
    0x01, 0x00, 0x02, 0x06,
    0x00, 0x58
])
```

---

## Decoder Behavior

Decoding is strictly sequential.

1. Read one control byte
2. If control is `0x00`, read one byte and append it
3. If control is `0x01`, read distance and length, then copy from prior output

Decoding completes when the input buffer is exhausted.
