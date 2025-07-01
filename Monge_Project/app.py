import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback_context
from dash import dash_table
import plotly.express as px

# Load the dataset (adjusted path)
df = pd.read_csv("education_analysis_dataset_clean.csv")

#Efficiency 
df["Efficiency_Graduation"] = df["BachelorRate"] / df["Expenditure"]
df["Efficiency_Employment_Females"] = df["EmploymentRate_Females"] / df["Expenditure"]
df["Efficiency_Employment_Males"] = df["EmploymentRate_Males"] / df["Expenditure"]

# Convert wide format to long format for Employment by Sex
df_long = pd.melt(
    df,
    id_vars=["Year", "Country", "BachelorRate", "MasterRate"],
    value_vars=["EmploymentRate_Females", "EmploymentRate_Males"],
    var_name="Sex",
    value_name="EmploymentRate"
)

# Renombrar valores para mejor visualización
df_long["Sex"] = df_long["Sex"].replace({
    "EmploymentRate_Females": "Female",
    "EmploymentRate_Males": "Male"
})


# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Education & Employment in Europe"

# Color palette: Yellow-Orange-Blue
color_palette = px.colors.sequential.YlOrBr + px.colors.sequential.Blues[::-1]

# App layout with location routing
app.layout = html.Div(style={"fontFamily": "Arial, sans-serif"}, children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
    ])

card_style = {
    "backgroundColor": "#ffffffdf",
    "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
    "padding": "20px",
    "borderRadius": "12px",
    "textAlign": "center",
    "flex": "1",
    "fontFamily": "Arial, sans-serif",
    "color": "#375999",
    "transition": "transform 0.2s",
    "cursor": "default",
    "userSelect": "none"
}

# Calcular KPIs para las tarjetas
max_investment_country = df.groupby("Country")["Expenditure"].mean().idxmax()
max_investment_value = df.groupby("Country")["Expenditure"].mean().max()

# Promedio empleo por país (promedio de hombres y mujeres)
employment_avg = df.groupby("Country")[["EmploymentRate_Females", "EmploymentRate_Males"]].mean()
employment_avg["Average"] = employment_avg.mean(axis=1)
max_employment_country = employment_avg["Average"].idxmax()
max_employment_value = employment_avg["Average"].max()

# Calcular eficiencia (graduación / gasto)
df["Efficiency_Graduation"] = df["BachelorRate"] / df["Expenditure"]
efficiency_avg = df.groupby("Country")["Efficiency_Graduation"].mean()
max_efficiency_country = efficiency_avg.idxmax()
max_efficiency_value = efficiency_avg.max()

# Crear componente con las tarjetas KPI
insight_cards = html.Div([
    html.Div([
        html.H3("Highest Investment"),
        html.P(f"{max_investment_country}: €{max_investment_value:,.1f}M")
    ], style=card_style),

    html.Div([
        html.H3("Highest Employment Rate (Avg)"),
        html.P(f"{max_employment_country}: {max_employment_value:.1f}%")
    ], style=card_style),

    html.Div([
        html.H3("Highest Efficiency (Graduation / Expenditure)"),
        html.P(f"{max_efficiency_country}: {max_efficiency_value:.2f}")
    ], style=card_style),
], style={
    "display": "flex",
    "justifyContent": "space-around",
    "margin": "40px auto",
    "maxWidth": "900px",
    "gap": "20px"
})


