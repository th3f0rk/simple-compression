class RLE:
    def __init__(self, min_run=3):
        self.min_run = min_run

    def encode(self, data):
        if not isinstance(data, bytearray):
            raise Exception("RLE encode requires bytearray input")

        if len(data) < self.min_run * 2:
            return data

        output = bytearray()

        current_value = data[0]
        count = 1
        cursor = 1

        def emit_run(count, value):
            while count > 255:
                output.append(0x01)
                output.append(255)
                output.append(value)
                count -= 255
            if count >= self.min_run:
                output.append(0x01)
                output.append(count)
                output.append(value)
            else:
                for _ in range(count):
                    output.append(0x00)
                    output.append(value)

        while cursor < len(data):
            if data[cursor] == current_value:
                count += 1
            else:
                emit_run(count, current_value)
                current_value = data[cursor]
                count = 1
            cursor += 1

        emit_run(count, current_value)

        return output

    def decode(self, data):
        if not isinstance(data, bytearray):
            raise Exception("RLE decode requires bytearray input")

        output = bytearray()
        cursor = 0

        while cursor < len(data):
            token = data[cursor]
            cursor += 1

            if token == 0x00:
                value = data[cursor]
                cursor += 1
                output.append(value)

            elif token == 0x01:
                count = data[cursor]
                cursor += 1
                value = data[cursor]
                cursor += 1

                repeated = 0
                while repeated < count:
                    output.append(value)
                    repeated += 1

            else:
                raise Exception("Invalid RLE token")

        return output

