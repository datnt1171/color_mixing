import dash
import dash_bootstrap_components as dbc
from dash import html, page_container

# Initialize the Dash app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "/assets/logo.png"

# Main Navbar for department selection

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("TE-1 Dashboard", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
            href="/",
            style={"textDecoration": "none"},
        ),

        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Daily Report", href="/color_mixing_daily"),
                dbc.DropdownMenuItem("Weekly Report", href="/color_mixing_weekly"),
                dbc.DropdownMenuItem("QC Loss Rate", href="/color_mixing_qc")
            ],
            nav=True,
            in_navbar=True,
            label="Color Mixing",
        ),
        
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Weekly Report", href="/warehouse_weekly"),
                dbc.DropdownMenuItem("Drilldown", href="/warehouse_drilldown"),
                
            ],
            nav=True,
            in_navbar=True,
            label="Wareshoue",
        ),
        
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Weekly Report", disabled=True, href="#"),
                dbc.DropdownMenuItem("Drilldown", disabled=True, href="#"),
                
            ],
            nav=True,
            in_navbar=True,
            label="Sales",
        ),
        
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Weekly Report",disabled=True, href="#"),
                dbc.DropdownMenuItem("Drilldown", disabled=True, href="#"),
                
            ],
            nav=True,
            in_navbar=True,
            label="Production",
        ),
        
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Weekly Report", disabled=True, href="#"),
                dbc.DropdownMenuItem("Drilldown", disabled=True, href="#"),
                
            ],
            nav=True,
            in_navbar=False,
            label="RD",
        ),
        
    ]),
    sticky="top"
)



# Main layout with navbar and page container
app.layout = html.Div([
    navbar,
    page_container  # Dynamically renders the page content based on URL
])

if __name__ == "__main__":
    app.run_server(debug=True)
