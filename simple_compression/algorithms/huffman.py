from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Node:
    weight: int
    byte: Optional[int] = field(default=None, compare=False)
    left: Optional["Node"] = field(default=None, compare=False)
    right: Optional["Node"] = field(default=None, compare=False)

class HUFFMAN:

    def encode(self, data):

        map = {}

        for byte in data:
            if byte in map:
                map[byte] += 1
            else:
                map[byte] = 1

        nodes = []
        for key, value in map.items():
            nodes.append(Node(value, key))

        while len(nodes) != 1:
            nodes.sort()
            node1 = nodes[0]
            node2 = nodes[1]
            nodes.remove(node1)
            nodes.remove(node2)
            nodes.append(Node(node1.weight + node2.weight, None, node1, node2))

        root = nodes[0]

        codes = {}
        bits = 0
        length = 0

        def walk(node, bits, length):
            if node.byte is not None:
                codes[node.byte] = (bits, length)
                return
            if node.left is not None:
                left_bits = bits << 1
                left_len = length + 1
                walk(node.left, left_bits, left_len)
            if node.right is not None:
                right_bits = (bits << 1) | 1
                right_len = length + 1
                walk(node.right, right_bits, right_len)

        walk(root, bits, length)

        lengths = {}
        for byte, (code_bits, code_len) in codes.items():
            lengths[byte] = code_len

        canonical_codes = {}
        pairs = []
        for byte, code_len in lengths.items():
            pairs.append((code_len, byte))

        pairs.sort()

        current_code = 0
        previous_len = 0
        for code_len, byte in pairs:
            if code_len > previous_len:
                current_code <<= (code_len - previous_len)
            canonical_codes[byte] = (current_code, code_len)
            current_code += 1
            previous_len = code_len

        out_bits = 0
        out_len = 0

        header = bytearray()

        for byte in data:
            code_bits, code_len = canonical_codes[byte]
            out_bits = (out_bits << code_len) | code_bits
            out_len += code_len

        for byte, (code_bits, code_len) in canonical_codes.items():
            header.append(code_len)
            header.append(byte)

        bitstream = bytearray()
        bitstream.extend(len(map).to_bytes(2, "big"))
        bitstream = bitstream + header
        bitstream.extend(out_len.to_bytes(4, "big"))
        num_bytes = (out_len + 7) // 8
        pad = (num_bytes * 8) - out_len
        out_bits = out_bits << pad
        packed = out_bits.to_bytes(num_bytes, "big")
        bitstream.extend(packed)

        return bitstream

    def decode(self, data):

        def header_parse(data):
            pairs = []
            symbol_count = int.from_bytes(data[0:2], "big")
            header_length = symbol_count * 2
            cursor = 2
            for i in range(cursor, cursor + header_length, 2):
                code_length = data[i]
                symbol = data[i+1]
                pairs.append((code_length, symbol))
                cursor += 2
            return pairs, cursor

        def reconstruct_huffman(pairs):
            remade_codes = {}
            pairs.sort()
            current_code = 0
            previous_len = 0
            for code_len, symbol in pairs:
                if code_len > previous_len:
                    current_code <<= (code_len - previous_len)
                remade_codes[symbol] = (current_code, code_len)
                current_code += 1
                previous_len = code_len
            return remade_codes

        def bitstream_slice(data, cursor):
            bitstream = bytearray()
            for i in range(cursor, len(data), 1):
                bitstream.append(data[i])
            return bitstream

        pairs, cursor = header_parse(data)
        remade_codes = reconstruct_huffman(pairs)

        rename_codes = {}
        for symbol, (bits, length) in remade_codes.items():
            rename_codes[(bits, length)] = symbol

        bit_len = int.from_bytes(data[cursor:cursor+4], "big")
        cursor += 4

        bitstream = bitstream_slice(data, cursor)

        def parse_bits(bitstream, bit_len):
            prefix = 0
            length = 0
            bits_read = 0
            decoded = bytearray()
            for byte in bitstream:
                bit_position = 7
                while bit_position >= 0:
                    if bits_read >= bit_len:
                        return decoded
                    bit = (byte >> bit_position) & 1
                    bit_position -= 1
                    prefix = (prefix << 1) | bit
                    length += 1
                    bits_read += 1
                    if (prefix, length) in rename_codes:
                        symbol = rename_codes[(prefix, length)]
                        decoded.append(symbol)
                        prefix = 0
                        length = 0
            return decoded

        decoded = parse_bits(bitstream, bit_len)
        return decoded

