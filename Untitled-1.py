"""
Evolución de salarios reales en Mendoza, 1895–1986
Fuentes:
  - Peón de bodega/Obrero vinícola: Salarios_varones_y_mujeres_1895-1986_DEFINITIVO.xlsx
  - Peón de viña:                   Salarios_varones_y_mujeres_1895-1986_DEFINITIVO.xlsx
  - Salario industrial (Cap. Fed.): Base de datos Ferreres (vía xlsx Salario ind, col. 11)
"""

import pandas as pd
import plotly.graph_objects as go

# ── 1. LEER DATOS ─────────────────────────────────────────────────────────────
XLSX = "Salarios_varones_y_mujeres_1895-1986_DEFINITIVO.xlsx"

raw = pd.read_excel(XLSX, sheet_name="Salario ind", header=None)
bloque = raw.iloc[5:50, [0, 5, 11, 14]].copy()
bloque.columns = ["año", "peon_bodega", "sal_industrial", "peon_viña"]
bloque = bloque.reset_index(drop=True)

def parse_year(y):
    if pd.isna(y):
        return None
    s = str(y).strip()
    if "-" in s and len(s) > 4:
        return int(s.split("-")[0])
    try:
        return int(float(s))
    except:
        return None

bloque["año"] = bloque["año"].apply(parse_year)
bloque = bloque.dropna(subset=["año"])
bloque["año"] = bloque["año"].astype(int)
bloque = bloque.set_index("año").sort_index()
for col in ["peon_bodega", "sal_industrial", "peon_viña"]:
    bloque[col] = pd.to_numeric(bloque[col], errors="coerce")

# ── 2. PALETA Y ESTILOS ───────────────────────────────────────────────────────
COLOR_BODEGA    = "#C0392B"   # terracota
COLOR_VIÑA      = "#27AE60"   # verde
COLOR_IND       = "#2980B9"   # azul

FONT_TITLE  = dict(family="Georgia, serif",    size=20, color="#1a1a2e")
FONT_AXIS   = dict(family="Arial, sans-serif", size=12, color="#333")
FONT_TICK   = dict(family="Arial, sans-serif", size=11, color="#555")
FONT_LEGEND = dict(family="Arial, sans-serif", size=12, color="#333")

# ── 3. CONSTRUIR FRAMES DE ANIMACIÓN ─────────────────────────────────────────
años = sorted(bloque.index.tolist())

frames = []
for a in años:
    subset = bloque.loc[:a]
    frame = go.Frame(
        name=str(a),
        data=[
            go.Scatter(
                x=subset.index.tolist(),
                y=subset["peon_bodega"].tolist(),
                mode="lines+markers",
                connectgaps=False,
                line=dict(color=COLOR_BODEGA, width=2.5),
                marker=dict(size=5, color=COLOR_BODEGA),
                name="Peón de bodega / Obrero vinícola",
                yaxis="y1",
                hovertemplate="<b>%{x}</b><br>Peón de bodega: %{y:.1f} $ ley 18188<extra></extra>",
            ),
            go.Scatter(
                x=subset.index.tolist(),
                y=subset["peon_viña"].tolist(),
                mode="lines+markers",
                connectgaps=False,
                line=dict(color=COLOR_VIÑA, width=2.5),
                marker=dict(size=5, color=COLOR_VIÑA),
                name="Peón de viña",
                yaxis="y1",
                hovertemplate="<b>%{x}</b><br>Peón de viña: %{y:.1f} $ ley 18188<extra></extra>",
            ),
            go.Scatter(
                x=subset.index.tolist(),
                y=subset["sal_industrial"].tolist(),
                mode="lines+markers",
                connectgaps=False,
                line=dict(color=COLOR_IND, width=2.5, dash="dot"),
                marker=dict(size=5, color=COLOR_IND),
                name="Salario industrial (Ferreres)",
                yaxis="y2",
                hovertemplate="<b>%{x}</b><br>Sal. industrial: %{y:.0f} $ de 2004<extra></extra>",
            ),
        ],
    )
    frames.append(frame)