# Home Page Layout
home_layout = html.Div([
    html.Div([
        html.H1("Education & Employment in Europe", style={
            "textAlign": "center",
            "fontSize": "48px",
            "color": "black",
            "paddingTop": "50px"
            
        }),
        html.H2("Explore how investment in tertiary education impacts outcomes across Europe.", style={
            "textAlign": "center",
            "fontSize": "24px",
            "color": "black"
        }),

        insight_cards,

        html.Div([
            html.Div([
                html.A(html.Button("Graduation vs. Expenditure", style={
                    "backgroundColor": "#ffffffcc",
                    "color": "#333",
                    "fontSize": "18px",
                    "padding": "15px 30px",
                    "margin": "10px",
                    "borderRadius": "12px",
                    "border": "none",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                    "cursor": "pointer",
                    "fontWeight": "bold"
                }), href="/hypothesis1"),

                html.A(html.Button("Graduation vs. Employment", style={
                    "backgroundColor": "#ffffffcc",
                    "color": "#333",
                    "fontSize": "18px",
                    "padding": "15px 30px",
                    "margin": "10px",
                    "borderRadius": "12px",
                    "border": "none",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                    "cursor": "pointer",
                    "fontWeight": "bold"
                }), href="/hypothesis2"),

                html.A(html.Button("Employment by Gender", style={
                    "backgroundColor": "#ffffffcc",
                    "color": "#333",
                    "fontSize": "18px",
                    "padding": "15px 30px",
                    "margin": "10px",
                    "borderRadius": "12px",
                    "border": "none",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                    "cursor": "pointer",
                    "fontWeight": "bold"
                }), href="/hypothesis3"),

                html.A(html.Button("Efficiency Index", style={
                "backgroundColor": "#ffffffcc",
                "color": "#333",
                "fontSize": "18px",
                "padding": "15px 30px",
                "margin": "10px",
                "borderRadius": "12px",
                "border": "none",
                "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                "cursor": "pointer",
                "fontWeight": "bold"
                }), href="/efficiency"),

                html.A(html.Button("Interactive Map", style={
                    "backgroundColor": "#ffffffcc",
                    "color": "#333",
                    "fontSize": "18px",
                    "padding": "15px 30px",
                    "margin": "10px",
                    "borderRadius": "12px",
                    "border": "none",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                    "cursor": "pointer",
                    "fontWeight": "bold"
                }), href="/map"),

                    html.A(html.Button("Custom Graph", style={
                    "backgroundColor": "#ffffffcc",
                    "color": "#333",
                    "fontSize": "18px",
                    "padding": "15px 30px",
                    "margin": "10px",
                    "borderRadius": "12px",
                    "border": "none",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                    "cursor": "pointer",
                    "fontWeight": "bold"
                }), href="/custom"),

                html.A(html.Button("Anomaly Detection", style={
                    "backgroundColor": "#ffffffcc",
                    "color": "#333",
                    "fontSize": "18px",
                    "padding": "15px 30px",
                    "margin": "10px",
                    "borderRadius": "12px",
                    "border": "none",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                    "cursor": "pointer",
                    "fontWeight": "bold"
                }), href="/anomalies"),

            ], style={"textAlign": "center", "padding": "40px"}),

        ], style={"textAlign": "center", "padding": "40px"}),
        html.Footer("Created by Celeste Monge", style={"textAlign": "center", "color": "gray", "paddingBottom": "30px", "fontSize": "16px"})
    ], 
    style={
        "backgroundImage": "url('/assets/fondo.jpg')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "minHeight": "100vh",
        "padding": "20px",
        "color": "white"
    })
])

# Create function to wrap graph layouts with back button
def graph_layout(title, description, controls, graph_id):
    return html.Div([
        
    html.Div([
        html.A("← Back to Home", href="/", style={
            "display": "inline-block", 
            "marginBottom": "20px", 
            "color": "#1f2a40", 
            "fontWeight": "bold",
            "textDecoration": "none"
        }),
        html.P(id="investment-highlight", style={
            "textAlign": "center",
            "fontSize": "20px",
            "color": "#1f2a40",
            "marginTop": "20px",
            "fontWeight": "500"
        }),
        html.H3(title, style={
            "marginTop": "10px", 
            "fontSize": "28px", 
            "color": "#1f2a40"
        }),
        html.P(description, style={
            "color": "#444", 
            "fontSize": "16px"
        }),
        *controls,
        dcc.Graph(id=graph_id)

    ], style={
        "backgroundColor": "white",
        "padding": "40px",
        "maxWidth": "1000px",
        "margin": "60px auto",
        "boxShadow": "none",
        "borderRadius": "16px",
        "animation": "fadeIn 1.2s ease-in-out",
        "fontFamily": "Arial, sans-serif"
    })
], style={
    "backgroundColor": "#ffffff",
    "minHeight": "100vh",
    "padding": "40px"
})


