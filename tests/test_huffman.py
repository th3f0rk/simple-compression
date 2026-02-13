from simple_compression.algorithms.huffman import HUFFMAN

def test_huffman_round_trip():
    huffman = HUFFMAN()
    data = bytearray(b"ABCABCABCABCABC")

    encoded = huffman.encode(data)
    decoded = huffman.decode(data)

    assert decoded == data
