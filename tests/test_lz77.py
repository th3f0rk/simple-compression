from simple_compression.algorithms.lz77 import LZ77

def test_lz77_round_trip():
    lz = LZ77()
    data = bytearray(b"ABCABCABCABCABC")

    encoded = lz.encode(data)
    decoded = lz.decode(encoded)

    assert decoded == data


