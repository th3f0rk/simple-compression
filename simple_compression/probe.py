class CompressionProbe:
    def __init__(self, min_run=3):
        self.min_run = min_run

    def analyze(self, data):
        if not isinstance(data, bytearray):
            raise Exception("probe requires bytearray input")

        has_runs = False
        has_repetition = False

        i = 0
        while i < len(data) - 1:
            run_length = 1
            while i + run_length < len(data) and data[i] == data[i + run_length]:
                run_length += 1

            if run_length >= self.min_run:
                has_runs = True
                break

            i += run_length

        seen = {}
        for b in data:
            seen[b] = seen.get(b, 0) + 1
            if seen[b] > 2:
                has_repetition = True
                break

        return {
            "use_rle": has_runs,
            "use_lz77": has_repetition
        }

