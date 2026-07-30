"""
Evolución de salarios reales en Mendoza, 1895-1986
Fuentes: Salarios varones y mujeres 1895-1986 (Olguín, JHE 2025) · Salario industrial, base Ferreres.
"""

import json
import plotly.graph_objects as go

with open("raw_data.json", encoding="utf-8") as f:
    RAW_DATA = json.load(f)

YEARS = sorted(int(y) for y in RAW_DATA.keys())

SERIES = {
    "pb": {"name": "Peón de bodega / Obrero vinícola", "color": "#C0392B", "axis": "y"},
    "pv": {"name": "Peón de viña", "color": "#27AE60", "axis": "y"},
    "al": {"name": "Albañil", "color": "#E67E22", "axis": "y"},
    "si": {"name": "Salario industrial (Ferreres)", "color": "#2980B9", "axis": "y2"},
}

# Etapas históricas: colores claros y distintos, solo de fondo (no deben tapar las series)
PERIODS = [
    {"from": 1893, "to": 1960, "color": "rgba(41, 128, 185, 0.07)", "label": "1890–1960"},
    {"from": 1960, "to": 1970, "color": "rgba(230, 126, 34, 0.12)", "label": "1960–1970"},
    {"from": 1970, "to": 1988, "color": "rgba(142, 68, 173, 0.09)", "label": "1970–1986"},
]


def build_frame_traces(up_to_year):
    years = [y for y in YEARS if y <= up_to_year]
    traces = []
    for key, meta in SERIES.items():
        x = years
        y = [RAW_DATA[str(y)][key] for y in years]
        traces.append(go.Scatter(
            x=x, y=y, mode="lines", name=meta["name"],
            line=dict(color=meta["color"], width=2.5),
            marker=dict(color=meta["color"], size=5),
            connectgaps=False, yaxis=meta["axis"],
            hovertemplate=f"<b>%{{x}}</b><br>{meta['name']}: %{{y:.1f}}<extra></extra>",
        ))
    return traces


def period_shapes():
    return [
        dict(type="rect", xref="x", yref="paper",
             x0=p["from"], x1=p["to"], y0=0, y1=1,
             fillcolor=p["color"], line_width=0, layer="below")
        for p in PERIODS
    ]


def period_annotations():
    # Etiquetas chicas y discretas en la parte superior de cada franja
    return [
        dict(x=(p["from"] + p["to"]) / 2, y=1.045, xref="x", yref="paper",
             text=p["label"], showarrow=False,
             font=dict(size=10, color="#888"))
        for p in PERIODS
    ]


frames = [
    go.Frame(data=build_frame_traces(year), name=str(year))
    for year in YEARS
]

fig = go.Figure(
    data=build_frame_traces(YEARS[0]),
    frames=frames,
)

fig.update_layout(
    title=dict(text="Evolución de salarios reales en Mendoza, 1895–1986", font=dict(family="Georgia, serif", size=20)),
    template="plotly_white",
    shapes=period_shapes(),
    annotations=period_annotations(),
    xaxis=dict(title="Año", range=[1893, 1988], dtick=10),
    yaxis=dict(title=dict(text="$ ley 18188 (1960)", font=dict(color="#C0392B")), range=[0, 120]),
    yaxis2=dict(title=dict(text="$ de 2004 (Ferreres)", font=dict(color="#2980B9")), range=[0, 2400], overlaying="y", side="right"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
    height=560,
    margin=dict(t=90, b=90),
    updatemenus=[dict(
        type="buttons", showactive=False, y=1.12, x=0.0, xanchor="left",
        buttons=[
            dict(label="▶ Reproducir", method="animate",
                 args=[None, dict(frame=dict(duration=90, redraw=True), fromcurrent=True, transition=dict(duration=0))]),
            dict(label="⏸ Pausar", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
        ],
    )],
    sliders=[dict(
        active=0,
        steps=[dict(method="animate", label=str(y),
                     args=[[str(y)], dict(mode="immediate", frame=dict(duration=0, redraw=True))])
               for y in YEARS],
        currentvalue=dict(prefix="Año: "),
    )],
)

fig.add_annotation(
    text="Fuentes: Salarios varones y mujeres 1895–1986 (Olguín, JHE 2025) · Salario industrial, base Ferreres.",
    xref="paper", yref="paper", x=0.5, y=-0.42, showarrow=False,
    font=dict(size=10, color="#aaa"),
)

fig.write_html("salarios_evolucion_completo_python.html", auto_play=False)
fig.show()