# Layouts for each hypothesis
h1_layout = graph_layout(
    "Education Investment vs. Graduation Rates",
    "Compare how much countries invest in tertiary education versus their graduation outcomes. Bachelor graduation is on the Y-axis, education investment on the X-axis, and Master graduation is shown as the size of each bubble.",
    [
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="h1-year",
            options=[{"label": y, "value": y} for y in sorted(df["Year"].unique())],
            value=df["Year"].min(),
            style={"marginBottom": "20px"}
        ),

        html.Label("Select Degree Type:"),
        dcc.Dropdown(
            id="h1-degree-mode",
            options=[
                {"label": "Bachelor only", "value": "bachelor"},
                {"label": "Master only", "value": "master"},
                {"label": "Both (bubble size shows Master)", "value": "both"}
            ],
            value="both",
            style={"marginBottom": "20px"}
        ),

        html.Label("Select Countries:"),
        dcc.Dropdown(
            id="h1-countries",
            options=[{"label": c, "value": c} for c in sorted(df["Country"].unique())],
            value=sorted(df["Country"].unique())[:5],
            multi=True,
            placeholder="Select countries...",
            style={
                "borderRadius": "10px",
                "padding": "10px",
                "fontSize": "16px",
                "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
                "backgroundColor": "#f8f9fa",
                "border": "1px solid #ced4da",
                "marginBottom": "30px"
            }
        )
    ],
    "h1-graph"
)




h2_layout = graph_layout(
    "Graduation Rate vs. Employment Rate by Gender",
    "This chart compares graduation rates with employment rates for females and males in each country.",
    [
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="h2-year",
            options=[{"label": y, "value": y} for y in sorted(df["Year"].unique())],
            value=df["Year"].min()
        ),
        html.Label("Select Degree Type:"),
        dcc.Dropdown(
            id="h2-degree",
            options=[
                {"label": "Bachelor", "value": "BachelorRate"},
                {"label": "Master", "value": "MasterRate"}
            ],
            value="BachelorRate"
        )
    ],
    "h2-graph"
)


h3_layout = graph_layout(
    "Impact of Educational Investment on Employability by Gender Over Time",
    "This line chart allows you to explore how male and female employment rates evolve over the years in a selected country, in relation to investment in education.",
    [
        html.Label("Select Country:"),
        dcc.Dropdown(
            id="h3-country",
            options=[{"label": c, "value": c} for c in sorted(df["Country"].unique())],
            value=sorted(df["Country"].unique())[0],
            style={
                "borderRadius": "10px",
                "padding": "10px",
                "fontSize": "16px",
                "width": "60%",
                "marginBottom": "20px"
            }
        )
    ],
    "h3-graph"
)

years = sorted(df["Year"].unique())
marks = {int(y): str(y) for y in years}

map_layout = html.Div([
    html.A("← Back to Home", href="/", style={
        "display": "inline-block",
        "marginBottom": "20px",
        "color": "#1f2a40",
        "fontWeight": "bold",
        "textDecoration": "none"
    }),
    html.H2("Interactive Map", style={
        "textAlign": "center",
        "color": "#1f2a40",
        "marginBottom": "20px"
    }),
    html.Label("Select Variable to Display:", style={"fontWeight": "bold", "marginLeft": "20px"}),
    dcc.Dropdown(
        id="map-variable-dropdown",
        options=[
            {"label": "Education Expenditure (Million €)", "value": "Expenditure"},
            {"label": "Graduation Rate Bachelor (%)", "value": "BachelorRate"},
            {"label": "Graduation Rate Master (%)", "value": "MasterRate"},
            {"label": "Employment Rate Females (%)", "value": "EmploymentRate_Females"},
            {"label": "Employment Rate Males (%)", "value": "EmploymentRate_Males"}
        ],
        value="Expenditure",
        clearable=False,
        style={"width": "60%", "margin": "0 auto 30px auto"}
    ),
    html.Label("Select Year:", style={"fontWeight": "bold", "marginLeft": "20px"}),
    dcc.Slider(
        id="map-year-slider",
        min=int(years[0]),
        max=int(years[-1]),
        step=1,
        value=int(years[0]),
        marks=marks,
        tooltip={"placement": "bottom", "always_visible": True},
        updatemode='drag'
    ),
    dcc.Graph(id="map-graph", style={"height": "700px", "marginTop": "30px"})
], style={"maxWidth": "1000px", "margin": "auto", "padding": "20px"})


