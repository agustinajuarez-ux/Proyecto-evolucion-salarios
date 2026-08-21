"""
Evolución de salarios reales en Mendoza, 1895–1986
Para correr en Google Colab.

Fuentes:
  1) Salarios varones y mujeres 1895-1986 — Olguín, JHE 2025:
     salarios nominal y real peón de viña y obrero vinícola,
     hojas SN 1895-1945, SR selecc 1895-1945, Sal nom y real 1952-1986.
  2) Salario industrial (Capital Federal):
     Base de datos Ferreres (hoja «Salario ind», columna 11).
"""

# ── PASO 1: subir el archivo ──────────────────────────────────────────────────
from google.colab import files
print("Subí el archivo Salarios_varones_y_mujeres_1895-1986_DEFINITIVO.xlsx")
uploaded = files.upload()
XLSX = list(uploaded.keys())[0]

# ── PASO 2: instalar dependencias (ya vienen en Colab, pero por las dudas) ───
# !pip install plotly pandas openpyxl -q

# ── PASO 3: leer datos ────────────────────────────────────────────────────────
import pandas as pd
import plotly.graph_objects as go

raw = pd.read_excel(XLSX, sheet_name="Salario ind", header=None)
bloque = raw.iloc[5:50, [0, 5, 11, 14]].copy()
bloque.columns = ["año", "peon_bodega", "sal_industrial", "peon_viña"]
bloque = bloque.reset_index(drop=True)

def parse_year(y):
    if pd.isna(y): return None
    s = str(y).strip()
    if "-" in s and len(s) > 4: return int(s.split("-")[0])
    try: return int(float(s))
    except: return None

bloque["año"] = bloque["año"].apply(parse_year)
bloque = bloque.dropna(subset=["año"])
bloque["año"] = bloque["año"].astype(int)
bloque = bloque.set_index("año").sort_index()
for col in ["peon_bodega", "sal_industrial", "peon_viña"]:
    bloque[col] = pd.to_numeric(bloque[col], errors="coerce")

# ── PASO 4: colores y estilos ─────────────────────────────────────────────────
COLOR_BODEGA = "#C0392B"
COLOR_VIÑA   = "#27AE60"
COLOR_IND    = "#2980B9"

años = sorted(bloque.index.tolist())

# ── PASO 5: frames de animación ───────────────────────────────────────────────
frames = []
for a in años:
    subset = bloque.loc[:a]
    frames.append(go.Frame(
        name=str(a),
        data=[
            go.Scatter(
                x=subset.index.tolist(), y=subset["peon_bodega"].tolist(),
                mode="lines+markers", connectgaps=False,
                line=dict(color=COLOR_BODEGA, width=2.5),
                marker=dict(size=5, color=COLOR_BODEGA),
                name="Peón de bodega / Obrero vinícola", yaxis="y1",
                hovertemplate="<b>%{x}</b><br>Peón de bodega: %{y:.1f} $ ley 18188<extra></extra>",
            ),
            go.Scatter(
                x=subset.index.tolist(), y=subset["peon_viña"].tolist(),
                mode="lines+markers", connectgaps=False,
                line=dict(color=COLOR_VIÑA, width=2.5),
                marker=dict(size=5, color=COLOR_VIÑA),
                name="Peón de viña", yaxis="y1",
                hovertemplate="<b>%{x}</b><br>Peón de viña: %{y:.1f} $ ley 18188<extra></extra>",
            ),
            go.Scatter(
                x=subset.index.tolist(), y=subset["sal_industrial"].tolist(),
                mode="lines+markers", connectgaps=False,
                line=dict(color=COLOR_IND, width=2.5, dash="dot"),
                marker=dict(size=5, color=COLOR_IND),
                name="Salario industrial (Ferreres)", yaxis="y2",
                hovertemplate="<b>%{x}</b><br>Sal. industrial: %{y:.0f} $ de 2004<extra></extra>",
            ),
        ],
    ))

# ── PASO 6: figura base ───────────────────────────────────────────────────────
fig = go.Figure(
    data=[
        go.Scatter(
            x=[años[0]], y=[bloque.loc[años[0], "peon_bodega"]],
            mode="lines+markers", connectgaps=False,
            line=dict(color=COLOR_BODEGA, width=2.5),
            marker=dict(size=5, color=COLOR_BODEGA),
            name="Peón de bodega / Obrero vinícola", yaxis="y1",
            hovertemplate="<b>%{x}</b><br>Peón de bodega: %{y:.1f} $ ley 18188<extra></extra>",
        ),
        go.Scatter(
            x=[años[0]], y=[bloque.loc[años[0], "peon_viña"]],
            mode="lines+markers", connectgaps=False,
            line=dict(color=COLOR_VIÑA, width=2.5),
            marker=dict(size=5, color=COLOR_VIÑA),
            name="Peón de viña", yaxis="y1",
            hovertemplate="<b>%{x}</b><br>Peón de viña: %{y:.1f} $ ley 18188<extra></extra>",
        ),
        go.Scatter(
            x=[años[0]], y=[bloque.loc[años[0], "sal_industrial"]],
            mode="lines+markers", connectgaps=False,
            line=dict(color=COLOR_IND, width=2.5, dash="dot"),
            marker=dict(size=5, color=COLOR_IND),
            name="Salario industrial (Ferreres)", yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Sal. industrial: %{y:.0f} $ de 2004<extra></extra>",
        ),
    ],
    frames=frames,
)

