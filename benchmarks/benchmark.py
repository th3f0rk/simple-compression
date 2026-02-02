import time
import random
import string
from simple_compression import SimpleCompression

SIZE = 500_000
SEED = 1337

random.seed(SEED)


def mb_per_sec(bytes_count, seconds):
    return (bytes_count / (1024 * 1024)) / seconds if seconds > 0 else 0.0


def run_case(name, data, compressor):
    print(f"\n--- {name} ---")

    modes = {
        "RLE only": dict(sequence=["RLE"]),
        "LZ77 only": dict(sequence=["LZ77"]),
        "RLE → LZ77": dict(sequence=["RLE", "LZ77"]),
        "AUTO": dict(auto=True),
    }

    for label, kwargs in modes.items():
        start = time.perf_counter()
        encoded = compressor.encode(data, **kwargs)
        enc_time = time.perf_counter() - start

        start = time.perf_counter()
        decoded = compressor.decode(encoded)
        dec_time = time.perf_counter() - start

        assert decoded == data

        ratio = len(encoded) / len(data)

        print(label)
        print(f"  input bytes : {len(data)}")
        print(f"  output bytes: {len(encoded)}")
        print(f"  ratio       : {ratio:.4f}")
        print(f"  encode time : {enc_time:.6f} s")
        print(f"  decode time : {dec_time:.6f} s")
        print(f"  enc MB/s    : {mb_per_sec(len(data), enc_time):.2f}")
        print(f"  dec MB/s    : {mb_per_sec(len(data), dec_time):.2f}")
        print()

#data generators
def gen_run_heavy():
    chunk = b"A" * 4096 + b"\n" + b" " * 2048 + b"\n"
    return bytearray(chunk * (SIZE // len(chunk)))


def gen_structured():
    row = "id=12345,status=OK,type=EVENT,timestamp=1700000000\n"
    text = row * (SIZE // len(row))
    return bytearray(text.encode())


def gen_mixed_realistic():
    blocks = []
    for _ in range(SIZE // 256):
        choice = random.random()
        if choice < 0.4:
            blocks.append("INFO 2024-01-01T12:00:00Z service=auth result=success\n")
        elif choice < 0.7:
            blocks.append("000000000000000000000000000000000000\n")
        else:
            blocks.append(
                "".join(random.choices(string.ascii_letters + string.digits, k=64)) + "\n"
            )
    return bytearray("".join(blocks).encode())


def gen_biased_binary():
    data = bytearray()
    for _ in range(SIZE):
        if random.random() < 0.85:
            data.append(random.choice([0x00, 0xFF, 0x20, 0x0A]))
        else:
            data.append(random.randint(0, 255))
    return data


def gen_random():
    return bytearray(random.getrandbits(8) for _ in range(SIZE))


if __name__ == "__main__":
    c = SimpleCompression()

    print(f"\n==============================")
    print(f"REALISTIC BENCHMARK (~500 KiB)")
    print(f"==============================")

    run_case("Run-heavy", gen_run_heavy(), c)
    run_case("Structured", gen_structured(), c)
    run_case("Mixed real-world", gen_mixed_realistic(), c)
    run_case("Biased binary", gen_biased_binary(), c)
    run_case("Pure random (control)", gen_random(), c)

