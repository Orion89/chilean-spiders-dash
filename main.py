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
                        dbc.Button(
                            "Descarga el afiche",
                            id="img-button",
                            color="success",
                            class_name="invisible",
                            type="button",
                        ),
                        dcc.Download(id="download-image"),
                        html.Br(),
                        # dbc.Card(
                        #     [
                        #        dbc.CardHeader(html.H4('¡Paciencia!', className='card-title text-center')),
                        #        dbc.CardBody(
                        #            [
                        #                html.P('Puede que la primera predicción cuando se entra al sitio tarde varios segundos.', className='card-text')
                        #            ]
                        #        )
                        #     ],
                        #     id='wait-msg',
                        #     color='warning',
                        #     class_name='m-1 shadow-sm'
                        # )
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
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H5("Consideraciones", className="card-title")
                            ),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "El algoritmo fue ajustado usando fotografías de sólo 51 clases, "
                                        "siendo este último término usado en forma general para distintos conceptos: "
                                        "Orden, Familia, género y especie.",
                                        className="card-text",
                                    ),
                                    html.P(
                                        "El modelo entregará un resultado aún cuando las fotografías no correspondan a arácnidos.",
                                        className="card-text",
                                    ),
                                    html.P(
                                        "Por lo anterior, cualquier predicción realizada por el modelo al enviar una fotografía "
                                        "estará limitada al alcance de las clases usadas en el ajuste.",
                                        className="card-text text-warning",
                                    ),
                                ],
                            ),
                        ],
                        className="m-2 mt-2 shadow-sm",
                    ),
                    width={"size": 4},
                    md={"size": 3, "offset": 1, "order": "first"},
                    sm={"size": 10, "offset": 1, "order": "first"},
                    xs={"size": 10, "offset": 1, "order": "first"},
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H5(
                                    "Clases de ajuste del algoritmo",
                                    className="card-title",
                                )
                            ),
                            dbc.CardBody(
                                html.P(
                                    ", ".join(
                                        [
                                            name.replace("_", "")
                                            for name in spiders_classes["train_classes"]
                                            if name != not_used_class_names
                                        ]
                                    ),
                                    className="card-text",
                                )
                            ),
                        ],
                        className="m-2 mt-2 shadow-sm",
                    ),
                    width={"size": 4},
                    md={"size": 4, "offset": 0, "order": 2},
                    sm={"size": 10, "offset": 1, "order": 2},
                    xs={"size": 10, "offset": 1, "order": 2},
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H5("Enlaces externos", className="card-title")
                                ),
                                dbc.CardBody(
                                    [
                                        html.A(
                                            "Grupo de Facebook de Arañas de Chile",
                                            disable_n_clicks=True,
                                            href="https://www.facebook.com/groups/aranasdechile",
                                            className="d-sm-block",
                                        ),
                                        html.A(
                                            "Instagram Arañas de Chile",
                                            disable_n_clicks=True,
                                            href="https://www.instagram.com/aranas_de_chile/",
                                            className="d-sm-block",
                                        ),
                                        html.A(
                                            "Grupo de Facebook de Tarántulas de Chile",
                                            disable_n_clicks=True,
                                            href="https://www.facebook.com/groups/276206972846798",
                                            className="d-sm-block",
                                        ),
                                        html.A(
                                            "Guía de Tarántulas Chilenas",
                                            disable_n_clicks=True,
                                            href="https://tarantulas-chilenas.wixsite.com/home",
                                            className="d-sm-block",
                                        ),
                                    ]
                                ),
                            ],
                            className="m-2 mt-2 shadow-sm",
                        )
                    ],
                    md={"size": 3, "offset": 0, "order": "last"},
                    sm={"size": 10, "offset": 1, "order": "last"},
                    xs={"size": 10, "offset": 1, "order": "last"},
                ),
            ]
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
    Output("result-container", "children"),  # Ahora actualizamos todo el contenedor
    Output("imgs-idx-store", "data"),
    Output("img-button", "class_name"),
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

                # --- NUEVA LÓGICA: Construir la tarjeta de resultado ---
                file_name = utils.infographics_dict.get(nearest_neighbors, None)
                download_button_class_name = (
                    "visible d-grid gap-2 col-6 mx-auto shadow"
                    if file_name
                    else "invisible"
                )

                # Determinar qué imagen mostrar (reutilizando tu lógica de refresh_infographic)
                if file_name:
                    img_src = str(infographics_path / file_name)
                else:
                    img_src = str(infographics_path / "no_afiche.png")

                result_card = dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H4(
                                f"Sugerencia de identificación: {nearest_neighbors}",
                                className="card-title text-white",
                            ),
                            className="bg-success",
                        ),
                        dbc.CardBody(
                            [
                                dbc.CardImg(src=img_src, id="info-img"),
                                dbc.CardFooter(
                                    html.P(
                                        "Todos los créditos al equipo de Arañas de Chile detallado en la parte inferior del afiche.",
                                        className="card-text mb-0",
                                    ),
                                    className="mt-2",
                                ),
                            ]
                        ),
                    ],
                    className="m-1 shadow-sm",
                )

                return (
                    result_card,
                    response_dict["nearest_imgs_idx"],
                    download_button_class_name,
                )
            else:
                # Manejo de error: Archivo no válido
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
                    dbc.CardBody(
                        html.P(
                            "Hubo un problema al procesar la imagen, vuelve a intentar con un archivo de imagen válido."
                        )
                    ),
                ],
                className="m-1 shadow-sm",
            )
            return error_card, no_update, no_update

    else:
        # Si no hay contenido (carga inicial), devolvemos el Empty State
        return initial_empty_state(), no_update, "invisible"


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
    State("info-img-title", "children"),
    prevent_initial_call=True,
)
def download_infographic(n_clicks, pred):
    # 'Afiche aleatorio'
    if "Sugerencia de clase:" in pred:
        first_pred = pred.partition(": ")[2]
        file_name = utils.infographics_dict.get(first_pred, None)
        if file_name:
            path_file = infographics_path / file_name
            return dcc.send_file(path_file)
        else:
            no_update
    else:
        no_update


if __name__ == "__main__":
    app.run(debug=False, port="9000")
