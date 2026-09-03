import base64
import json
import os
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import dash
import dash_bootstrap_components as dbc
import plotly
import requests
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
from flask import request
from sqlalchemy import text

from components.classes_accordion import render_classes_accordion
from components.upload_component import upload_component
from utils import utils

API = os.environ["API_URL"]  # 'http://127.0.0.1:8000'
api_upload_image = "/upload_img/"
api_get_classes = "/get_train_classes/"
api_get_pred_imgs = "/send_nearest_imgs/"

infographics_path = Path("./static/afiches/")
spiders_classes = json.loads(requests.get(urljoin(API, api_get_classes)).text)
not_used_class_names = "canis spider"

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SIMPLEX,
        dbc.icons.BOOTSTRAP,
    ],  # https://www.nelsontang.com/blog/2022-06-02-dash-tips
    title="Identifica esa araña",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    suppress_callback_exceptions=True,
)

server = app.server


def initial_empty_state():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Img(
                            src="/static/ilustraciones/spider-web-1.svg",
                            style={
                                "height": "120px",
                                "opacity": "0.6",
                            },
                            className="mb-3",
                        ),
                        html.H4(
                            "Sin imagen seleccionada",
                            className="mt-3 text-secondary fw-bold",
                        ),
                        html.P(
                            "Sube una fotografía nítida (de preferencia vista ventral) de un arácnido encontrado en Chile para obtener su clasificación taxonómica y afiche educativo.",
                            className="text-muted mx-auto",
                            style={"maxWidth": "500px"},
                        ),
                    ],
                    className="text-center py-5",
                )
            ]
        ),
        className="shadow-sm border-dashed",
        id="empty-state-card",
    )