# ── 4. FIGURA BASE ────────────────────────────────────────────────────────────
fig = go.Figure(
    data=[
        go.Scatter(
            x=[años[0]],
            y=[bloque.loc[años[0], "peon_bodega"]],
            mode="lines+markers",
            connectgaps=False,
            line=dict(color=COLOR_BODEGA, width=2.5),
            marker=dict(size=5, color=COLOR_BODEGA),
            name="Peón de bodega / Obrero vinícola",
            yaxis="y1",
            hovertemplate="<b>%{x}</b><br>Peón de bodega: %{y:.1f} $ ley 18188<extra></extra>",
        ),
        go.Scatter(
            x=[años[0]],
            y=[bloque.loc[años[0], "peon_viña"]],
            mode="lines+markers",
            connectgaps=False,
            line=dict(color=COLOR_VIÑA, width=2.5),
            marker=dict(size=5, color=COLOR_VIÑA),
            name="Peón de viña",
            yaxis="y1",
            hovertemplate="<b>%{x}</b><br>Peón de viña: %{y:.1f} $ ley 18188<extra></extra>",
        ),
        go.Scatter(
            x=[años[0]],
            y=[bloque.loc[años[0], "sal_industrial"]],
            mode="lines+markers",
            connectgaps=False,
            line=dict(color=COLOR_IND, width=2.5, dash="dot"),
            marker=dict(size=5, color=COLOR_IND),
            name="Salario industrial (Ferreres)",
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Sal. industrial: %{y:.0f} $ de 2004<extra></extra>",
        ),
    ],
    frames=frames,
)

# ── 5. LAYOUT ─────────────────────────────────────────────────────────────────
fig.update_layout(
    title=dict(
        text="Evolución de salarios reales en Mendoza, 1895–1986",
        font=FONT_TITLE,
        x=0.5,
        xanchor="center",
        y=0.97,
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=FONT_AXIS,
    margin=dict(l=70, r=90, t=90, b=140),
    legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=-0.22,
        font=FONT_LEGEND,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#ccc",
        borderwidth=1,
    ),
    xaxis=dict(
        title=dict(text="Año", font=FONT_AXIS),
        tickfont=FONT_TICK,
        gridcolor="#ebebeb",
        showline=True,
        linecolor="#aaa",
        range=[1890, 1990],
    ),
    yaxis=dict(
        title=dict(text="Salario real ($ ley 18188 / 1960)", font=dict(family="Arial, sans-serif", size=12, color=COLOR_BODEGA)),
        tickfont=dict(family="Arial, sans-serif", size=11, color=COLOR_BODEGA),
        gridcolor="#ebebeb",
        showline=True,
        linecolor="#aaa",
        rangemode="tozero",
    ),
    yaxis2=dict(
        title=dict(text="Salario industrial ($ de 2004)", font=dict(family="Arial, sans-serif", size=12, color=COLOR_IND)),
        tickfont=dict(family="Arial, sans-serif", size=11, color=COLOR_IND),
        overlaying="y",
        side="right",
        showgrid=False,
        showline=True,
        linecolor="#aaa",
        rangemode="tozero",
    ),
    annotations=[
        dict(
            text=(
                "Fuentes: Peón de bodega/Obrero vinícola y Peón de viña: <i>Salarios_varones_y_mujeres_1895-1986_DEFINITIVO.xlsx</i> &nbsp;|&nbsp; "
                "Salario industrial: <i>Base de datos Ferreres</i>"
            ),
            xref="paper", yref="paper",
            x=0.5, y=-0.32,
            xanchor="center", yanchor="top",
            showarrow=False,
            font=dict(family="Arial, sans-serif", size=10, color="#777"),
        )
    ],
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            x=0.08,
            y=-0.15,
            xanchor="left",
            yanchor="top",
            buttons=[
                dict(
                    label="▶ Reproducir",
                    method="animate",
                    args=[
                        None,
                        dict(
                            frame=dict(duration=200, redraw=True),
                            fromcurrent=True,
                            transition=dict(duration=50),
                        ),
                    ],
                ),
                dict(
                    label="⏸ Pausar",
                    method="animate",
                    args=[
                        [None],
                        dict(
                            frame=dict(duration=0, redraw=False),
                            mode="immediate",
                            transition=dict(duration=0),
                        ),
                    ],
                ),
            ],
        )
    ],
    sliders=[
        dict(
            active=0,
            currentvalue=dict(
                prefix="Año: ",
                visible=True,
                xanchor="center",
                font=dict(family="Arial, sans-serif", size=13, color="#333"),
            ),
            pad=dict(t=10, b=10),
            x=0.0,
            y=-0.12,
            len=1.0,
            steps=[
                dict(
                    args=[
                        [str(a)],
                        dict(
                            frame=dict(duration=100, redraw=True),
                            mode="immediate",
                            transition=dict(duration=50),
                        ),
                    ],
                    label=str(a),
                    method="animate",
                )
                for a in años
            ],
        )
    ],
)

# ── 6. MOSTRAR ────────────────────────────────────────────────────────────────
fig.show()

# Descomenta para guardar como HTML standalone:
# fig.write_html("salarios_evolucion.html")