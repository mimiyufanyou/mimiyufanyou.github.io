"""Interactive charts for the multilayer post, from analysis/results/multilayer.json.

    python analysis/multilayer_charts.py   # writes public/charts/ml_*.html
"""

import json
from pathlib import Path

import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from plotly.subplots import make_subplots

ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "analysis" / "results" / "multilayer.json").read_text())
OUT = ROOT / "public" / "charts"

FONT = dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif', size=12, color="#333")
DEFECT, COOP = "#440154", "#fde725"  # the two ends of viridis, as in part 1's banner


def viridis(n, lo=0.0, hi=0.9):
    return sample_colorscale("Viridis", [lo + (hi - lo) * i / max(n - 1, 1) for i in range(n)])


def save(fig, name, title, height=500):
    fig.update_layout(
        template="plotly_white", font=FONT, height=height,
        title=dict(text=title, x=0, xanchor="left", y=0.985, yanchor="top", yref="container", font=dict(size=14)),
        margin=dict(l=50, r=15, t=60, b=50), legend=dict(font=dict(size=10)), hoverlabel=dict(font=FONT),
    )
    fig.write_html(OUT / name, include_plotlyjs="cdn", full_html=True,
                   config={"displaylogo": False, "responsive": True},
                   default_width="100%", default_height=f"{height}px")
    print("wrote", name)


def lattice_animation():
    s = DATA["snapshots"]
    times = s["times"]
    scale = [[0, DEFECT], [0.5, DEFECT], [0.5, COOP], [1, COOP]]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.04, subplot_titles=(
        f"One layer, b = {s['single']['b']}",
        f"Two coupled layers, b = {s['interdependent']['b']}, α = {s['interdependent']['alpha']}"))

    def hm(z, col):
        return go.Heatmap(z=z, colorscale=scale, zmin=0, zmax=1, showscale=False, hoverinfo="skip", xaxis=f"x{col}" if col > 1 else "x", yaxis=f"y{col}" if col > 1 else "y")

    fig.add_trace(hm(s["single"]["frames"][0], 1), row=1, col=1)
    fig.add_trace(hm(s["interdependent"]["frames"][0], 2), row=1, col=2)
    fig.frames = [go.Frame(name=str(t), data=[hm(s["single"]["frames"][k], 1), hm(s["interdependent"]["frames"][k], 2)], traces=[0, 1])
                  for k, t in enumerate(times)]
    for ax in ["xaxis", "xaxis2", "yaxis", "yaxis2"]:
        fig.layout[ax].update(showticklabels=False, showgrid=False, zeroline=False, constrain="domain")
    fig.layout.yaxis.update(scaleanchor="x")
    fig.layout.yaxis2.update(scaleanchor="x2")
    fig.update_annotations(font=dict(size=11))
    fig.update_layout(
        sliders=[dict(active=0, x=0, len=1, y=0, yanchor="top", pad=dict(t=30),
                      currentvalue=dict(prefix="Monte Carlo step ", font=dict(size=11)),
                      steps=[dict(label=str(t), method="animate", args=[[str(t)], dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))]) for t in times])],
        updatemenus=[dict(type="buttons", x=1, xanchor="right", y=0, yanchor="top", pad=dict(t=30), showactive=False,
                          buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=600, redraw=True), fromcurrent=True, transition=dict(duration=0))])])],
        margin=dict(l=10, r=10, t=70, b=110),
    )
    save(fig, "ml_lattice.html", "Yellow cooperates, purple defects", height=430)


def over_time():
    s = DATA["snapshots"]
    fig = go.Figure()
    series = [
        (f"One layer, b = {s['single']['b']}", s["single"]["history"], "#7f7f7f", "solid"),
        (f"One layer, b = {s['single_same_b']['b']}", s["single_same_b"]["history"], "#7f7f7f", "dot"),
        (f"Two coupled layers, b = {s['interdependent']['b']}, α = {s['interdependent']['alpha']}", s["interdependent"]["history"], "#21918c", "solid"),
    ]
    for name, h, color, dash in series:
        fig.add_trace(go.Scatter(x=list(range(1, len(h) + 1)), y=h, name=name, mode="lines",
                                 line=dict(color=color, dash=dash, width=2),
                                 hovertemplate=f"{name}<br>step %{{x}}<br>%{{y:.0%}} cooperate<extra></extra>"))
    fig.update_xaxes(title="Monte Carlo step", type="log")
    fig.update_yaxes(title="Share cooperating", tickformat=".0%", range=[0, 1])
    fig.update_layout(legend=dict(orientation="h", y=-0.25))
    save(fig, "ml_over_time.html", "Cooperation over time", height=460)


def sweep(name, key, label, fmt, title, height=500):
    d = DATA[key]
    groups = d["alpha"] if key == "interdependent" else d["layers"]
    colors = viridis(len(groups))
    fig = go.Figure()
    for k, g in enumerate(groups):
        lab = fmt(g)
        fig.add_trace(go.Scatter(x=d["b"], y=d["cooperation"][k], name=lab, mode="lines+markers",
                                 line=dict(color=colors[k], width=2), marker=dict(size=5),
                                 hovertemplate=f"{lab}<br>b = %{{x:.2f}}<br>%{{y:.0%}} cooperate<extra></extra>"))
    fig.update_xaxes(title="Temptation to defect, b")
    fig.update_yaxes(title="Share cooperating", tickformat=".0%", range=[0, 1])
    fig.update_layout(legend=dict(title=dict(text=label)))
    save(fig, name, title, height)


def single():
    d = DATA["single"]
    fig = go.Figure(go.Scatter(x=d["b"], y=d["cooperation"], mode="lines+markers", line=dict(color="#21918c", width=2),
                               hovertemplate="b = %{x:.2f}<br>%{y:.0%} cooperate<extra></extra>"))
    fig.update_xaxes(title="Temptation to defect, b")
    fig.update_yaxes(title="Share cooperating", tickformat=".0%", range=[0, 1])
    save(fig, "ml_single.html", "One layer: cooperation against temptation", height=400)


if __name__ == "__main__":
    lattice_animation()
    over_time()
    single()
    sweep("ml_interdependent.html", "interdependent", "Coupling α", lambda a: f"α = {a}", "Two coupled layers")
    sweep("ml_multiplex.html", "multiplex", "Layers", lambda m: f"{m} layer" + ("s" if m > 1 else ""), "The same players on several layers")
