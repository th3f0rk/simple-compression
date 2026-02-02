class LZ77:
    def __init__(self, window_size=4096, min_match=3, max_match=255):
        self.window_size = window_size
        self.min_match = min_match
        self.max_match = max_match

    def encode(self, data):
        output = bytearray()
        cursor = 0

        index = {}

        while cursor < len(data):
            if cursor - self.window_size > 0:
                back_start = cursor - self.window_size
            else:
                back_start = 0

            back_end = cursor
            ahead_start = cursor

            max_ahead = ahead_start + self.max_match
            if max_ahead < len(data):
                ahead_end = max_ahead
            else:
                ahead_end = len(data)

            best_length = 0
            best_distance = 0

            if cursor + 2 < len(data):
                key = (data[cursor], data[cursor + 1], data[cursor + 2])
                candidates = index.get(key, [])
            else:
                key = None
                candidates = []

            for j in reversed(candidates):
                if j < back_start:
                    break

                k = 0
                while k < min(ahead_end - ahead_start, back_end - j):
                    if data[j + k] == data[ahead_start + k]:
                        k += 1
                    else:
                        break

                match_length = k
                match_distance = cursor - j

                if match_length > best_length:
                    best_length = match_length
                    best_distance = match_distance

            if best_length >= self.min_match:
                output.append(0x01)

                high = (best_distance >> 8) & 0xFF
                low = best_distance & 0xFF

                output.append(high)
                output.append(low)
                output.append(best_length)

                step = best_length
            else:
                output.append(0x00)
                output.append(data[cursor])
                step = 1

            for i in range(step):
                pos = cursor + i
                if pos + 2 < len(data):
                    k = (data[pos], data[pos + 1], data[pos + 2])
                    lst = index.setdefault(k, [])
                    lst.append(pos)

                    if len(lst) > 64:
                        del lst[0]

            cursor += step

        return output

    def decode(self, data):
        output = bytearray()
        cursor = 0

        while cursor < len(data):
            token = data[cursor]
            cursor += 1

            if token == 0x00:
                literal = data[cursor]
                cursor += 1
                output.append(literal)

            elif token == 0x01:
                high = data[cursor]
                cursor += 1
                low = data[cursor]
                cursor += 1

                distance = (high << 8) | low

                length = data[cursor]
                cursor += 1

                copy_start = len(output) - distance
                copy_index = copy_start
                copied = 0

                while copied < length:
                    output.append(output[copy_index])
                    copy_index += 1
                    copied += 1

            else:
                raise ValueError("Invalid LZ77 token")

        return output