custom_layout = graph_layout(
    "Custom Chart Builder",
    "Select the variables you want to plot and compare from the dataset.",
    [
        html.Label("Select X-Axis Variable:"),
        dcc.Dropdown(
            id="custom-x",
            options=[{"label": col, "value": col} for col in df.columns if df[col].dtype != "object"],
            value="Expenditure",
            style={"marginBottom": "20px"}
        ),

        html.Label("Select Y-Axis Variable:"),
        dcc.Dropdown(
            id="custom-y",
            options=[{"label": col, "value": col} for col in df.columns if df[col].dtype != "object"],
            value="BachelorRate",
            style={"marginBottom": "20px"}
        ),

        html.Label("Select Year:"),
        dcc.Dropdown(
            id="custom-year",
            options=[{"label": y, "value": y} for y in sorted(df["Year"].unique())],
            value=df["Year"].min(),
            style={"marginBottom": "20px"}
        ),

        html.Label("Select Countries (optional):"),
        dcc.Dropdown(
            id="custom-countries",
            options=[{"label": c, "value": c} for c in sorted(df["Country"].unique())],
            value=[],
            multi=True,
            placeholder="Leave empty to show all countries"
        )
    ],
    "custom-graph"
)
anomaly_layout = html.Div([
    html.Div([
        html.A("← Back to Home", href="/", style={
            "display": "inline-block",
            "marginBottom": "20px",
            "color": "#1f2a40",
            "fontWeight": "bold",
            "textDecoration": "none"
        }),
        html.H3("Anomaly Detection in Education and Employment Data", style={
            "marginTop": "10px",
            "fontSize": "28px",
            "color": "#1f2a40"
        }),
        html.P("Identify unusual data points in investment, graduation, or employment metrics using the Interquartile Range (IQR) method.", style={
            "color": "#444",
            "fontSize": "16px"
        }),
        html.Label("Select Metric to Analyze:"),
        dcc.Dropdown(
            id="anomaly-metric",
            options=[
                {"label": "Education Expenditure", "value": "Expenditure"},
                {"label": "Bachelor Graduation Rate", "value": "BachelorRate"},
                {"label": "Master Graduation Rate", "value": "MasterRate"},
                {"label": "Employment Rate (Females)", "value": "EmploymentRate_Females"},
                {"label": "Employment Rate (Males)", "value": "EmploymentRate_Males"},
            ],
            value="Expenditure",
            style={
                "borderRadius": "10px",
                "padding": "10px",
                "fontSize": "16px",
                "width": "60%",
                "marginBottom": "30px"
            }
        ),
        html.Div([
    html.H3("What is an Anomaly?", style={
        "fontSize": "24px", "marginBottom": "10px", "color": "#1f2a40"
    }),
    html.P("An anomaly is a value that stands out because it's much higher or lower than most other values. "
           "We use a simple statistical method to detect them based on quartiles and the interquartile range (IQR):", 
           style={"fontSize": "16px", "color": "#333"}),
    html.Ul([
        html.Li("Q1 = 25th percentile (lower bound of the 'normal' range)"),
        html.Li("Q3 = 75th percentile (upper bound of the 'normal' range)"),
        html.Li("IQR = Q3 - Q1"),
        html.Li("Lower limit = Q1 - 1.5 × IQR"),
        html.Li("Upper limit = Q3 + 1.5 × IQR")
    ], style={"fontSize": "15px", "color": "#333", "paddingLeft": "20px"}),
    html.P("Any value outside this range is flagged as an anomaly.", style={
        "fontSize": "16px", "color": "#333", "marginTop": "10px", "fontStyle": "italic"
    }),
        ], style={
            "backgroundColor": "#ffffff",
            "padding": "30px",
            "margin": "30px auto",
            "borderRadius": "12px",
            "boxShadow": "none",
            "maxWidth": "900px"
        }),

        dcc.Graph(id="anomaly-graph"),
        html.Div(id="anomaly-table")

    ], style={
        "backgroundColor": "white",
        "padding": "40px",
        "maxWidth": "1000px",
        "margin": "60px auto",
        "boxShadow": "none",
        "borderRadius": "16px",
        "animation": "fadeIn 1.2s ease-in-out",
        "fontFamily": "Arial, sans-serif"
    })
], style={
    "backgroundColor": "#ffffff",
    "minHeight": "100vh",
    "padding": "40px"
})