app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("¿Qué araña es?", className="fw-bolder text-center"), width=12
            ),
            className="m-2",
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H2(
                        "Identificador de arácnidos de Chile",
                        className="fw-bolder text-center",
                    )
                ],
                width=12,
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        id="loading-upload",
                        type="circle",
                        color="#0d6efd",
                        children=upload_component,
                    ),
                    width={"size": 10, "offset": 1},
                    md={"size": 10, "offset": 1},
                    xs={"size": 12, "offset": 0},
                )
            ],
            justify="around",
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardImg(id="img-1", class_name="m-1 p-1 shadow-sm"),
                                dbc.CardImg(id="img-2", class_name="m-1 p-1 shadow-sm"),
                                dbc.CardFooter(
                                    html.P(
                                        "Créditos de las fotografías a quien corresponda.",
                                        className="card-text",
                                    )
                                ),
                            ],
                            id="img-container-1",
                            class_name="m-1 invisible",
                        ),
                    ],
                    width={"size": 2, "offset": 0},
                    lg={
                        "size": 2,
                        "offset": 0,
                        # 'order': 'first'
                    },
                    md={"size": 2, "offset": 0, "order": "first"},  # '2'
                    sm={"size": 8, "offset": 2, "order": "2"},
                    xs={"size": 8, "offset": 2, "order": "2"},
                ),
                dbc.Col(
                    html.Div(
                        id="result-container",
                        children=[initial_empty_state()],  # Llamamos a la función aquí
                        className="m-1 primary",
                    ),
                    width={"size": 8, "offset": 0},
                    lg={"size": 8, "offset": 0},
                    md={"size": 8, "offset": 0, "order": 2},
                    sm={"size": 12, "offset": 0, "order": "first"},
                    xs={"size": 12, "offset": 0, "order": "first"},
                ),
                dcc.Store(id="imgs-idx-store"),
                dcc.Store(id="pred-store"),  # Guardará la predicción limpia
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4(
                                        "¡Paciencia!",
                                        id="warning-title",
                                        className="card-title text-center",
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "Puede que el primer uso (envío de fotografía y sugerencia de clase) que se realice tarde varios segundos.",
                                            id="warning-text",
                                            className="card-text",
                                        )
                                    ]
                                ),
                            ],
                            id="warning-msg",
                            color="warning",
                            class_name="m-1 shadow-sm",
                        ),
                        html.Br(),
                    ],
                    lg={
                        "size": 2,
                        "offset": 0,
                        # 'order': 'last'
                    },
                    md={"size": 2, "offset": 0, "order": "last"},
                    sm={"size": 8, "offset": 2, "order": "last"},
                    xs={"size": 8, "offset": 2, "order": "last"},
                ),
            ],
            align="start",
        ),
        # -------------------------------------------------------------
        # NUEVA ZONA INFERIOR: Acordeón + Contexto (Consideraciones y Enlaces)
        # -------------------------------------------------------------
        dbc.Row(
            dbc.Col(render_classes_accordion(spiders_classes), width=12),
            className="mx-2",
        ),
        dbc.Row(
            [
                # Tarjeta de Consideraciones (Izquierda)
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.I(className="bi bi-shield-exclamation me-2"),
                                    "Consideraciones del Algoritmo",
                                ],
                                className="fw-bold bg-light",
                            ),
                            dbc.CardBody(
                                [
                                    html.Ul(
                                        [
                                            html.Li(
                                                "El algoritmo fue ajustado usando fotografías de sólo 51 clases (Orden, Familia, Género y Especie).",
                                                className="mb-2",
                                            ),
                                            html.Li(
                                                "El modelo entregará un resultado aproximado aún cuando las fotografías no correspondan a arácnidos.",
                                                className="mb-2",
                                            ),
                                            html.Li(
                                                "Cualquier predicción estará limitada estrictamente al catálogo de clases registradas.",
                                                className="text-danger fw-bold",
                                            ),
                                        ],
                                        className="card-text small mb-0",
                                    )
                                ],
                            ),
                        ],
                        className="shadow-sm h-100",
                    ),
                    md=6,
                    xs=12,
                    className="mb-3",
                ),
                # Tarjeta de Enlaces Externos (Derecha)
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.I(className="bi bi-link-45deg me-2"),
                                    "Enlaces Externos de Interés",
                                ],
                                className="fw-bold bg-light",
                            ),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            html.A(
                                                [
                                                    html.I(
                                                        className="bi bi-facebook text-primary me-2"
                                                    ),
                                                    "Grupo de Facebook de Arañas de Chile",
                                                ],
                                                href="https://www.facebook.com/groups/aranasdechile",
                                                target="_blank",
                                                className="d-block mb-3 text-decoration-none text-dark",
                                            ),
                                            html.A(
                                                [
                                                    html.I(
                                                        className="bi bi-instagram text-danger me-2"
                                                    ),
                                                    "Instagram Arañas de Chile",
                                                ],
                                                href="https://www.instagram.com/aranas_de_chile/",
                                                target="_blank",
                                                className="d-block mb-3 text-decoration-none text-dark",
                                            ),
                                            html.A(
                                                [
                                                    html.I(
                                                        className="bi bi-facebook text-primary me-2"
                                                    ),
                                                    "Grupo de Facebook de Tarántulas de Chile",
                                                ],
                                                href="https://www.facebook.com/groups/276206972846798",
                                                target="_blank",
                                                className="d-block mb-3 text-decoration-none text-dark",
                                            ),
                                            html.A(
                                                [
                                                    html.I(
                                                        className="bi bi-book text-success me-2"
                                                    ),
                                                    "Guía de Tarántulas Chilenas",
                                                ],
                                                href="https://tarantulas-chilenas.wixsite.com/home",
                                                target="_blank",
                                                className="d-block text-decoration-none text-dark",
                                            ),
                                        ]
                                    )
                                ]
                            ),
                        ],
                        className="shadow-sm h-100",
                    ),
                    md=6,
                    xs=12,
                    className="mb-3",
                ),
            ],
            className="mx-2 mb-4 align-items-stretch",  # Alinea las tarjetas para que tengan la misma altura
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # html.Div(id='user-info', className='invisible m-0'),
                        dbc.Card(
                            [
                                dbc.CardFooter(
                                    [
                                        html.P(
                                            [
                                                html.A(
                                                    children=[
                                                        html.I(className="bi bi-github")
                                                    ],
                                                    disable_n_clicks=True,
                                                    href="https://github.com/Orion89",
                                                    title="GitHub profile",
                                                ),
                                                " ",
                                                html.A(
                                                    children=[
                                                        html.I(
                                                            className="bi bi-linkedin"
                                                        )
                                                    ],
                                                    disable_n_clicks=True,
                                                    href="https://www.linkedin.com/in/leonardo-molina-v-68a601183/",
                                                    title="LinkedIn profile",
                                                ),
                                                " 2023 Leonardo Molina V.",
                                            ]
                                        ),
                                        html.P(
                                            "Proyecto académico. El autor no se hace responsable del mal uso del contenido o predicciones."
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                    class_name="mt-4",
                    width={"size": 12},
                )
            ],
            align="center",
            class_name="text-end",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("result-container", "children"),
    Output("imgs-idx-store", "data"),
    Output("pred-store", "data"),
    Input("pic-upload-1", "contents"),
)
def send_image(contents):
    if contents is not None:
        content_type, content_string = contents.split(",")
        n_neighbors = 1

        try:
            if "image" in content_type:
                decoded = base64.b64decode(content_string)
                files = {"file": decoded}
                response = requests.post(urljoin(API, api_upload_image), files=files)
                response_dict = json.loads(response.text)

                nearest_neighbors = ", ".join(
                    [name for name in response_dict["nearest_neighbors"][:n_neighbors]]
                )
                file_name = utils.infographics_dict.get(nearest_neighbors, None)
                if file_name:
                    img_src = str(infographics_path / file_name)
                    # Si hay afiche, creamos el botón de descarga aquí mismo
                    download_btn = html.Div(
                        [
                            dbc.Button(
                                [
                                    html.I(className="bi bi-download me-2"),
                                    "Descargar afiche",
                                ],
                                id="img-button",
                                color="success",
                                className="w-100 shadow-sm",
                            ),
                            dcc.Download(id="download-image"),
                        ],
                        className="mt-3",
                    )
                else:
                    img_src = str(infographics_path / "no_afiche.png")
                    download_btn = html.Div()  # Vacío si no hay afiche

                # Construir la tarjeta de resultado
                result_card = dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H4(
                                f"Sugerencia de identificación: {nearest_neighbors}",
                                className="card-title text-white mb-0",
                            ),
                            className="bg-success",
                        ),
                        dbc.CardBody(
                            [
                                dbc.CardImg(src=img_src, id="info-img"),
                                download_btn,  # Insertamos el botón debajo de la imagen
                            ]
                        ),
                        dbc.CardFooter(
                            html.P(
                                "Todos los créditos al equipo de Arañas de Chile detallado en la parte inferior del afiche.",
                                className="card-text mb-0 text-muted small",
                            ),
                        ),
                    ],
                    className="m-1 shadow-sm",
                )

                # Retornamos la tarjeta, la ID de imágenes, y la PREDICCIÓN LIMPIA para el Store
                return result_card, response_dict["nearest_imgs_idx"], nearest_neighbors

            # ... (Manejo de errores `else` y `except` sin cambios, pero retornando `no_update` para el pred-store) ...
            else:
                error_card = dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H4("Error", className="card-title text-white"),
                            className="bg-danger",
                        ),
                        dbc.CardBody(html.P("Tipo de archivo no válido.")),
                    ],
                    className="m-1 shadow-sm",
                )
                return error_card, no_update, no_update
        except Exception as e:
            print(e)
            error_card = dbc.Card(
                [
                    dbc.CardHeader(
                        html.H4("Error", className="card-title text-white"),
                        className="bg-danger",
                    ),
                    dbc.CardBody(html.P("Hubo un problema al procesar la imagen.")),
                ],
                className="m-1 shadow-sm",
            )
            return error_card, no_update, no_update
    else:
        return initial_empty_state(), no_update, no_update


