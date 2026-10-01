"""月間ファン獲得数の集計。使い方: python3 tally.py 基準.csv 月末.csv [月]"""
import csv
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        return {r["name"]: int(r["total_fans"]) for r in csv.DictReader(f)}


def fmt(n):
    """9月分の投稿に合わせた表記：1億以上は小数1桁の億、未満は万。"""
    if n >= 100_000_000:
        oku = round(n / 100_000_000, 1)
        return f"{int(oku)}億" if oku == int(oku) else f"{oku}億".replace(".", "．")
    return f"{round(n / 10_000):,}万".replace(",", "")


def main():
    base, cur = load(sys.argv[1]), load(sys.argv[2])
    month = sys.argv[3] if len(sys.argv) > 3 else "◯"
    gains = sorted(((cur[n] - base[n], n) for n in cur if n in base), reverse=True)

    print("=== 獲得数一覧 ===")
    for i, (g, n) in enumerate(gains, 1):
        print(f"{i:>2} {n}\t{g:>13,}")
    for n in cur.keys() - base.keys():
        print(f"※基準値なし（新規加入）: {n}")
    for n in base.keys() - cur.keys():
        print(f"※月末に不在（脱退）: {n}")

    print("\n=== 2500万以下 ===")
    for g, n in gains:
        if g <= 25_000_000:
            print(f"{n}\t{g:,}")

    print("\n=== 投稿文 ===")
    print(f"☆{month}月ファン獲得数サークル内ランキング☆\n")
    print("上位15名まで発表します。いつもランキング維持に大きく貢献して下さり、本当にありがとうございます！\n")
    top = gains[:15]
    for i in range(0, len(top), 3):
        print("".join(f"●{j + 1}位：{n}さん@{fmt(g)}" for j, (g, n) in enumerate(top[i:i + 3], i)) + "\n")
    print("☆以上TOP15名でした☆")


main()
