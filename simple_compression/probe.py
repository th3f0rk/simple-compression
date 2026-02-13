import random
from math import log2

class CompressionProbe:
    def __init__(self, min_run = 3):
        self.min_run = min_run
        self.use_RLE = False
        self.use_LZ77 = False
        self.use_HUFFMAN = False


    def analyze(self, data):
        if not isinstance(data, bytearray):
            raise Exception("Probe layer requires bytearray input as does all compression algorithms for this library")

        data_len = len(data)
        max_split = data_len // 5
        max_window_size = max_split - (data_len // 8)
        min_window_size = max_window_size // 4
        
        start_index = 0
        window_count = 0
        windows = {}
        for i in range(0, data_len - 1, max_split):
            window_size = random.randrange(min_window_size, max_window_size)
            end_index = min(start_index + window_size, data_len)  # prevent overflow
            window_count += 1
            windows[window_count] = (start_index, end_index)
            start_index = start_index + (max_split + 1)

        results = {}
        window_count = 0

        # iterate through windows
        for (key, (start, end)) in windows.items():
            window_count += 1

            # rle run length metrics
            cursor = start
            window_size = end - start
            run_list = []
            run_total = 0
            run_count = 0
            avg_run = 0
            run_freq = 0
            run_coverage = 0
            rle_gain = 0

            while cursor < end:
                run_length = 1
                while cursor + run_length < end and data[cursor] == data[cursor + run_length]:
                    run_length += 1
                if run_length >= self.min_run:
                    run_count += 1
                    run_list.append(run_length)
                    cursor += run_length
                else:
                    cursor += 1
            if run_list:
                for i in run_list:
                    run_total += i
                avg_run = run_total / len(run_list)
                run_freq = run_count / window_size
                run_coverage = run_total / window_size
                overhead = 3
                rle_gain = run_total - (run_count * overhead)
            
            #LZ77 Metrics
            chunk_size = 4
            cursor = start
            window_size = end - start
            match_count = 0
            total_match_bytes = 0
            max_match_length = 0
            match_coverage = 0
            lz77_gain = 0

            seen = {}

            while cursor + chunk_size < end:

                chunk = bytes(data[cursor:cursor + chunk_size])

                if chunk in seen:
                    prev_pos = seen[chunk]
                    match_length = chunk_size

                    # extend match forward
                    while (cursor + match_length < end and
                           prev_pos + match_length < end and
                           data[cursor + match_length] == data[prev_pos + match_length]):
                        match_length += 1

                    if match_length > chunk_size:
                        match_count += 1
                        total_match_bytes += match_length

                        if match_length > max_match_length:
                            max_match_length = match_length

                        cursor += match_length
                        continue

                # record position and advance
                seen[chunk] = cursor
                cursor += 1

            if window_size > 0:
                match_coverage = total_match_bytes / window_size
                overhead = 3
                lz77_gain = total_match_bytes - (match_count * overhead)

                
            #Huffman metrics
            entropy = 0
            symbol_map = {}

            for i in range(start, end, 1):
                symbol = data[i]
                if symbol not in symbol_map:
                    symbol_map[symbol] = 1
                else:
                    symbol_map[symbol] += 1

            alphabet = len(symbol_map)

            for symbol in symbol_map:
                probability = symbol_map[symbol] / window_size
                entropy += -probability * log2(probability)

            estimated_bits = entropy * window_size
            estimated_bytes = estimated_bits / 8
            header_bytes = 1 + (alphabet * 2) + 4
            huffman_gain = window_size - (estimated_bytes + header_bytes)

            # output stats
            results[window_count] = {
                    'RLE': {'run_count': run_count, 'avg_run': avg_run, 'run_freq': run_freq, 'run_coverage': run_coverage, 'rle_gain': rle_gain}, #RLE Metrics
                    'LZ77': {'match_count': match_count, 'max_match_length': max_match_length, 'match_coverage': match_coverage, 'lz77_gain': lz77_gain},
                    'Huffman': {'entropy': entropy, 'alphabet': alphabet, 'estimated_bytes': estimated_bytes, 'huffman_gain': huffman_gain} #Huffman metrics
            }
        return results


    def process(self, results):

        window_count = len(results)

        # ---- Aggregate RLE ----
        total_rle_gain = 0
        total_run_coverage = 0

        # ---- Aggregate LZ77 ----
        total_lz77_gain = 0
        total_match_coverage = 0

        # ---- Aggregate Huffman ----
        total_huffman_gain = 0
        total_entropy = 0

        for key in results:

            # RLE
            total_rle_gain += results[key]['RLE']['rle_gain']
            total_run_coverage += results[key]['RLE']['run_coverage']

            # LZ77
            total_lz77_gain += results[key]['LZ77']['lz77_gain']
            total_match_coverage += results[key]['LZ77']['match_coverage']

            # Huffman
            total_huffman_gain += results[key]['Huffman']['huffman_gain']
            total_entropy += results[key]['Huffman']['entropy']

        # Averages
        avg_rle_gain = total_rle_gain / window_count
        avg_run_coverage = total_run_coverage / window_count

        avg_lz77_gain = total_lz77_gain / window_count
        avg_match_coverage = total_match_coverage / window_count

        avg_huffman_gain = total_huffman_gain / window_count
        avg_entropy = total_entropy / window_count

        # ---- Decision Logic ----

        # RLE Decision
        if avg_rle_gain > 0 and avg_run_coverage > 0.05:
            self.use_RLE = True

        # LZ77 Decision
        if avg_lz77_gain > 0 and avg_match_coverage > 0.05:
            self.use_LZ77 = True

        # Huffman Decision
        if avg_huffman_gain > 0 and avg_entropy < 7.8:
            self.use_HUFFMAN = True

        # ---- Build Sequence ----
        sequence = []

        if self.use_RLE:
            sequence.append("RLE")

        if self.use_LZ77:
            sequence.append("LZ77")

        if self.use_HUFFMAN:
            sequence.append("HUFFMAN")

        return sequence

