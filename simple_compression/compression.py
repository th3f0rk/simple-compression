from simple_compression.algorithms.rle import RLE
from simple_compression.algorithms.lz77 import LZ77
from simple_compression.probe import CompressionProbe

HDR_RLE = 0x01
HDR_LZ77 = 0x02

MAGIC_0 = 0x53
MAGIC_1 = 0x43


class SimpleCompression:
    def __init__(self, min_run=3, window_size=4096):
        self.rle = RLE(min_run=min_run)
        self.lz77 = LZ77(window_size=window_size)
        self.probe = CompressionProbe(min_run=min_run)

    def encode(self, data, sequence=None, auto=False):
        if not isinstance(data, bytearray):
            raise Exception("encode requires bytearray input")

        if auto:
            sequence = self._auto_select(data)

        if not sequence:
            return data

        output = data
        headers = bytearray()

        for alg in sequence:
            if alg == "RLE":
                output = self.rle.encode(output)
                headers.append(HDR_RLE)
            elif alg == "LZ77":
                output = self.lz77.encode(output)
                headers.append(HDR_LZ77)
            else:
                raise Exception("Unknown algorithm")

        framed = bytearray()
        framed.append(MAGIC_0)
        framed.append(MAGIC_1)
        framed.append(len(headers))
        framed.extend(headers)
        framed.extend(output)
        return framed

    def decode(self, data):
        if not isinstance(data, bytearray):
            raise Exception("decode requires bytearray input")

        if len(data) < 3:
            return data

        if data[0] != MAGIC_0 or data[1] != MAGIC_1:
            return data

        header_count = data[2]
        cursor = 3

        if len(data) < cursor + header_count:
            raise Exception("Invalid frame")

        headers = data[cursor:cursor + header_count]
        cursor += header_count

        output = data[cursor:]

        i = len(headers) - 1
        while i >= 0:
            header = headers[i]
            if header == HDR_RLE:
                output = self.rle.decode(output)
            elif header == HDR_LZ77:
                output = self.lz77.decode(output)
            else:
                raise Exception("Invalid header")
            i -= 1

        return output

    def _auto_select(self, data):
        metrics = self.probe.analyze(data)
        sequence = []

        if metrics["use_rle"]:
            sequence.append("RLE")
        if metrics["use_lz77"]:
            sequence.append("LZ77")

        return sequence

