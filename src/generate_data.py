from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "events.csv"
rng = np.random.default_rng(42)


def make_events(n_users=8000):
    # синтетика: view -> иногда contact -> иногда deal
    # у варианта B конверсия в контакт чуть выше
    rows = []
    start = pd.Timestamp("2026-09-01")

    for uid in range(1, n_users + 1):
        platform = rng.choice(["ios", "android", "web"], p=[0.35, 0.4, 0.25])
        variant = rng.choice(["A", "B"])
        category = rng.choice(
            ["auto", "realty", "electronics", "jobs"],
            p=[0.3, 0.25, 0.3, 0.15],
        )
        ts = start + pd.Timedelta(days=int(rng.integers(0, 45)), hours=int(rng.integers(0, 24)))

        rows.append([uid, "view_item", variant, platform, category, ts])

        p_contact = 0.18 if variant == "A" else 0.21
        if rng.random() < p_contact:
            ts2 = ts + pd.Timedelta(minutes=int(rng.integers(1, 120)))
            rows.append([uid, "contact", variant, platform, category, ts2])
            if rng.random() < 0.22:
                ts3 = ts2 + pd.Timedelta(hours=int(rng.integers(1, 72)))
                rows.append([uid, "deal", variant, platform, category, ts3])

    df = pd.DataFrame(rows, columns=["user_id", "event", "variant", "platform", "category", "ts"])
    return df.sort_values(["user_id", "ts"]).reset_index(drop=True)


def save_events(path=DATA_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    make_events().to_csv(path, index=False)
    return path


if __name__ == "__main__":
    save_events()
