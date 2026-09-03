import dash_bootstrap_components as dbc
from dash import html


def render_classes_accordion(spiders_classes_dict):
    not_used_class_names = "canis spider"

    class_badges = [
        dbc.Badge(
            name.replace("_", " ").title(),
            color="secondary",
            pill=True,
            className="me-1 mb-1 text-wrap fw-normal px-2 py-1",
        )
        for name in spiders_classes_dict.get("train_classes", [])
        if name != not_used_class_names
    ]
    accordion_title = (
        f"Ver las {len(class_badges)} clases taxonómicas soportadas por el modelo"
    )

    return dbc.Accordion(
        [
            dbc.AccordionItem(
                html.Div(class_badges, className="d-flex flex-wrap gap-1 p-2"),
                title=accordion_title,
                item_id="item-1",
            )
        ],
        active_item=None,  # Inicia cerrado
        className="shadow-sm mb-4",
    )
