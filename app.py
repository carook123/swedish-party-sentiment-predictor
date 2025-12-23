import dash
from dash import html, dcc
import plotly.graph_objects as go
from threading import Timer
import webbrowser
import joblib
import random

from src.predict_sentiment import predict_sentiment
from dash import Input, Output, State

# Server constants
port = 8050
host = "localhost"

# Loading evaluating metrics
metrics = joblib.load("models/model_metrics.joblib")

avg_r2 = metrics["average"]["r2"]
avg_mse = metrics["average"]["mse"]

# Metric-ranges for random input
metric_ranges = {
    "metric-1": (250, 420),          # CPI
    "metric-2": (5000, 20000),       # EC
    "metric-3": (1000000, 1300000),  # GD
    "metric-4": (-15, 20),           # MSR
    "metric-5": (1, 6),              # MIR
    "metric-6": (10300000, 10500000),# Pop
    "metric-7": (5, 11),             # UR
}

def open_browser(host=host, port=port) -> None:
    """
    Call to Webbrowser to open server when running
    """

    webbrowser.open_new(f"http://{host}:{port}")

def _metric_input(label: str, component_id: str, placeholder: str, info_text: str):
    """Helper for a clean, consistent input card with clickable info button."""

    info_div_id = f"{component_id}-info"  

    return html.Div(
        style={"minWidth": 0, "maxWidth": "60%"},
        children=[
            html.Label(
                label,
                htmlFor=component_id,
                style={
                    "display": "block",
                    "fontSize": "12px",
                    "fontWeight": "700",
                    "color": "rgba(11,18,32,0.75)",
                    "marginBottom": "6px",
                },
            ),
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "6px"},
                children=[
                    dcc.Input(
                        id=component_id,
                        type="number",
                        placeholder=placeholder,
                        inputMode="decimal",
                        style={
                            "flex": 1,
                            "borderRadius": "12px",
                            "border": "1px solid rgba(11,18,32,0.12)",
                            "padding": "10px 12px",
                            "fontSize": "14px",
                            "outline": "none",
                            "backgroundColor": "white",
                        },
                    ),
                    html.Button(
                        "ⓘ",
                        id=f"{component_id}-btn",
                        n_clicks=0,
                        style={
                            "border": "none",
                            "background": "none",
                            "cursor": "pointer",
                            "color": "#0d67df",
                            "fontWeight": "900",
                            "fontSize": "16px",
                        },
                    ),
                ],
            ),
            html.Div(
                info_text,
                id=info_div_id,
                style={
                    "display": "none",
                    "backgroundColor": "#f0f0f0",
                    "padding": "8px",
                    "borderRadius": "6px",
                    "marginTop": "4px",
                    "fontSize": "12px",
                },
            ),
        ],
    )

app = dash.Dash(__name__)

