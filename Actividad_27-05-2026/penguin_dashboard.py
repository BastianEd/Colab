#a

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# --- Cargar y limpiar datos ---
df = pd.read_csv("/workspaces/Colab/Actividad_27-05-2026/penguins_size.csv")
df = df.dropna()
df.columns = df.columns.str.strip()

# Paleta de colores por especie
COLOR_MAP = {
    "Adelie":    "#FF6B6B",
    "Chinstrap": "#4ECDC4",
    "Gentoo":    "#FFE66D",
}

BACKGROUND = "#0D1B2A"
CARD_BG    = "#F3D7CD"
TEXT       = "#E8F4FD"
ACCENT     = "#4ECDC4"

LAYOUT_BASE = dict(
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font=dict(color=TEXT, family="IBM Plex Mono, monospace"),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
)

# ---- App ----
app = Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": BACKGROUND,
        "minHeight": "100vh",
        "fontFamily": "IBM Plex Mono, monospace",
        "color": TEXT,
        "padding": "24px",
    },
    children=[
        # Header
        html.Div([
            html.H1("🐧 PENGUIN EXPLORER", style={
                "fontSize": "2rem", "letterSpacing": "0.2em",
                "color": ACCENT, "margin": 0
            }),
            html.P(f"{len(df)} registros · Palmer Archipelago, Antarctica", style={
                "color": "#8899AA", "margin": "4px 0 0 0", "fontSize": "0.85rem"
            }),
        ], style={"marginBottom": "24px"}),

        # Filtros
        html.Div([
            html.Div([
                html.Label("Especie", style={"fontSize": "0.75rem", "color": "#8899AA"}),
                dcc.Checklist(
                    id="filter-species",
                    options=[{"label": f"  {s}", "value": s} for s in df["species"].unique()],
                    value=list(df["species"].unique()),
                    inline=True,
                    style={"marginTop": "6px"},
                    labelStyle={"marginRight": "16px", "cursor": "pointer"},
                ),
            ], style={"flex": 1}),
            html.Div([
                html.Label("Isla", style={"fontSize": "0.75rem", "color": "#8899AA"}),
                dcc.Checklist(
                    id="filter-island",
                    options=[{"label": f"  {i}", "value": i} for i in df["island"].unique()],
                    value=list(df["island"].unique()),
                    inline=True,
                    style={"marginTop": "6px"},
                    labelStyle={"marginRight": "16px", "cursor": "pointer"},
                ),
            ], style={"flex": 1}),
            html.Div([
                html.Label("Sexo", style={"fontSize": "0.75rem", "color": "#8899AA"}),
                dcc.Checklist(
                    id="filter-sex",
                    options=[{"label": f"  {s}", "value": s} for s in df["sex"].unique()],
                    value=list(df["sex"].unique()),
                    inline=True,
                    style={"marginTop": "6px"},
                    labelStyle={"marginRight": "16px", "cursor": "pointer"},
                ),
            ], style={"flex": 1}),
        ], style={
            "display": "flex", "gap": "24px", "flexWrap": "wrap",
            "backgroundColor": CARD_BG, "borderRadius": "12px",
            "padding": "16px 20px", "marginBottom": "20px",
            "border": f"1px solid #2A3F5A"
        }),

        # KPIs
        html.Div(id="kpi-row", style={
            "display": "flex", "gap": "16px", "marginBottom": "20px", "flexWrap": "wrap"
        }),

        # Gráficos fila 1
        html.Div([
            html.Div(dcc.Graph(id="scatter-main"), style={
                "flex": "2", "backgroundColor": CARD_BG,
                "borderRadius": "12px", "border": "1px solid #2A3F5A", "padding": "8px"
            }),
            html.Div(dcc.Graph(id="box-mass"), style={
                "flex": "1", "backgroundColor": CARD_BG,
                "borderRadius": "12px", "border": "1px solid #2A3F5A", "padding": "8px"
            }),
        ], style={"display": "flex", "gap": "16px", "marginBottom": "16px", "flexWrap": "wrap"}),

        # Gráficos fila 2
        html.Div([
            html.Div(dcc.Graph(id="bar-island"), style={
                "flex": "1", "backgroundColor": CARD_BG,
                "borderRadius": "12px", "border": "1px solid #2A3F5A", "padding": "8px"
            }),
            html.Div(dcc.Graph(id="hist-flipper"), style={
                "flex": "1", "backgroundColor": CARD_BG,
                "borderRadius": "12px", "border": "1px solid #2A3F5A", "padding": "8px"
            }),
            html.Div(dcc.Graph(id="scatter-culmen"), style={
                "flex": "1", "backgroundColor": CARD_BG,
                "borderRadius": "12px", "border": "1px solid #2A3F5A", "padding": "8px"
            }),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),
    ]
)