df["Efficiency_Graduation"] = df["BachelorRate"] / df["Expenditure"]
df["Efficiency_Employment_Females"] = df["EmploymentRate_Females"] / df["Expenditure"]
df["Efficiency_Employment_Males"] = df["EmploymentRate_Males"] / df["Expenditure"]
efficiency_layout = html.Div([
    html.Div([
        html.A("← Back to Home", href="/", style={
            "display": "inline-block",
            "marginBottom": "20px",
            "color": "#1f2a40",
            "fontWeight": "bold",
            "textDecoration": "none"
        }),
        html.H3("Educational and Employment Efficiency Index by Country", style={
            "marginTop": "10px",
            "fontSize": "28px",
            "color": "#1f2a40"
        }),
        html.P("This section shows efficiency indicators calculated as graduation or employment rate divided by education expenditure. Compare how effectively countries turn investment into results.", style={
            "color": "#444",
            "fontSize": "16px",
            "marginBottom": "30px"
        }),

        # Selector de año
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="efficiency-year",
            options=[{"label": y, "value": y} for y in sorted(df["Year"].unique())],
            value=df["Year"].min(),
            style={"marginBottom": "30px", "width": "40%"}
        ),

        # Gráfico eficiencia graduación
        dcc.Graph(id="efficiency-grad-graph"),

        # Gráfico eficiencia empleo femenino
        dcc.Graph(id="efficiency-emp-female-graph"),

        # Gráfico eficiencia empleo masculino
        dcc.Graph(id="efficiency-emp-male-graph"),

    ], style={
        "backgroundColor": "white",
        "padding": "40px",
        "maxWidth": "1000px",
        "margin": "60px auto",
        "boxShadow": "none",
        "borderRadius": "16px",
        "fontFamily": "Arial, sans-serif"
    })
], style={
    "backgroundColor": "#ffffff",
    "minHeight": "100vh",
    "padding": "40px"
})



# Routing callback
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/hypothesis1':
        return h1_layout
    elif pathname == '/hypothesis2':
        return h2_layout
    elif pathname == '/hypothesis3':
        return h3_layout
    elif pathname == '/map':
        return map_layout
    elif pathname == '/custom':
        return custom_layout
    elif pathname == '/anomalies':
        return anomaly_layout
    elif pathname == "/efficiency":
        return efficiency_layout

    else:
        return home_layout

