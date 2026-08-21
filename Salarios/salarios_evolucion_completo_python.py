"""
Evolución de salarios reales en Mendoza, 1895-1986 (índice base 1970=1)
Fuentes: Salarios en Mendoza (Olguín, JHE 2025) - Salario industrial en Capital Federal (Ferreres, 2010).
Datos: hoja "Evolución del salario obrero vi" del Excel original, columnas "Real" (índice 1970=100).
"""

import plotly.graph_objects as go

RAW_DATA = {"1914":{"pb":None,"pv":63,"al":69,"si":41},"1915":{"pb":50,"pv":42,"al":64,"si":37},"1916":{"pb":47,"pv":39,"al":59,"si":35},"1923":{"pb":None,"pv":None,"al":50,"si":52},"1928":{"pb":96,"pv":None,"al":54,"si":59},"1929":{"pb":96,"pv":None,"al":54,"si":59},"1930":{"pb":96,"pv":None,"al":54,"si":59},"1931":{"pb":96,"pv":None,"al":54,"si":59},"1932":{"pb":119,"pv":None,"al":None,"si":63},"1933":{"pb":100,"pv":None,"al":53,"si":58},"1945":{"pb":None,"pv":None,"al":50,"si":66},"1952":{"pb":172,"pv":114,"al":116,"si":79},"1953":{"pb":135,"pv":90,"al":91,"si":83},"1954":{"pb":155,"pv":110,"al":101,"si":91},"1955":{"pb":138,"pv":98,"al":90,"si":88},"1956":{"pb":167,"pv":118,"al":123,"si":96},"1957":{"pb":134,"pv":95,"al":99,"si":93},"1958":{"pb":217,"pv":170,"al":166,"si":100},"1959":{"pb":129,"pv":115,"al":78,"si":74},"1960":{"pb":120,"pv":99,"al":83,"si":76},"1961":{"pb":126,"pv":87,"al":92,"si":84},"1962":{"pb":127,"pv":87,"al":110,"si":82},"1963":{"pb":125,"pv":77,"al":97,"si":84},"1964":{"pb":116,"pv":86,"al":103,"si":93},"1965":{"pb":128,"pv":107,"al":109,"si":101},"1966":{"pb":127,"pv":115,"al":110,"si":102},"1967":{"pb":122,"pv":111,"al":114,"si":102},"1968":{"pb":105,"pv":96,"al":98,"si":94},"1969":{"pb":109,"pv":112,"al":102,"si":97},"1970":{"pb":100,"pv":100,"al":100,"si":100},"1971":{"pb":112,"pv":136,"al":97,"si":104},"1972":{"pb":99,"pv":124,"al":91,"si":97},"1973":{"pb":81,"pv":162,"al":98,"si":104},"1974":{"pb":80,"pv":153,"al":94,"si":115},"1975":{"pb":104,"pv":77,"al":81,"si":111},"1976":{"pb":78,"pv":65,"al":46,"si":73},"1977":{"pb":54,"pv":48,"al":34,"si":69},"1978":{"pb":39,"pv":38,"al":27,"si":68},"1979":{"pb":36,"pv":27,"al":29,"si":79},"1980":{"pb":43,"pv":42,"al":30,"si":88},"1981":{"pb":42,"pv":43,"al":29,"si":79},"1982":{"pb":45,"pv":54,"al":32,"si":70},"1983":{"pb":72,"pv":75,"al":51,"si":91},"1984":{"pb":86,"pv":85,"al":63,"si":111},"1985":{"pb":74,"pv":72,"al":38,"si":90},"1986":{"pb":74,"pv":63,"al":37,"si":95}}

YEARS = sorted(
    int(y) for y, v in RAW_DATA.items()
    if any(v[k] is not None for k in ("pb", "pv", "al", "si"))
)

SERIES = {
    "pb": {"name": "Obrero vinícola", "color": "#C0392B"},
    "pv": {"name": "Peón de viña", "color": "#27AE60"},
    "al": {"name": "Albañil", "color": "#E67E22"},
    "si": {"name": "Salario industrial en Capital Federal", "color": "#2980B9"},
}

PERIODS = [
    {"from": 1914, "to": 1960, "color": "rgba(41, 128, 185, 0.07)", "label": "1914–1960"},
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
            connectgaps=False,
            hovertemplate=f"<b>%{{x}}</b><br>{meta['name']}: %{{y:.0f}}<extra></extra>",
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
    title=dict(text="Evolución de salarios reales en Mendoza, 1914–1986", font=dict(family="Georgia, serif", size=20)),
    template="plotly_white",
    shapes=period_shapes(),
    annotations=period_annotations(),
    xaxis=dict(title="Año", range=[1913, 1988], dtick=10),
    yaxis=dict(
        range=[0, 230],
        tickmode="array",
        tickvals=[0, 50, 100, 150, 200],
        ticktext=["0", "50", "100", "150", "200"],
        tickfont=dict(color="#999", size=10),
        showgrid=False,
        zeroline=False,
        title=dict(text="$ de 1970", font=dict(color="#C0392B", size=13, family="Arial Black, Arial")),
    ),
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
    text="Fuentes: Salarios en Mendoza (Olguín, JHE 2025) - Salario industrial en Capital Federal (Ferreres, 2010)",
    xref="paper", yref="paper", x=0.5, y=-0.42, showarrow=False,
    font=dict(size=10, color="#aaa"),
)

fig.write_html("salarios_evolucion_completo_python.html", auto_play=False)
fig.show()
