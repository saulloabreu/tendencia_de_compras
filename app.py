from app import *
from dash_bootstrap_templates import ThemeSwitchAIO
import dash_bootstrap_components as dbc
import dash

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

app = dash.Dash(__name__, 
                # external_stylesheets=FONT_AWESOME, 
                external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True, 
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                )

app.config.suppress_callback_exceptions = True
app.scripts.config.serve_localy = True
server = app.server