# Graph Callbacks
@app.callback(
    Output("h1-graph", "figure"),
    [Input("h1-year", "value"), Input("h1-countries", "value"), Input("h1-degree-mode", "value")]
)
def update_h1_graph(year, selected_countries, mode):
    dff = df[(df["Year"] == year) & (df["Country"].isin(selected_countries))]

    if dff.empty:
        fig = px.scatter()
        fig.add_annotation(
            text="No data available for the selected filters.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="red")
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        return fig

    if mode == "bachelor":
        y_col = "BachelorRate"
        size_col = None
        title = "Education Investment vs. Bachelor Graduation"
    elif mode == "master":
        y_col = "MasterRate"
        size_col = None
        title = "Education Investment vs. Master Graduation"
    else:  # both
        y_col = "BachelorRate"
        size_col = "MasterRate"
        title = "Investment vs. Bachelor (Y) + Master (Size)"

    fig = px.scatter(
        dff,
        x="Expenditure",
        y=y_col,
        size=size_col,
        color="Country",
        hover_name="Country",
        labels={
            "Expenditure": "Education Expenditure (Million €)",
            y_col: f"{y_col.replace('Rate', '')} Graduation Rate (%)",
            "MasterRate": "Master Graduation Rate (%)"
        },
        size_max=60,
        color_discrete_sequence=px.colors.diverging.Portland  # strong/vibrant yellow-orange-blue
    )

    fig.update_traces(marker=dict(line=dict(width=1, color="black")))

    fig.update_layout(
        title=title + f" – {year}",
        xaxis_title="Education Expenditure (Million €)",
        yaxis_title=f"{y_col.replace('Rate', '')} Graduation Rate (%)",
        font=dict(family="Arial", size=14),
        height=650,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title="Country",
        transition={"duration": 1000, "easing": "cubic-in-out"}
    )

    return fig


@app.callback(
    Output("h2-graph", "figure"),
    [Input("h2-year", "value"), Input("h2-degree", "value")]
)
def update_h2_graph(year, degree_col):
    dff = df_long[df_long["Year"] == year].dropna(subset=[degree_col, "EmploymentRate"])

    if dff.empty:
        return px.scatter(title="No data available for the selected year.")

    fig = px.scatter(
        dff,
        x=degree_col,
        y="EmploymentRate",
        color="Country",
        facet_col="Sex",
        hover_name="Country",
        labels={
            degree_col: f"{degree_col.replace('Rate', '')} Graduation Rate (%)",
            "EmploymentRate": "Employment Rate (%)",
            "Sex": "Gender"
        },
        color_discrete_sequence=px.colors.sequential.YlOrBr + px.colors.sequential.Blues[::-1],
        height=600
    )

    fig.update_layout(
        title=f"Graduation Rate vs Employment Rate by Gender – {year}",
        font=dict(family="Arial", size=15),
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#ffffff",
        margin=dict(t=60, l=40, r=40, b=40)
    )

    return fig


@app.callback(Output("h3-graph", "figure"), Input("h3-country", "value"))
def update_h3_graph(country):
    dff = df[df["Country"] == country].dropna(subset=["Year", "EmploymentRate_Females", "EmploymentRate_Males"])

    if dff.empty:
        return px.line(title="No data available for the selected country.")

    # Melt para formato largo
    dff_long = pd.melt(
        dff,
        id_vars=["Year", "Expenditure"],
        value_vars=["EmploymentRate_Females", "EmploymentRate_Males"],
        var_name="Sex",
        value_name="EmploymentRate"
    )

    dff_long["Sex"] = dff_long["Sex"].replace({
        "EmploymentRate_Females": "Female",
        "EmploymentRate_Males": "Male"
    })

    # Gráfico
    fig = px.line(
        dff_long,
        x="Year",
        y="EmploymentRate",
        color="Sex",
        markers=True,
        labels={
            "Year": "Year",
            "EmploymentRate": "Employment Rate (%)",
            "Sex": "Gender"
        },
        color_discrete_map={
            "Female": "#FFFD69",
            "Male": "#1E90FF"
        },
        height=600
    )

    fig.update_layout(
        title=f"Employment Rate by Gender in {country} Over Time",
        font=dict(family="Arial", size=15),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(t=60, l=40, r=40, b=40)
    )

    return fig

@app.callback(
    [
        Output("efficiency-grad-graph", "figure"),
        Output("efficiency-emp-female-graph", "figure"),
        Output("efficiency-emp-male-graph", "figure")
    ],
    [Input("efficiency-year", "value")]
)
def update_efficiency_graphs(year):
    dff = df[df["Year"] == year]

    if dff.empty:
        no_data_fig = px.bar()
        no_data_fig.add_annotation(
            text="No data available for the selected year.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="red")
        )
        no_data_fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        return no_data_fig, no_data_fig, no_data_fig

    # Graduación / gasto
    fig_grad = px.bar(
        dff.sort_values("Efficiency_Graduation", ascending=False),
        x="Country",
        y="Efficiency_Graduation",
        labels={
            "Efficiency_Graduation": "Graduation Rate / Expenditure",
            "Country": "Country"
        },
        title=f"Graduation Efficiency by Country – {year}",
        color="Efficiency_Graduation",
        color_continuous_scale=px.colors.sequential.YlOrBr,
        height=400
    )
    fig_grad.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    # Empleo femenino / gasto
    fig_emp_female = px.bar(
        dff.sort_values("Efficiency_Employment_Females", ascending=False),
        x="Country",
        y="Efficiency_Employment_Females",
        labels={
            "Efficiency_Employment_Females": "Employment Rate Females / Expenditure",
            "Country": "Country"
        },
        title=f"Employment Efficiency (Females) by Country – {year}",
        color="Efficiency_Employment_Females",
        color_continuous_scale=px.colors.sequential.Blues,
        height=400
    )
    fig_emp_female.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    # Empleo masculino / gasto
    fig_emp_male = px.bar(
        dff.sort_values("Efficiency_Employment_Males", ascending=False),
        x="Country",
        y="Efficiency_Employment_Males",
        labels={
            "Efficiency_Employment_Males": "Employment Rate Males / Expenditure",
            "Country": "Country"
        },
        title=f"Employment Efficiency (Males) by Country – {year}",
        color="Efficiency_Employment_Males",
        color_continuous_scale=px.colors.sequential.Blues,
        height=400
    )
    fig_emp_male.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    return fig_grad, fig_emp_female, fig_emp_male


@app.callback(
    Output("map-graph", "figure"),
    [Input("map-variable-dropdown", "value"), Input("map-year-slider", "value")]
)
def update_map(variable, year):
    dff = df[df["Year"] == year].copy()

    # Algunos países podrían no tener datos, asignamos NaN para que sean blancos
    dff[variable] = dff[variable].replace({0: None})  # O depende de cómo manejas datos faltantes

    fig = px.choropleth(
        dff,
        locations="Country",
        locationmode="country names",
        color=variable,
        color_continuous_scale=px.colors.sequential.Blues,
        hover_name="Country",
        hover_data={variable: ":,.2f"},
        labels={variable: variable.replace("_", " ")},
        scope="europe"
    )

    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        coloraxis_colorbar=dict(title=variable.replace("_", " ")),
        title=f"{variable.replace('_', ' ')} in Europe, {year}",
        font=dict(family="Arial", size=14),
        paper_bgcolor="white"
    )

    return fig


