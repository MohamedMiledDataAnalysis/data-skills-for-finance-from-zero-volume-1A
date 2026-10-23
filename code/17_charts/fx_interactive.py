import pandas as pd
import plotly.express as px

fx = pd.read_csv("data/csv/fx_rates.csv", parse_dates=["rate_date"])

fig = px.line(
    fx, x="rate_date", y="rate_per_gbp", color="currency",
    color_discrete_map={"EUR": "#1F2A44", "USD": "#2E7D7A"},
    labels={"rate_date": "Date",
            "rate_per_gbp": "Units per £1",
            "currency": "Currency"},
    title="EUR and USD per £1, 2025",
)
fig.update_traces(
    hovertemplate="%{x|%d %b %Y}<br>%{y:.4f} per £1")
fig.update_layout(template="simple_white",
                  hovermode="x unified",
                  font_family="Arial", title_x=0.02)
fig.write_html("output/ch17_fx_interactive.html")
print("Saved output/ch17_fx_interactive.html")

try:
    fig.write_image("output/ch17_fx_interactive.png",
                    width=900, height=500, scale=2)
    print("Saved output/ch17_fx_interactive.png")
except Exception as error:
    print("Static export failed:", type(error).__name__)
