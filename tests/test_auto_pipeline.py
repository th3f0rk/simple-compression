from simple_compression.compression import SimpleCompression

def test_auto_uses_rle():
    c = SimpleCompression()
    data = bytearray(b"AAAAAAAB")

    encoded = c.encode(data, auto=True)
    decoded = c.decode(encoded)

    assert decoded == data


def test_auto_uses_lz77():
    c = SimpleCompression()
    data = bytearray(b"ABCABCABCABC")

    encoded = c.encode(data, auto=True)
    decoded = c.decode(encoded)

    assert decoded == data


def test_auto_uses_rle_then_lz77():
    c = SimpleCompression()
    data = bytearray(b"AAAAABBBBBCCCCCAAAAABBBBB")

    encoded = c.encode(data, auto=True)
    decoded = c.decode(encoded)

    assert decoded == data


def test_auto_negative_tech_passthrough():
    c = SimpleCompression()
    data = bytearray(b"\x01\xA9\x3F\x7C\xD2\x88\x10")

    encoded = c.encode(data, auto=True)
    decoded = c.decode(encoded)

    assert decoded == data