@app.callback(
    Output("custom-graph", "figure"),
    [Input("custom-x", "value"), Input("custom-y", "value"), Input("custom-year", "value"), Input("custom-countries", "value")]
)
def update_custom_graph(x_col, y_col, year, selected_countries):
    dff = df[df["Year"] == year]

    if selected_countries:
        dff = dff[dff["Country"].isin(selected_countries)]

    dff = dff.dropna(subset=[x_col, y_col])

    if dff.empty:
        fig = px.scatter()
        fig.add_annotation(
            text="No data available for the selected options.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="red")
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        return fig

    fig = px.scatter(
        dff,
        x=x_col,
        y=y_col,
        color="Country",
        hover_name="Country",
        labels={
            x_col: x_col.replace("_", " "),
            y_col: y_col.replace("_", " ")
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
        height=600
    )

    fig.update_traces(marker=dict(size=12, line=dict(width=1, color="black")))

    fig.update_layout(
        title=f"{y_col} vs {x_col} – {year}",
        xaxis_title=x_col.replace("_", " "),
        yaxis_title=y_col.replace("_", " "),
        font=dict(family="Arial", size=14),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title="Country",
        transition={"duration": 800, "easing": "cubic-in-out"}
    )

    return fig


@app.callback(
    [Output("anomaly-graph", "figure"),
     Output("anomaly-table", "children")],
    Input("anomaly-metric", "value")
)
def detect_anomalies(metric):
    dff = df[["Year", "Country", metric]].dropna()

    Q1 = dff[metric].quantile(0.25)
    Q3 = dff[metric].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    # Identificar outliers y razón
    def explain(value):
        if value < lower:
            return f"Below normal range (Q1 - 1.5×IQR)"
        elif value > upper:
            return f"Above normal range (Q3 + 1.5×IQR)"
        else:
            return None

    dff["Explanation"] = dff[metric].apply(explain)
    outliers = dff[dff["Explanation"].notnull()]

    # Crear gráfico sin mostrar columna de anomalía
    fig = px.scatter(
        dff,
        x="Year",
        y=metric,
        color=dff["Explanation"].notnull().map({True: "Anomaly", False: "Normal"}),
        hover_name="Country",
        labels={
            metric: metric.replace("_", " "),
        },
        color_discrete_map={"Anomaly": "#FF4C4C", "Normal": "#B0B0B0"},
        height=600
    )

    fig.update_layout(
        title=f"Anomaly Detection for {metric.replace('_', ' ')}",
        font=dict(family="Arial", size=14),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        legend_title="",
        margin=dict(t=60, l=40, r=40, b=40)
    )

    # Crear tabla explicativa
    if outliers.empty:
        table = html.P("No anomalies found for this metric.", style={"marginTop": "30px", "fontSize": "16px"})
    else:
        table = dash_table.DataTable(
            columns=[
                {"name": "Country", "id": "Country"},
                {"name": "Year", "id": "Year"},
                {"name": metric.replace("_", " "), "id": metric},
                {"name": "Explanation", "id": "Explanation"},
            ],
            data=outliers.to_dict("records"),
            style_table={"marginTop": "30px", "overflowX": "auto"},
            style_cell={
                "textAlign": "center",
                "padding": "8px",
                "fontFamily": "Arial"
            },
            style_header={
                "backgroundColor": "#f8f9fa",
                "fontWeight": "bold"
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#f3f3f3"
                }
            ],
        )

    return fig, table





if __name__ == '__main__':
    app.run(debug=True)



