import dash
from dash import html, dcc
import plotly.graph_objects as go
from threading import Timer
import webbrowser

from src.predict_sentiment import predict_sentiment

# Server constants
port = 8050
host = "localhost"


def open_browser(host=host, port=port) -> None:
    """
    Call to Webbrowser to open server when running
    """
    webbrowser.open_new(f"http://{host}:{port}")


def _metric_input(label: str, component_id: str, placeholder: str):
    """Helper for a clean, consistent input card."""
    return html.Div(
        style={
            "minWidth": 0,  # important so CSS grid can shrink properly
            "maxWidth": "60%",
        },
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
            dcc.Input(
                id=component_id,
                type="number",
                placeholder=placeholder,
                inputMode="decimal",
                style={
                    "width": "100%",
                    "boxSizing": "border-box",
                    "borderRadius": "12px",
                    "border": "1px solid rgba(11,18,32,0.12)",
                    "padding": "10px 12px",
                    "fontSize": "14px",
                    "outline": "none",
                    "backgroundColor": "white",
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

            /* --- Segmented control styling for model-choice --- */
            .segmented {
                display: inline-flex;
                gap: 6px;
                padding: 6px;
                border-radius: 14px;
                background: rgba(11,18,32,0.06);
                border: 1px solid rgba(11,18,32,0.10);
            }

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
                        # Title + model on the same row
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
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                    },
                                    children=[
                                        html.Div(
                                            "Model",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "800",
                                                "color": "rgba(11,18,32,0.75)",
                                            },
                                        ),
                                        dcc.RadioItems(
                                            id="model-choice",
                                            className="segmented",
                                            options=[
                                                {"label": "Linear Regression", "value": "linreg"},
                                                {"label": "Random Forest", "value": "rf"},
                                            ],
                                            value="linreg",
                                            inline=True,
                                        ),
                                    ],
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
                                _metric_input("Consumer Price Index", "metric-1", "To be implemented"),
                                _metric_input("Electricity Consumption", "metric-2", "To be implemented"),
                                _metric_input("Government Debt", "metric-3", "To be implemented"),
                                _metric_input("Money Supply Growth", "metric-4", "To be implemented"),
                                _metric_input("Mortgage Interest Rate", "metric-5", "To be implemented"),
                                _metric_input("Population", "metric-6", "To be implemented"),
                                _metric_input("Unemployment Rate", "metric-7", "To be implemented"),

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


def predict(cpi, ec, gd, msr, mir, pop, ur):

    user_input = {
        'CPI': cpi,
        'EC': ec,
        'GD': gd,
        'MSR': msr,
        'MIR': mir,
        'Pop': pop,
        'UR': ur
        }
    
    preds = predict_sentiment(user_input)
    
    return None

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=False, port=port, host=host)
