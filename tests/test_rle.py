from simple_compression.algorithms.rle import RLE

def test_rle_round_trip():
    rle = RLE()
    data = bytearray(b"AAAAAAABBBBBCCCCDDDDDAA")

    encoded = rle.encode(data)
    decoded = rle.decode(encoded)

    assert decoded == data

