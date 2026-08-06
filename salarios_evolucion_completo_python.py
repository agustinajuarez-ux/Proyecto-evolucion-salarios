"""
Evolución de salarios reales en Mendoza, 1895-1986 (índice base 1970=1)
Fuentes: Salarios en Mendoza (Olguín, JHE 2025) - Salario industrial en Capital Federal (Ferreres, 2010).
Datos: hoja "Evolución del salario obrero vi" del Excel original, columnas "Real" (índice 1970=100),
normalizadas dividiendo por 100 (1970 = 1).
"""

import plotly.graph_objects as go

RAW_DATA = {"1895":{"pb":None,"pv":None,"al":None,"si":None},"1896":{"pb":None,"pv":None,"al":None,"si":None},"1897":{"pb":None,"pv":None,"al":None,"si":None},"1898":{"pb":None,"pv":None,"al":None,"si":None},"1899":{"pb":None,"pv":None,"al":None,"si":None},"1900":{"pb":None,"pv":None,"al":None,"si":None},"1901":{"pb":None,"pv":None,"al":None,"si":None},"1902":{"pb":None,"pv":None,"al":None,"si":None},"1903":{"pb":None,"pv":None,"al":None,"si":None},"1904":{"pb":None,"pv":None,"al":None,"si":None},"1905":{"pb":None,"pv":None,"al":None,"si":None},"1906":{"pb":None,"pv":None,"al":None,"si":None},"1907":{"pb":None,"pv":None,"al":None,"si":None},"1908":{"pb":None,"pv":None,"al":None,"si":None},"1909":{"pb":None,"pv":None,"al":None,"si":None},"1910":{"pb":None,"pv":None,"al":None,"si":None},"1911":{"pb":None,"pv":None,"al":None,"si":None},"1912":{"pb":None,"pv":None,"al":None,"si":None},"1913":{"pb":None,"pv":None,"al":None,"si":None},"1914":{"pb":None,"pv":0.63,"al":0.69,"si":0.41},"1915":{"pb":0.5,"pv":0.42,"al":0.64,"si":0.37},"1916":{"pb":0.47,"pv":0.39,"al":0.59,"si":0.35},"1917":{"pb":None,"pv":None,"al":None,"si":None},"1918":{"pb":None,"pv":None,"al":None,"si":None},"1919":{"pb":None,"pv":None,"al":None,"si":None},"1920":{"pb":None,"pv":None,"al":None,"si":None},"1921":{"pb":None,"pv":None,"al":None,"si":None},"1922":{"pb":None,"pv":None,"al":None,"si":None},"1923":{"pb":None,"pv":None,"al":0.5,"si":0.52},"1924":{"pb":None,"pv":None,"al":None,"si":None},"1925":{"pb":None,"pv":None,"al":None,"si":None},"1926":{"pb":None,"pv":None,"al":None,"si":None},"1927":{"pb":None,"pv":None,"al":None,"si":None},"1928":{"pb":0.96,"pv":None,"al":0.54,"si":0.59},"1929":{"pb":0.96,"pv":None,"al":0.54,"si":0.59},"1930":{"pb":0.96,"pv":None,"al":0.54,"si":0.59},"1931":{"pb":0.96,"pv":None,"al":0.54,"si":0.59},"1932":{"pb":1.19,"pv":None,"al":None,"si":0.63},"1933":{"pb":1.0,"pv":None,"al":0.53,"si":0.58},"1934":{"pb":None,"pv":None,"al":None,"si":None},"1935":{"pb":None,"pv":None,"al":None,"si":None},"1936":{"pb":None,"pv":None,"al":None,"si":None},"1937":{"pb":None,"pv":None,"al":None,"si":None},"1938":{"pb":None,"pv":None,"al":None,"si":None},"1939":{"pb":None,"pv":None,"al":None,"si":None},"1940":{"pb":None,"pv":None,"al":None,"si":None},"1941":{"pb":None,"pv":None,"al":None,"si":None},"1942":{"pb":None,"pv":None,"al":None,"si":None},"1943":{"pb":None,"pv":None,"al":None,"si":None},"1944":{"pb":None,"pv":None,"al":None,"si":None},"1945":{"pb":None,"pv":None,"al":0.5,"si":0.66},"1946":{"pb":None,"pv":None,"al":None,"si":None},"1947":{"pb":None,"pv":None,"al":None,"si":None},"1948":{"pb":None,"pv":None,"al":None,"si":None},"1949":{"pb":None,"pv":None,"al":None,"si":None},"1950":{"pb":None,"pv":None,"al":None,"si":None},"1951":{"pb":None,"pv":None,"al":None,"si":None},"1952":{"pb":1.72,"pv":1.14,"al":1.16,"si":0.79},"1953":{"pb":1.35,"pv":0.9,"al":0.91,"si":0.83},"1954":{"pb":1.55,"pv":1.1,"al":1.01,"si":0.91},"1955":{"pb":1.38,"pv":0.98,"al":0.9,"si":0.88},"1956":{"pb":1.67,"pv":1.18,"al":1.23,"si":0.96},"1957":{"pb":1.34,"pv":0.95,"al":0.99,"si":0.93},"1958":{"pb":2.17,"pv":1.7,"al":1.66,"si":1.0},"1959":{"pb":1.29,"pv":1.15,"al":0.78,"si":0.74},"1960":{"pb":1.2,"pv":0.99,"al":0.83,"si":0.76},"1961":{"pb":1.26,"pv":0.87,"al":0.92,"si":0.84},"1962":{"pb":1.27,"pv":0.87,"al":1.1,"si":0.82},"1963":{"pb":1.25,"pv":0.77,"al":0.97,"si":0.84},"1964":{"pb":1.16,"pv":0.86,"al":1.03,"si":0.93},"1965":{"pb":1.28,"pv":1.07,"al":1.09,"si":1.01},"1966":{"pb":1.27,"pv":1.15,"al":1.1,"si":1.02},"1967":{"pb":1.22,"pv":1.11,"al":1.14,"si":1.02},"1968":{"pb":1.05,"pv":0.96,"al":0.98,"si":0.94},"1969":{"pb":1.09,"pv":1.12,"al":1.02,"si":0.97},"1970":{"pb":1.0,"pv":1.0,"al":1.0,"si":1.0},"1971":{"pb":1.12,"pv":1.36,"al":0.97,"si":1.04},"1972":{"pb":0.99,"pv":1.24,"al":0.91,"si":0.97},"1973":{"pb":0.81,"pv":1.62,"al":0.98,"si":1.04},"1974":{"pb":0.8,"pv":1.53,"al":0.94,"si":1.15},"1975":{"pb":1.04,"pv":0.77,"al":0.81,"si":1.11},"1976":{"pb":0.78,"pv":0.65,"al":0.46,"si":0.73},"1977":{"pb":0.54,"pv":0.48,"al":0.34,"si":0.69},"1978":{"pb":0.39,"pv":0.38,"al":0.27,"si":0.68},"1979":{"pb":0.36,"pv":0.27,"al":0.29,"si":0.79},"1980":{"pb":0.43,"pv":0.42,"al":0.3,"si":0.88},"1981":{"pb":0.42,"pv":0.43,"al":0.29,"si":0.79},"1982":{"pb":0.45,"pv":0.54,"al":0.32,"si":0.7},"1983":{"pb":0.72,"pv":0.75,"al":0.51,"si":0.91},"1984":{"pb":0.86,"pv":0.85,"al":0.63,"si":1.11},"1985":{"pb":0.74,"pv":0.72,"al":0.38,"si":0.9},"1986":{"pb":0.74,"pv":0.63,"al":0.37,"si":0.95}}

YEARS = sorted(int(y) for y in RAW_DATA.keys())

SERIES = {
    "pb": {"name": "Obrero vinícola", "color": "#C0392B"},
    "pv": {"name": "Peón de viña", "color": "#27AE60"},
    "al": {"name": "Albañil", "color": "#E67E22"},
    "si": {"name": "Salario industrial en Capital Federal", "color": "#2980B9"},
}

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
            connectgaps=False,
            hovertemplate=f"<b>%{{x}}</b><br>{meta['name']}: %{{y:.2f}}<extra></extra>",
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
    title=dict(text="Evolución de salarios reales en Mendoza, 1895–1986", font=dict(family="Georgia, serif", size=20)),
    template="plotly_white",
    shapes=period_shapes(),
    annotations=period_annotations(),
    xaxis=dict(title="Año", range=[1893, 1988], dtick=10),
    yaxis=dict(
        range=[0, 2.3],
        tickmode="array",
        tickvals=[1],
        ticktext=["$1970"],
        tickfont=dict(color="black", size=12),
        showgrid=False,
        zeroline=False,
        title=None,
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
