import dash
import dash_bootstrap_components as dbc
from dash import html, page_container

# Initialize the Dash app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://scontent.fsgn21-1.fna.fbcdn.net/v/t39.30808-6/230984148_150696287177804_977364881514081647_n.png?_nc_cat=107&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=7Sm1heTp5_QQ7kNvgH20GJ3&_nc_ht=scontent.fsgn21-1.fna&oh=00_AYBFYge9aGAoTW7NDm6-hBsDAV39-P_EUNfBU-hKXdmbKA&oe=66FD8C54"

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
            label="Production",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Daily Report", href="/warehouse_daily"),
                
            ],
            nav=True,
            in_navbar=True,
            label="Wareshoue",
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
