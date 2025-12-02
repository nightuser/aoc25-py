import sys


def process_pair(lo_raw: str, hi_raw: str, parts: int) -> set[int]:
    if len(lo_raw) % parts == 0:
        k = len(lo_raw) // parts
    elif len(hi_raw) % parts == 0:
        k = len(hi_raw) // parts
    else:
        return set()

    if len(lo_raw) % parts != 0:
        lo_raw = "1" + "0" * (parts * k - 1)
    if len(hi_raw) % parts != 0:
        hi_raw = "9" * (parts * k)

    lo = int(lo_raw)
    hi = int(hi_raw)

    base = 10**k
    n = 1
    for _ in range(parts - 1):
        n = n * base + 1

    def build_id(prefix: int) -> int:
        return prefix * n

    start = int(lo_raw[:k])
    end = int(hi_raw[:k])
    bad_ids = set[int]()
    if start == end:
        candidate_id = build_id(start)
        if candidate_id in range(lo, hi + 1):
            bad_ids.add(candidate_id)
    else:
        start_id = build_id(start)
        if start_id >= lo:
            bad_ids.add(start_id)

        for bad_prefix in range(start + 1, end):
            bad_ids.add(build_id(bad_prefix))

        end_id = build_id(end)
        if end_id <= hi:
            bad_ids.add(end_id)
    return bad_ids


def main() -> None:
    fname = sys.argv[1]
    id_pairs = list[tuple[str, str]]()
    with open(fname) as fh:
        data = fh.read().rstrip()
        id_pairs_raw = data.split(",")
        for pair in id_pairs_raw:
            lo_raw, hi_raw = pair.split("-", 1)
            assert len(hi_raw) - len(lo_raw) <= 1
            id_pairs.append((lo_raw, hi_raw))

    ans1 = 0
    for lo_raw, hi_raw in id_pairs:
        ans1 += sum(process_pair(lo_raw, hi_raw, 2))

    ans2 = 0
    for lo_raw, hi_raw in id_pairs:
        total = set[int]()
        for parts in range(2, len(hi_raw) + 1):
            total.update(process_pair(lo_raw, hi_raw, parts))
        ans2 += sum(total)

    print(f"ans1 = {ans1}")
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
