import dash_bootstrap_components as dbc
from dash import dcc, html

upload_component = dcc.Upload(
    id="pic-upload-1",
    children=html.Div(
        [
            html.I(className="bi bi-cloud-arrow-up text-primary display-4 mb-2"),
            html.H6("Arrastra tu fotografía aquí", className="fw-bold mb-1"),
            html.Small(
                "O haz clic para explorar tus archivos (JPG, PNG)",
                className="text-muted d-block mb-2",
            ),
            dbc.Badge(
                "Consejo: Vista ventral y buena iluminación",
                color="light",
                text_color="dark",
                className="border",
            ),
        ],
        className="py-4 text-center",
    ),
    multiple=False,
    accept="image/*",
    max_size=4e7,
    style={
        "width": "100%",
        "borderWidth": "2px",
        "borderStyle": "dashed",
        "borderColor": "#0d6efd",
        "borderRadius": "12px",
        "backgroundColor": "#f8f9fa",
        "cursor": "pointer",
        "transition": "all 0.3s ease",
    },
)