# --- Remove default white border + add segmented control styling ---
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body { height: 100%; margin: 0; padding: 0; }

            .segmented label {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 12px;
                border-radius: 12px;
                cursor: pointer;
                user-select: none;
                font-weight: 800;
                font-size: 12px;
                color: rgba(11,18,32,0.70);
                transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease, color 120ms ease;
            }

            .segmented label:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 18px rgba(0,0,0,0.08);
                background: rgba(255,255,255,0.55);
            }

            /* Hide the default radio circle */
            .segmented input[type="radio"] {
                display: none;
            }

            /* Selected label */
            .segmented label.is-selected {
                color: #ffffff;
                background: linear-gradient(135deg, #0d67df 0%, #003d99 100%);
                box-shadow: 0 12px 22px rgba(13,103,223,0.25);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
            // Add/remove 'is-selected' class based on checked input.
            // Runs on load and whenever Dash re-renders.
            function syncSegmented() {
                const root = document.querySelector('.segmented');
                if (!root) return;
                const labels = root.querySelectorAll('label');
                labels.forEach(label => {
                    const input = label.querySelector('input[type="radio"]');
                    if (!input) return;
                    if (input.checked) label.classList.add('is-selected');
                    else label.classList.remove('is-selected');
                });
            }
            window.addEventListener('load', syncSegmented);
            const obs = new MutationObserver(syncSegmented);
            obs.observe(document.body, { childList: true, subtree: true });
        </script>
    </body>
</html>
"""

# ---- Placeholder bar chart (8 bars) ----
parties = ["M", "L", "C", "KD", "S", "V", "MP", "SD"]
placeholder_values = [12, 8, 6, 4, 25, 7, 5, 14]

party_colors = {
    "V":  "#7a0d0d",  # dark red
    "S":  "#d81b3a",  # red
    "MP": "#78c850",  # light green
    "C":  "#2aa84a",  # green
    "L":  "#0a5bd3",  # blue
    "KD": "#1b2a8f",  # dark blue
    "M":  "#7fc6e8",  # light blue
    "SD": "#f2c230",  # yellow
}
bar_colors = [party_colors[p] for p in parties]

bar_fig = go.Figure(
    data=[
        go.Bar(
            x=parties,
            y=placeholder_values,
            marker=dict(color=bar_colors),
        )
    ]
)
bar_fig.update_layout(
    xaxis_title="Party",
    yaxis_title="Percentage of votes",
    margin=dict(l=30, r=30, t=30, b=30),
    height=420,
    # 4 % - line
    shapes=[  
        dict(
            type="line",
            x0=-0.5,     
            x1=7.5,       
            y0=4,         
            y1=4,        
            line=dict(
                color="red", 
                width=2, 
                dash="dash"  
            ),
        )
    ]
)

# ---- Layout ----
app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #0b1220 0%, #0f2b5b 40%, #0d67df 100%)",
        "padding": "28px",
        "fontFamily": "Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",
    },
    children=[
        html.Div(
            style={"maxWidth": "1100px", "margin": "0 auto"},
            children=[
                # Header
                html.Div(
                    style={"marginBottom": "18px", "color": "white"},
                    children=[
                        html.H1(
                            "Swedish Party Sentiment Predictor",
                            style={
                                "margin": "0 0 8px 0",
                                "fontSize": "32px",
                                "fontWeight": "800",
                                "letterSpacing": "0.2px",
                            },
                        ),
                        html.P(
                            "Fill in arbitrary values for these 7 socially relevant metrics and see how the Swedish party polls change.",
                            style={
                                "margin": "0",
                                "opacity": "0.9",
                                "fontSize": "14px",
                                "maxWidth": "850px",
                                "lineHeight": "1.5",
                            },
                        ),
                        html.P(
                            "Predictions are based on metrical data from SCB and public poll data.",
                            style={
                                "margin": "0",
                                "opacity": "0.9",
                                "fontSize": "14px",
                                "maxWidth": "850px",
                                "lineHeight": "1.5",
                            },
                        ),
                    ],
                ),

                # Card: Inputs
                html.Div(
                    style={
                        "backgroundColor": "rgba(255,255,255,0.92)",
                        "border": "1px solid rgba(255,255,255,0.18)",
                        "borderRadius": "18px",
                        "padding": "18px",
                        "boxShadow": "0 12px 35px rgba(0,0,0,0.25)",
                        "backdropFilter": "blur(6px)",
                        "marginBottom": "18px",
                    },
                    children=[
                        # Title + Random button on the same row
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "gap": "12px",
                                "flexWrap": "wrap",
                                "marginBottom": "12px",
                            },
                            children=[
                                html.H2(
                                    "Input metric values",
                                    style={
                                        "margin": "0",
                                        "fontSize": "18px",
                                        "fontWeight": "800",
                                        "color": "#0b1220",
                                    },
                                ),
                                html.Button(
                                    "Random",
                                    id="random-btn",
                                    n_clicks=0,
                                    style={
                                        "border": "none",
                                        "borderRadius": "12px",
                                        "padding": "8px 16px",
                                        "fontWeight": "700",
                                        "cursor": "pointer",
                                        "color": "white",
                                        "background": "linear-gradient(135deg, #0d67df 0%, #003d99 100%)",
                                    },
                                ),                                
                            ],
                        ),

                        # Grid with 7 inputs + submit as 8th field
                        html.Div(
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "repeat(auto-fit, minmax(240px, 1fr))",
                                "gap": "12px",
                                "alignItems": "end",
                            },
                            children=[
                                _metric_input("Consumer Price Index", "metric-1", "Insert value",
                                              "Measures changes in consumer prices over time using official CPI values. "
                                              "Typical index range: 250–420 (base year 1980 = 100)."),
                                _metric_input("Electricity Consumption", "metric-2", "Insert value",
                                              "Measures total monthly electricity consumption (GWh). "
                                              "Transit exports via Sweden are included. "
                                              "Typical index range: 5000–20000 GWh per month. "),
                                _metric_input("Government Debt", "metric-3", "Insert value",
                                              "Official measure of the Swedish government’s gross debt (million SEK). "
                                              "Typical index range: 1,000,000–1,300,000 million SEK"),
                                _metric_input("Money Supply Growth", "metric-4", "Insert value",
                                              "Measures the 12-month growth rate of the money supply (%) according to the selected monetary aggregate. "
                                              "Typical index range: -15-20%."),
                                _metric_input("Mortgage Interest Rate", "metric-5", "Insert value",
                                              "Average mortgage interest rate for new household loans (%) according to MFIs. "
                                              "Typical index range: 1–6%."),
                                _metric_input("Population", "metric-6", "Insert value",
                                              "Total population of Sweden by month. "
                                              "Typical index range: 10,300,000–10,500,000 people."),
                                _metric_input("Unemployment Rate", "metric-7", "Insert value",
                                              "Non-seasonally adjusted unemployment rate (%) for total population aged 15–74. "
                                              "Typical index range: 5–11%."),

                                # 8th "field": submit button
                                html.Div(
                                    style={"minWidth": 0},
                                    children=[
                                        html.Label(
                                            " ",
                                            style={
                                                "display": "block",
                                                "fontSize": "12px",
                                                "fontWeight": "700",
                                                "color": "rgba(11,18,32,0.75)",
                                                "marginBottom": "6px",
                                            },
                                        ),
                                        html.Button(
                                            "Submit",
                                            id="submit-btn",
                                            n_clicks=0,
                                            style={
                                                "width": "100%",
                                                "border": "none",
                                                "borderRadius": "14px",
                                                "padding": "12px 16px",
                                                "fontWeight": "800",
                                                "cursor": "pointer",
                                                "color": "white",
                                                "background": "linear-gradient(135deg, #0d67df 0%, #003d99 100%)",
                                                "boxShadow": "0 10px 18px rgba(13,103,223,0.25)",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # Card: Chart
                html.Div(
                    style={
                        "backgroundColor": "rgba(255,255,255,0.92)",
                        "border": "1px solid rgba(255,255,255,0.18)",
                        "borderRadius": "18px",
                        "padding": "18px",
                        "boxShadow": "0 12px 35px rgba(0,0,0,0.25)",
                        "backdropFilter": "blur(6px)",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "gap": "10px",
                                "flexWrap": "wrap",
                                "marginBottom": "10px",
                            },
                            children=[
                                html.H2(
                                    "Poll Results",
                                    style={
                                        "margin": "0",
                                        "fontSize": "18px",
                                        "fontWeight": "800",
                                        "color": "#0b1220",
                                    },
                                ),
                            ],
                        ),
                        dcc.Graph(
                            id="party-bar-chart",
                            figure=bar_fig,
                            config={"displayModeBar": False},
                            style={"width": "100%"},
                        ),
                    ],
                ),

                # Card: Model info
                html.Div(
                    style={
                        "backgroundColor": "rgba(255,255,255,0.92)",
                        "border": "1px solid rgba(255,255,255,0.18)",
                        "borderRadius": "18px",
                        "padding": "18px",
                        "boxShadow": "0 12px 35px rgba(0,0,0,0.25)",
                        "backdropFilter": "blur(6px)",
                        "width": "100%",
                        "marginTop": "18px", 
                        "marginBottom": "18px",
                    },
                    children=[
                        html.H2(
                            "Model Information",
                            style={
                                "margin": "0 0 10px 0",
                                "fontSize": "18px",
                                "fontWeight": "800",
                                "color": "#0b1220",
                            },
                        ),
                        html.Ul(
                            children=[
                                html.Li("Model: Random Forest"),
                                html.Li(f"MSE score on test data: {avg_mse:.3f}"),
                                html.Li(f"R² score on test data: {avg_r2:.3f}"),
                            ],
                            style={"margin": "0", "paddingLeft": "20px", "fontSize": "14px"},
                        ),
                    ],
                ),                

                # Footer
                html.Div(
                    style={
                        "marginTop": "16px",
                        "color": "rgba(255,255,255,0.85)",
                        "fontSize": "12px",
                        "textAlign": "center",
                    },
                    children="© Carolina Oker-Blom, Albin Kårlin, Sofie Melander",
                ),
            ],
        )
    ],
)

@app.callback(
    Output("party-bar-chart", "figure"),
    Input("submit-btn", "n_clicks"),
    State("metric-1", "value"),  # CPI
    State("metric-2", "value"),  # EC
    State("metric-3", "value"),  # GD
    State("metric-4", "value"),  # MSR
    State("metric-5", "value"),  # MIR
    State("metric-6", "value"),  # Pop
    State("metric-7", "value"),  # UR
    prevent_initial_call=True,
)

def predict(n_clicks, cpi, ec, gd, msr, mir, pop, ur):

    user_input = {
        'CPI': cpi,
        'EC': ec,
        'GD': gd,
        'MSR': msr,
        'MIR': mir,
        'Pop': pop,
        'UR': ur
        }
    
    predictions = predict_sentiment(user_input)
    
    # Keep party order consistent with chart
    parties = ["M", "L", "C", "KD", "S", "V", "MP", "SD"]
    values = [predictions[p] for p in parties]

    fig = go.Figure(
        data=[
            go.Bar(
                x=parties,
                y=values,
                marker=dict(color=[party_colors[p] for p in parties]),
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Party",
        yaxis_title="Predicted percentage",
        margin=dict(l=30, r=30, t=30, b=30),
        height=420,
        shapes=[  
            dict(
                type="line",
                x0=-0.5,     
                x1=7.5,       
                y0=4,         
                y1=4,        
                line=dict(
                    color="red", 
                    width=2, 
                    dash="dash"  
                ),
            )
        ]
    )

    return fig

for i in range(1, 8):  # Callback for all 7 metrics
    @app.callback(
        Output(f"metric-{i}-info", "style"),
        Input(f"metric-{i}-btn", "n_clicks"),
        State(f"metric-{i}-info", "style"),
        prevent_initial_call=True,
    )
    def toggle_info(n_clicks, current_style):
        if current_style["display"] == "none":
            current_style["display"] = "block"
        else:
            current_style["display"] = "none"
        return current_style

@app.callback(
    [Output(f"metric-{i}", "value") for i in range(1, 8)],
    Input("random-btn", "n_clicks"),
    prevent_initial_call=True
)

def randomize_metrics(n_clicks):
    values = []
    for i in range(1, 8):
        min_val, max_val = metric_ranges[f"metric-{i}"]
        if i in [2, 3, 6]:
            val = int(random.uniform(min_val, max_val))
        else:
            val = round(random.uniform(min_val, max_val), 2)
        values.append(val)
    return values

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=False, port=port, host=host)