# ── PASO 7: layout ────────────────────────────────────────────────────────────
fig.update_layout(
    title=dict(
        text="Evolución de salarios reales en Mendoza, 1895–1986",
        font=dict(family="Georgia, serif", size=20, color="#1a1a2e"),
        x=0.5, xanchor="center", y=0.97,
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial, sans-serif", size=12, color="#333"),
    margin=dict(l=70, r=90, t=90, b=160),
    legend=dict(
        orientation="h", x=0.5, xanchor="center", y=-0.25,
        font=dict(family="Arial, sans-serif", size=12, color="#333"),
        bgcolor="rgba(255,255,255,0.9)", bordercolor="#ccc", borderwidth=1,
    ),
    xaxis=dict(
        title=dict(text="Año", font=dict(family="Arial, sans-serif", size=13)),
        tickfont=dict(family="Arial, sans-serif", size=11, color="#555"),
        gridcolor="#ebebeb", showline=True, linecolor="#aaa",
        range=[1890, 1990],
    ),
    yaxis=dict(
        title=dict(
            text="Salario real ($ ley 18188 / 1960)",
            font=dict(family="Arial, sans-serif", size=13, color=COLOR_BODEGA),
        ),
        tickfont=dict(family="Arial, sans-serif", size=11, color=COLOR_BODEGA),
        gridcolor="#ebebeb", showline=True, linecolor="#aaa", rangemode="tozero",
    ),
    yaxis2=dict(
        title=dict(
            text="Salario industrial ($ de 2004)",
            font=dict(family="Arial, sans-serif", size=13, color=COLOR_IND),
        ),
        tickfont=dict(family="Arial, sans-serif", size=11, color=COLOR_IND),
        overlaying="y", side="right",
        showgrid=False, showline=True, linecolor="#aaa", rangemode="tozero",
    ),
    annotations=[
        dict(
            text=(
                "<b>Fuentes:</b> 1) <i>Salarios varones y mujeres 1895–1986 — Olguín, JHE 2025</i>: "
                "salarios nominal y real peón de viña y obrero vinícola, hojas SN 1895–1945, "
                "SR selecc 1895–1945, Sal nom y real 1952–1986. &nbsp;"
                "2) Salario industrial (Cap. Fed.): <i>Base de datos Ferreres</i> "
                "(hoja «Salario ind», col. 11). "
                "Los gaps reflejan ausencia de fuente, no interpolación."
            ),
            xref="paper", yref="paper",
            x=0.5, y=-0.38,
            xanchor="center", yanchor="top",
            showarrow=False,
            font=dict(family="Arial, sans-serif", size=10, color="#777"),
        )
    ],
    updatemenus=[
        dict(
            type="buttons", showactive=False,
            x=0.08, y=-0.18, xanchor="left", yanchor="top",
            buttons=[
                dict(
                    label="▶ Reproducir", method="animate",
                    args=[None, dict(frame=dict(duration=200, redraw=True),
                                    fromcurrent=True, transition=dict(duration=50))],
                ),
                dict(
                    label="⏸ Pausar", method="animate",
                    args=[[None], dict(frame=dict(duration=0, redraw=False),
                                      mode="immediate", transition=dict(duration=0))],
                ),
            ],
        )
    ],
    sliders=[
        dict(
            active=0,
            currentvalue=dict(
                prefix="Año: ", visible=True, xanchor="center",
                font=dict(family="Arial, sans-serif", size=13, color="#333"),
            ),
            pad=dict(t=10, b=10),
            x=0.0, y=-0.14, len=1.0,
            steps=[
                dict(
                    args=[[str(a)], dict(frame=dict(duration=100, redraw=True),
                                        mode="immediate", transition=dict(duration=50))],
                    label=str(a), method="animate",
                )
                for a in años
            ],
        )
    ],
)

# ── PASO 8: mostrar en Colab ──────────────────────────────────────────────────
fig.show()

# Para descargar el HTML desde Colab:
fig.write_html("salarios_evolucion.html")
files.download("salarios_evolucion.html")