def filter_df(species, island, sex):
    return df[
        df["species"].isin(species) &
        df["island"].isin(island) &
        df["sex"].isin(sex)
    ]


@app.callback(
    Output("kpi-row", "children"),
    Output("scatter-main", "figure"),
    Output("box-mass", "figure"),
    Output("bar-island", "figure"),
    Output("hist-flipper", "figure"),
    Output("scatter-culmen", "figure"),
    Input("filter-species", "value"),
    Input("filter-island", "value"),
    Input("filter-sex", "value"),
)
def update(species, island, sex):
    d = filter_df(species or [], island or [], sex or [])

    # KPIs
    kpis = []
    for label, val in [
        ("Pingüinos", f"{len(d)}"),
        ("Masa media (g)", f"{d['body_mass_g'].mean():.0f}" if len(d) else "—"),
        ("Aleta media (mm)", f"{d['flipper_length_mm'].mean():.1f}" if len(d) else "—"),
        ("Culmen medio (mm)", f"{d['culmen_length_mm'].mean():.1f}" if len(d) else "—"),
    ]:
        kpis.append(html.Div([
            html.P(label, style={"margin": 0, "fontSize": "0.7rem", "color": "#8899AA", "letterSpacing": "0.1em"}),
            html.H2(val, style={"margin": "4px 0 0 0", "color": ACCENT, "fontSize": "1.6rem"}),
        ], style={
            "backgroundColor": CARD_BG, "borderRadius": "10px",
            "padding": "14px 20px", "border": "1px solid #2A3F5A",
            "minWidth": "140px", "flex": "1"
        }))

    # Scatter principal: aleta vs masa
    fig_scatter = px.scatter(
        d, x="flipper_length_mm", y="body_mass_g",
        color="species", size="culmen_length_mm",
        hover_data=["island", "sex"],
        color_discrete_map=COLOR_MAP,
        title="Longitud de aleta vs Masa corporal",
        labels={"flipper_length_mm": "Aleta (mm)", "body_mass_g": "Masa (g)"},
    )
    fig_scatter.update_layout(**LAYOUT_BASE)
    fig_scatter.update_traces(marker=dict(opacity=0.8, line=dict(width=0)))

    # Box: masa por especie
    fig_box = px.box(
        d, x="species", y="body_mass_g", color="species",
        color_discrete_map=COLOR_MAP,
        title="Masa por especie",
        labels={"body_mass_g": "Masa (g)", "species": ""},
    )
    fig_box.update_layout(**LAYOUT_BASE, showlegend=False)

    # Bar: conteo por isla
    counts = d.groupby(["island", "species"]).size().reset_index(name="count")
    fig_bar = px.bar(
        counts, x="island", y="count", color="species",
        color_discrete_map=COLOR_MAP,
        title="Distribución por isla",
        labels={"count": "Cantidad", "island": "Isla"},
        barmode="group",
    )
    fig_bar.update_layout(**LAYOUT_BASE)

    # Histograma: aleta
    fig_hist = px.histogram(
        d, x="flipper_length_mm", color="species",
        color_discrete_map=COLOR_MAP,
        title="Distribución longitud de aleta",
        labels={"flipper_length_mm": "Aleta (mm)"},
        barmode="overlay", opacity=0.75,
    )
    fig_hist.update_layout(**LAYOUT_BASE)

    # Scatter culmen
    fig_culmen = px.scatter(
        d, x="culmen_length_mm", y="culmen_depth_mm",
        color="species", symbol="sex",
        color_discrete_map=COLOR_MAP,
        title="Culmen: largo vs profundidad",
        labels={"culmen_length_mm": "Largo (mm)", "culmen_depth_mm": "Profundidad (mm)"},
    )
    fig_culmen.update_layout(**LAYOUT_BASE)
    fig_culmen.update_traces(marker=dict(opacity=0.85, line=dict(width=0)))

    return kpis, fig_scatter, fig_box, fig_bar, fig_hist, fig_culmen


if __name__ == "__main__":
    app.run(debug=True, port=8050)
