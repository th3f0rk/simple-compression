import time
from pathlib import Path

from simple_compression.compression import SimpleCompression


CORPUS_DIR = Path("benchmarks/canterbury")

MODES = [
    ("RLE only", dict(sequence=["RLE"])),
    ("LZ77 only", dict(sequence=["LZ77"])),
    ("RLE → LZ77", dict(sequence=["RLE", "LZ77"])),
    ("AUTO", dict(auto=True)),
]


def mb_per_s(byte_count, seconds):
    if seconds == 0:
        return float("inf")
    return (byte_count / (1024 * 1024)) / seconds


def benchmark_file(path: Path):
    data = bytearray(path.read_bytes())
    size = len(data)

    print(f"\n=== {path.name} ({size} bytes) ===")

    for label, kwargs in MODES:
        compressor = SimpleCompression()

        # encode
        t0 = time.perf_counter()
        encoded = compressor.encode(data, **kwargs)
        t1 = time.perf_counter()

        # decode
        t2 = time.perf_counter()
        decoded = compressor.decode(encoded)
        t3 = time.perf_counter()

        assert decoded == data, f"Decode mismatch: {path.name} [{label}]"

        enc_time = t1 - t0
        dec_time = t3 - t2
        ratio = len(encoded) / size

        print(label)
        print(f"  input bytes : {size}")
        print(f"  output bytes: {len(encoded)}")
        print(f"  ratio       : {ratio:.4f}")
        print(f"  encode time : {enc_time:.6f} s")
        print(f"  decode time : {dec_time:.6f} s")
        print(f"  enc MB/s    : {mb_per_s(size, enc_time):.2f}")
        print(f"  dec MB/s    : {mb_per_s(size, dec_time):.2f}")
        print()


def main():
    if not CORPUS_DIR.exists():
        raise RuntimeError(f"Corpus directory not found: {CORPUS_DIR}")

    files = sorted(p for p in CORPUS_DIR.iterdir() if p.is_file())

    print("==============================")
    print("CANTERBURY CORPUS (SMALL)")
    print("==============================")

    for path in files:
        benchmark_file(path)


if __name__ == "__main__":
    main()

