"""Interactive charts for part 2, from analysis/results/ipd_part2.json.

Writes public/charts/ipd2_*.html. Each chart sits in the post's 550px column,
so they are drawn narrow and resize with the frame. Plotly is loaded from its CDN
to keep each file small (part 1's charts carried all of Plotly inside each file).

    python analysis/ipd_part2_charts.py
"""

import json
from pathlib import Path

import plotly.graph_objects as go
from plotly.colors import sample_colorscale

ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "analysis" / "results" / "ipd_part2.json").read_text())
OUT = ROOT / "public" / "charts"

FONT = dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif', size=12, color="#333")
ZD_NAMES = {"ZD-Extort-2", "ZD-Extort-4", "ZD-GTFT-2", "ZD-SET-2", "GTFT"}


def short(name):
    """Display name: drop the library's parameters ("GTFT: 0.33" -> "Generous TFT")."""
    base = name.split(":")[0].replace("First by ", "").replace(" and ", " & ")
    return {"GTFT": "Generous TFT"}.get(base, base)


def is_new(name):
    return name.split(":")[0] in ZD_NAMES


def viridis(n):
    return sample_colorscale("Viridis", [i / max(n - 1, 1) for i in range(n)])


def save(fig, name, title, height=520):
    fig.update_layout(
        template="plotly_white",
        font=FONT,
        title=dict(text=title, x=0, xanchor="left", y=0.985, yanchor="top", yref="container", font=dict(size=14)),
        height=height,
        margin=dict(l=50, r=15, t=60, b=50),
        legend=dict(font=dict(size=10)),
        hoverlabel=dict(font=FONT),
    )
    fig.write_html(
        OUT / name,
        include_plotlyjs="cdn",
        full_html=True,
        config={"displaylogo": False, "responsive": True},
        default_width="100%",
        default_height=f"{height}px",
    )
    print("wrote", name)


def noise_chart():
    runs = DATA["noise"]
    players = runs[0]["players"]
    # Order lines by how they finished without noise, best first.
    order = [players.index(p) for p in runs[0]["ranking"]]
    colors = viridis(len(order))
    fig = go.Figure()
    for rank, i in enumerate(order):
        name = players[i]
        tft = name == "Tit For Tat"
        fig.add_trace(go.Scatter(
            x=[r["noise"] for r in runs],
            y=[r["median_score"][i] for r in runs],
            mode="lines+markers",
            name=short(name),
            line=dict(color="#f14e32" if tft else colors[rank], width=4 if tft else 1.5),
            marker=dict(size=7 if tft else 4),
            hovertemplate=f"<b>{short(name)}</b><br>noise %{{x:.0%}}<br>median score %{{y:.2f}} per turn<extra></extra>",
        ))
    fig.update_xaxes(title="Chance each move is flipped (noise)", tickformat=".0%")
    fig.update_yaxes(title="Median score per turn")
    save(fig, "ipd2_noise.html", "The first tournament, replayed with noise")


def forgiveness_chart():
    f = DATA["forgiveness"]
    colors = viridis(len(f["noise"]))
    fig = go.Figure()
    for which, grid, visible in [("self", f["self_play"], True), ("field", f["vs_field"], False)]:
        for k, noise in enumerate(f["noise"]):
            fig.add_trace(go.Scatter(
                x=f["generosity"], y=grid[k], mode="lines+markers",
                name=f"noise {noise:.0%}", legendgroup=which, visible=visible,
                line=dict(color=colors[k], width=2), marker=dict(size=5),
                hovertemplate=f"noise {noise:.0%}<br>forgives %{{x:.0%}} of defections<br>%{{y:.2f}} per turn<extra></extra>",
            ))
    n = len(f["noise"])
    fig.add_vline(x=f["molander_optimum"], line=dict(color="#555", dash="dash", width=1),
                  annotation_text="Molander's ⅓", annotation_position="bottom right")
    fig.update_layout(updatemenus=[dict(
        type="buttons", direction="right", x=0, y=-0.2, xanchor="left", yanchor="top", pad=dict(t=0, b=0), font=dict(size=11),
        buttons=[
            dict(label="Against a copy of itself", method="update", args=[{"visible": [True] * n + [False] * n}]),
            dict(label="Against the first-tournament field", method="update", args=[{"visible": [False] * n + [True] * n}]),
        ],
    )], margin=dict(t=60, b=110))
    fig.update_xaxes(title="Generosity: chance of forgiving a defection", tickformat=".0%")
    fig.update_yaxes(title="Mean score per turn")
    save(fig, "ipd2_forgiveness.html", "How much should Tit For Tat forgive?", height=540)


