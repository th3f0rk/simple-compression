from simple_compression.compression import SimpleCompression

def test_manual_rle_only():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, sequence=["RLE"])
    decoded = c.decode(encoded)

    assert decoded == data


def test_manual_lz77_only():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, sequence=["LZ77"])
    decoded = c.decode(encoded)

    assert decoded == data

def test_manual_huffman_only():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, sequence=["HUFFMAN"])
    decoded = c.decode(encoded)

    assert decoded == data

def test_manual_rle_then_lz77():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, sequence=["RLE", "LZ77"])
    decoded = c.decode(encoded)

    assert decoded == data

def test_manual_rle_lz77_huffman():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, sequence=["RLE", "LZ77", "HUFFMAN"])
    decoded = c.decode(encoded)

    assert decoded == data

def test_manual_lz77_huffman():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, sequence=["LZ77", "HUFFMAN"])
    decoded = c.decode(encoded)

    assert decoded == data

def test_manual_rle_huffman():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, sequence=["RLE", "HUFFMAN"])
    decoded = c.decode(encoded)

    assert decoded == data

