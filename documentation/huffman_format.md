# Huffman Formatting

---

## Input / Output
 
This Huffman module operaters exclusively on `bytearray` objects.

It assumes the user is responisble for extracting raw bytes from files or other sources.
The format is designed to compose with RLE and LZ77 to further compress the data as far as its entropy allows.

The encoding implementation is a canonical Huffman Coding implemetation based on the original research paper.
It was designed to be effectively O(n + k log k) time complexity where k is the number of symbols and is limited 
in speed by the probe when doing auto sequencing as well as by Python's overhead. The encoding uses a huffman tree 
to create the codes and arranges them in the bitsream. The encoding process also prepends a header which contains 
the information needed by the decoder to reconstruct the codes and lengths to decode losslessly. This header is 
indepentent of the library's sequencing header which is used to determine the sequence algorithms were applied 
in encoding to properly decode.

---

## Global Parameters

There are technically not any global parameters that can be defined by the user, there are only limitations.
There are some internal parameters that are defined such as the Node class used to build the tree:

```python
@dataclass(order=True)
class Node:
    weight: int
    byte: Optional[int] = field(default=None, compare=False)
    left: Optional["Node"] = field(default=None, compare=False)
    right: Optional["Node"] = field(default=None, compare=False)
```

---

## Bitstream Overview

The compressed output is a linear stream of bits. The header is first constructed by appending the alphabet
size then appending `code_len` and corresponding `byte` or symbol which was used to construct the codes used
in the bitstream. The order of the header is significant for how the decoder parses it and reconstructs the
codes and lengths to decode the bitstream. The rest of the output is constructed first by appending the `out_len`
which tells the decoder how many bits are in the bitstream. The bitstream that follows is the raw huffman encoded data.
the padding of the bits ended up being essential to keeping the output lossless as without it leading zeros
would be ambiguous and the decoder struggle.

---

## Data Reconstruction

The decoder first will parse the header to deterministically reconstruct the codes in the same fashion as 
the encoder. Once it has parsed the header and `out_len` it can faithfully reverse the output of the encoder 
in a lossless fashion.