about_classifications_text = "Tener presente que la clasificación puede ser desacertada. Considerar con precaución."
about_classifications_title = "Es importante"


@app.callback(
    Output("img-1", "src"),
    Output("img-2", "src"),
    Output("img-container-1", "class_name"),
    Output("warning-title", "children"),
    Output("warning-text", "children"),
    Input("imgs-idx-store", "modified_timestamp"),
    State("imgs-idx-store", "data"),
)
def get_nearest_imgs(timestamp, data):
    if data:
        nearest_imgs_list = []
        for num in data[1:3]:
            body = {"imgs_idxs": num}
            response = requests.post(urljoin(API, api_get_pred_imgs), json=body)
            img_decoded = "data:image/png;base64," + base64.b64encode(
                response.content
            ).decode("utf-8")
            nearest_imgs_list.append(img_decoded)
        # print(response.content)
        return (
            nearest_imgs_list[0],
            nearest_imgs_list[1],
            "m-1 visible shadow-sm",
            about_classifications_title,
            about_classifications_text,
        )
    else:
        return no_update, no_update, no_update, no_update, no_update


@app.callback(
    Output("download-image", "data"),
    Input("img-button", "n_clicks"),
    State("pred-store", "data"),
    prevent_initial_call=True,
)
def download_infographic(n_clicks, pred_name):
    if pred_name:
        file_name = utils.infographics_dict.get(pred_name, None)
        if file_name:
            path_file = infographics_path / file_name
            return dcc.send_file(path_file)
    return no_update


if __name__ == "__main__":
    app.run(debug=False, port="9000")
