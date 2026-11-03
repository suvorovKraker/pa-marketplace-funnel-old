import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # без всплывающих окон — только сохранение в файл
import matplotlib.pyplot as plt
import pandas as pd

from src.ab_test import ab_contact
from src.funnel import funnel_table, load_events, user_flags
from src.generate_data import DATA_PATH, save_events

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def main():
    if not DATA_PATH.exists():
        save_events()

    events = load_events(DATA_PATH)
    users = user_flags(events)

    overall = funnel_table(users)
    by_platform = funnel_table(users, by="platform")
    ab = ab_contact(users)

    REPORTS.mkdir(exist_ok=True)
    overall.to_csv(REPORTS / "funnel_overall.csv", index=False)
    by_platform.to_csv(REPORTS / "funnel_by_platform.csv", index=False)
    pd.DataFrame([ab["A"], ab["B"]]).to_csv(REPORTS / "ab_table.csv", index=False)

    funnel_png = REPORTS / "funnel.png"
    ab_png = REPORTS / "ab_conversion.png"

    fig, ax = plt.subplots()
    ax.bar(
        ["view", "contact", "deal"],
        [
            overall.iloc[0]["users_view"],
            overall.iloc[0]["users_contact"],
            overall.iloc[0]["users_deal"],
        ],
    )
    ax.set_title("funnel")
    fig.tight_layout()
    fig.savefig(funnel_png, dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots()
    ax.bar([ab["A"]["variant"], ab["B"]["variant"]], [ab["A"]["cr"], ab["B"]["cr"]])
    ax.set_title("contact CR by variant")
    fig.tight_layout()
    fig.savefig(ab_png, dpi=120)
    plt.close(fig)

    print("=== воронка ===")
    print(overall.to_string(index=False))
    print()
    print("=== по платформам ===")
    print(by_platform.to_string(index=False))
    print()
    print("=== A/B (contact / view) ===")
    print(
        f"A={ab['A']['cr']:.3f}, B={ab['B']['cr']:.3f}, "
        f"lift B-A={ab['lift_B']:.4f}, p={ab['p_value']:.4f}"
    )
    print()
    print("картинки сохранены сюда (не всплывающее окно):")
    print(funnel_png)
    print(ab_png)

    # открыть файлы в Preview — они не исчезнут
    subprocess.run(["open", str(funnel_png), str(ab_png)], check=False)


if __name__ == "__main__":
    main()
