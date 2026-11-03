import pandas as pd

STEPS = ["view_item", "contact", "deal"]


def load_events(path):
    return pd.read_csv(path, parse_dates=["ts"])


def user_flags(events):
    # одна строка на юзера: дошёл ли до шага + его variant/platform
    flags = (
        events.assign(ok=1)
        .pivot_table(index="user_id", columns="event", values="ok", aggfunc="max", fill_value=0)
        .reindex(columns=STEPS, fill_value=0)
        .astype(bool)
    )
    info = events.groupby("user_id").agg(
        variant=("variant", "first"),
        platform=("platform", "first"),
        category=("category", "first"),
    )
    return info.join(flags)


def funnel_table(users, by=None):
    def stats(g):
        v = g["view_item"].sum()
        c = g["contact"].sum()
        d = g["deal"].sum()
        return pd.Series({
            "users_view": v,
            "users_contact": c,
            "users_deal": d,
            "cr_view_contact": c / v if v else 0,
            "cr_contact_deal": d / c if c else 0,
            "cr_view_deal": d / v if v else 0,
        })

    if by is None:
        return stats(users).to_frame().T

    out = []
    for key, g in users.groupby(by):
        row = {by: key}
        row.update(stats(g).to_dict())
        out.append(row)
    return pd.DataFrame(out)