def zd_chart():
    fig = go.Figure()
    runs = DATA["zd"]
    for k, run in enumerate(runs):
        is_zd = [is_new(p) for p in run["players"]]
        for group, color, symbol in [(False, "#7f7f7f", "circle"), (True, "#f14e32", "diamond")]:
            idx = [i for i, z in enumerate(is_zd) if z == group]
            fig.add_trace(go.Scatter(
                x=[run["wins_share"][i] for i in idx],
                y=[run["mean_score"][i] for i in idx],
                text=[short(run["players"][i]) for i in idx],
                mode="markers+text" if group else "markers",
                textposition="middle right", textfont=dict(size=10),
                marker=dict(color=color, size=11 if group else 8, symbol=symbol, line=dict(width=1, color="#fff")),
                name="ZD and generous entrants" if group else "First-tournament strategies",
                visible=(k == 0),
                hovertemplate="<b>%{text}</b><br>wins %{x:.0%} of matches<br>%{y:.2f} per turn<extra></extra>",
            ))
    fig.update_layout(updatemenus=[dict(
        type="buttons", direction="right", x=0, y=-0.2, xanchor="left", yanchor="top", pad=dict(t=0, b=0), font=dict(size=11),
        buttons=[
            dict(label="No noise", method="update", args=[{"visible": [True, True, False, False]}]),
            dict(label="5% noise", method="update", args=[{"visible": [False, False, True, True]}]),
        ],
    )], margin=dict(t=60, b=110), legend=dict(orientation="h", y=-0.36))
    fig.update_xaxes(title="Share of matches won outright", tickformat=".0%", range=[-0.05, 1.18])
    fig.update_yaxes(title="Mean score per turn")
    save(fig, "ipd2_zd.html", "Winning matches is not winning the tournament", height=600)


def evolution_chart():
    e = DATA["evolution"]
    hist = e["equal_start"]
    players = e["players"]
    final = hist[-1]
    order = sorted(range(len(players)), key=lambda i: final[i])
    colors = viridis(len(players))
    fig = go.Figure()
    for c, i in enumerate(order):
        fig.add_trace(go.Scatter(
            x=list(range(len(hist))), y=[g[i] for g in hist], name=short(players[i]),
            stackgroup="one", groupnorm="percent", mode="lines",
            line=dict(width=0.5, color=colors[c]),
            hovertemplate=f"<b>{short(players[i])}</b><br>generation %{{x}}<br>%{{y:.1f}}%<extra></extra>",
        ))
    fig.update_xaxes(title="Generation")
    fig.update_yaxes(title="Share of the population (%)", range=[0, 100])
    save(fig, "ipd2_evolution.html", "Evolution with ZD strategies and 5% noise", height=560)

    counts = e["largest_at_end"]
    idx = [i for i in sorted(range(len(players)), key=lambda i: counts[i]) if counts[i] > 0]
    fig = go.Figure(go.Bar(
        x=[counts[i] / e["random_starts"] for i in idx], y=[short(players[i]) for i in idx], orientation="h",
        marker=dict(color=["#f14e32" if is_new(players[i]) else "#7f7f7f" for i in idx]),
        hovertemplate="<b>%{y}</b><br>largest in %{x:.0%} of runs<extra></extra>",
    ))
    fig.update_xaxes(title=f"Share of {e['random_starts']} random starting populations", tickformat=".0%")
    save(fig, "ipd2_random_starts.html", "Who ends up largest, from random starts", height=max(260, 60 + 28 * len(idx)))


if __name__ == "__main__":
    noise_chart()
    forgiveness_chart()
    zd_chart()
    evolution_chart()
