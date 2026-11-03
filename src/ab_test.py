import math

from scipy import stats


def ab_contact(users, alpha=0.05):
    # конверсия contact / view по вариантам, двусторонний z-test
    rows = []
    for var, g in users.groupby("variant"):
        n = int(g["view_item"].sum())
        s = int(g["contact"].sum())
        rows.append({"variant": var, "n": n, "contacts": s, "cr": s / n if n else 0})

    a = next(r for r in rows if r["variant"] == "A")
    b = next(r for r in rows if r["variant"] == "B")

    p1, p2 = a["cr"], b["cr"]
    p = (a["contacts"] + b["contacts"]) / (a["n"] + b["n"])
    se = math.sqrt(p * (1 - p) * (1 / a["n"] + 1 / b["n"]))
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        "A": a,
        "B": b,
        "lift_B": p2 - p1,
        "z": z,
        "p_value": p_value,
        "significant": p_value < alpha,
    }
