import base64
from datetime import datetime
import json
import os
from pathlib import Path
import random
from urllib.parse import urljoin
# from config.db import engine
from utils import utils

import plotly
import dash
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import request
from sqlalchemy import text

# from ip2geotools.databases.noncommercial import DbIpCity
import requests


API = os.environ['API_URL'] # 'http://127.0.0.1:8000' 
api_upload_image = '/upload_img/'
api_get_classes = '/get_train_classes/'
api_get_pred_imgs = '/send_nearest_imgs/'

infographics_path = Path('./static/afiches/')
spiders_classes = json.loads(requests.get(urljoin(API, api_get_classes)).text)
not_used_class_names = 'canis spider'

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SIMPLEX, dbc.icons.BOOTSTRAP], # https://www.nelsontang.com/blog/2022-06-02-dash-tips
                title='Identifica esa araña',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = app.server

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("¿Qué araña es?", className='fw-bolder text-center'),
                width=12
            ),
            className='m-2'
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H2(
                        "Identificador de arácnidos de Chile",
                        className='fw-bolder text-center'
                    )
                ],
                width=12
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(
                        id='pic-upload-1',
                        children=[
                            # dbc.Card(
                            #     dbc.CardLink(
                            #         'Arrastra la fotografía acá o haz click para seleciconar el archivo',
                            #         href='#'
                            #     )
                            # )
                            html.Div(
                                [
                                    # "Arrastra la fotografía acá o ",
                                    # html.P('Arrastra la fotografía acá o'),
                                    html.I(
                                        className="bi bi-cloud-upload text-secondary"
                                    ),
                                    html.A(
                                        'Arrastra la foto acá o haz click (toca) para tomar una foto (o seleccionar desde el dispositivo)',
                                        style={
                                            'overflowWrap': 'breakWord',
                                            'cursor': 'pointer',
                                            'wordBreak': 'breakAll',
                                            'verticalAlign': 'sub',
                                            'textDecoration': 'none',
                                            'fontWeight': 'bold'
                                        },
                                        className='mt-3 mb-2 text-info font-weight-bold'
                                    ),
                                ],
                                className='mt-3 mb-2 font-weight-bold'
                            )
                        ],
                        multiple=False,
                        accept='image/*',
                        max_size=4e7,
                        style={
                            'width': '90%',
                            'height': '90px',
                            'lineHeight': 'normal',
                            'borderWidth': '2px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px',
                        },
                    ),
                    width={'size': 10, 'offset': 1},
                    md={
                        'size': 10,
                        'offset': 1
                    },
                    xs={
                        'size': 12,
                        'offset': 0
                    }
                )
            ],
            justify='around'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Se recomienda fotografía ventral. La imagen debe ser lo más cercana y nítida posible para sugerencias más precisas.',
                               className='text-center')
                    ],
                    width={'size': 12, 'offset': 0},
                )
            ],
            justify='center'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    id='img-1',
                                    class_name='m-1 p-1 shadow-sm'
                                ),
                                dbc.CardImg(
                                    id='img-2',
                                    class_name='m-1 p-1 shadow-sm'
                                ),
                                dbc.CardFooter(
                                    html.P('Créditos de las fotografías a quien corresponda.', className='card-text')
                                )
                            ],
                            id='img-container-1',
                            class_name='m-1 invisible'
                        ),
                    ],
                    width={'size': 2, 'offset': 0},
                    lg={
                        'size': 2,
                        'offset': 0,
                        # 'order': 'first'
                    },
                    md={
                        'size': 2,
                        'offset': 0,
                        'order': 'first' # '2'
                    },
                    sm={
                        'size': 8,
                        'offset': 2,
                        'order': '2'
                    },
                    xs={
                        'size': 8,
                        'offset': 2,
                        'order': '2'
                    }
                    
                ),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                            dbc.Spinner(
                                                    html.H4(
                                                        'Afiche aleatorio',
                                                        id='info-img-title',
                                                        className='card-title'
                                                    ),
                                                    type='grow',
                                                    color='secondary'
                                                )
                                        ),
                                    dbc.CardBody(
                                        [
                                            #  html.P(
                                            #     id="cls-predictions",
                                            #     className='fw-bolder'
                                            # ),
                                            dbc.Spinner(
                                                dbc.CardImg(
                                                    src="/static/afiches/familia_salticidae.jpg",
                                                    id='info-img'
                                                ),
                                                type='border',
                                                color='secondary'
                                            ),
                                    dbc.CardFooter(
                                        [
                                            html.P(
                                                "Todos los créditos al equipo de Arañas de Chile detallado en la parte inferior del afiche.", className='card-text'),
                                            dcc.Store(id='imgs-idx-store') # html.P(id='imgs-idxs', className='invisible')
                                        ],
                                        className='mt-2 mb-1'
                                    )
                                        ]
                                    ),
                                    
                                ],
                                id='main-card',
                                class_name='m-1 shadow-sm'
                            )
                        ],
                        className='m-1 primary'
                    ),
                    width={'size': 8, 'offset': 0},
                    lg={
                        'size': 8,
                        'offset': 0,
                        # 'order': 'first'
                    },
                    md={
                        'size': 8,
                        'offset': 0,
                        'order': 2 # first'
                    },
                    sm={
                        'size': 12,
                        'offset': 0,
                        'order': 'first'
                    },
                    xs={
                        'size': 12,
                        'offset': 0,
                        'order': 'first'
                    }
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                               dbc.CardHeader(html.H4('¡Paciencia!',
                                                      id='warning-title',
                                                      className='card-title text-center')),
                               dbc.CardBody(
                                   [
                                       html.P('Puede que el primer uso (envío de fotografía y sugerencia de clase) que se realice tarde varios segundos.',
                                              id='warning-text',
                                              className='card-text')
                                   ]
                               ) 
                            ],
                            id='warning-msg',
                            color='warning',
                            class_name='m-1 shadow-sm'
                        ),
                        html.Br(),
                        dbc.Button(
                            'Descarga el afiche',
                            id='img-button',
                            color='success',
                            class_name='invisible',
                            type='button',
                        ),
                        dcc.Download(
                            id='download-image'
                        ),
                        html.Br()
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
                        'size': 2,
                        'offset': 0,
                        # 'order': 'last'
                    },
                    md={
                        'size': 2,
                        'offset': 0,
                        'order': 'last'
                    },
                    sm={
                        'size': 8,
                        'offset': 2,
                        'order': 'last'
                    },
                    xs={
                        'size': 8,
                        'offset': 2,
                        'order': 'last'
                    },
                )
            ],
            align='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.H5('Consideraciones', className='card-title')),
                            dbc.CardBody(
                            [
                                html.P(
                                    'El algoritmo fue ajustado usando fotografías de sólo 51 clases, '
                                    'siendo este último término usado en forma general para distintos conceptos: '
                                    'Orden, Familia, género y especie.',
                                    className='card-text'
                                ),
                                html.P(
                                    'El modelo entregará un resultado aún cuando las fotografías no correspondan a arácnidos.',
                                    className='card-text'
                                ),
                                html.P(
                                    'Por lo anterior, cualquier predicción realizada por el modelo al enviar una fotografía '
                                    'estará limitada al alcance de las clases usadas en el ajuste.',
                                    className='card-text text-warning'
                                )
                            ],
                        )   
                        ],
                        className='m-2 mt-2 shadow-sm'
                    ),
                    width={'size': 4},
                    md={
                        'size': 3,
                        'offset': 1,
                        'order': 'first'
                    },
                    sm={
                        'size': 10,
                        'offset': 1,
                        'order': 'first'
                    },
                    xs={
                        'size': 10,
                        'offset': 1,
                        'order': 'first'
                    }
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.H5('Clases de ajuste del algoritmo', className='card-title')),
                            dbc.CardBody(
                                html.P(
                                    ", ".join([name.replace('_', '') for name in spiders_classes['train_classes'] if name != not_used_class_names]),
                                    className='card-text'
                                )
                            )
                        ],
                        className='m-2 mt-2 shadow-sm'
                    
                    ),
                    width={'size': 4},
                    md={
                        'size': 4,
                        'offset': 0,
                        'order': 2
                    },
                    sm={
                        'size': 10,
                        'offset': 1,
                        'order': 2
                    },
                    xs={
                        'size': 10,
                        'offset': 1,
                        'order': 2
                    }
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H5('Enlaces externos', className='card-title')),
                                dbc.CardBody(
                                    [
                                        html.A('Grupo de Facebook de Arañas de Chile',
                                                disable_n_clicks=True,
                                                href='https://www.facebook.com/groups/aranasdechile',
                                                className='d-sm-block'),
                                        html.A('Instagram Arañas de Chile',
                                               disable_n_clicks=True,
                                               href='https://www.instagram.com/aranas_de_chile/',
                                               className='d-sm-block'),
                                        html.A('Grupo de Facebook de Tarántulas de Chile',
                                               disable_n_clicks=True,
                                               href='https://www.facebook.com/groups/276206972846798',
                                               className='d-sm-block'),
                                        html.A('Guía de Tarántulas Chilenas',
                                               disable_n_clicks=True,
                                               href='https://tarantulas-chilenas.wixsite.com/home',
                                               className='d-sm-block')
                                    ]
                                )
                            ],
                            className='m-2 mt-2 shadow-sm'
                        )
                    ],
                    md={
                        'size': 3,
                        'offset': 0,
                        'order': 'last'
                    },
                    sm={
                        'size': 10,
                        'offset': 1,
                        'order': 'last'
                    },
                    xs={
                        'size': 10,
                        'offset': 1,
                        'order': 'last'
                    }
                )
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
                                        html.P([
                                            html.A(
                                                children=[html.I(className="bi bi-github")],
                                                disable_n_clicks=True,
                                                href='https://github.com/Orion89',
                                                title="GitHub profile"
                                            ),
                                            " ",
                                            html.A(
                                                children=[html.I(className="bi bi-linkedin")],
                                                disable_n_clicks=True,
                                                href='https://www.linkedin.com/in/leonardo-molina-v-68a601183/',
                                                title="LinkedIn profile"
                                            ),
                                            " 2023 Leonardo Molina V."
                                            ]
                                        ),
                                        html.P('Proyecto académico. El autor no se hace responsable del mal uso del contenido o predicciones.')
                                    ]
                                    
                                )
                            ],
                        )
                    ],
                    class_name='mt-4',
                    width={'size': 12}
                )
            ],
            align='center',
            class_name='text-end'
        )
    ],
    fluid=True
)


@app.callback(Output('info-img-title', 'children'),
              # Output('cls-predictions', 'children'),
              Output('main-card', 'className'),
              Output('imgs-idx-store', 'data'),
              Output('img-button', 'class_name'),
              Input('pic-upload-1', 'contents'))
def send_image(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        n_neighbors = 1
        print(content_type)
        try:
            if 'image' in content_type:
                decoded = base64.b64decode(content_string)
                files = {'file': decoded}
                response = requests.post(urljoin(API, api_upload_image), files=files)
                response_dict = json.loads(response.text)
                nearest_neighbors = ', '.join([name for name in response_dict['nearest_neighbors'][:n_neighbors]])
                download_button_class_name = 'visible d-grid gap-2 col-6 mx-auto shadow' if utils.infographics_dict.get(nearest_neighbors, None) else 'invisible'
                # pred_style={
                #         'width': '90%',
                #         'height': '70px',
                #         'lineHeight': '60px',
                #         'borderWidth': '2px',
                #         'borderStyle': 'dashed',
                        
                #         'borderRadius': '5px',
                #         'textAlign': 'center',
                #         'margin': '10px'
                #     }
                return 'Sugerencia de identificación: ' + nearest_neighbors, 'bg-success', response_dict['nearest_imgs_idx'], download_button_class_name
            else:
                return 'Tipo de archivo no válido.', 'bg-danger', no_update, no_update
        except Exception as e:
            print(e)
            return "Hubo un problema al procesar la imagen, vuelve a intentar con un archivo de imagen válido.", '', None, no_update
    else:
        return 'Afiche aleatorio', '', None, no_update
        

about_classifications_text = 'Tener presente que la clasificación puede ser desacertada. Considerar con precaución.'
about_classifications_title = 'Es importante' 
    
@app.callback(Output('info-img', 'src'),
              Input('info-img-title', 'children')) # Input('cls-predictions', 'children')
def refresh_infographic(predictions):
    random_img = random.choice(list(infographics_path.glob('*.jpg')))
    first_pred = predictions.partition(': ')[2]
    if 'Sugerencia' in predictions:
        if first_pred == 'acanthogonatus sp':
            return (str(infographics_path / 'genero_acanthogonatus.jpg'))
        
        elif first_pred == 'allende sp' or first_pred == 'tetragnatha sp':
            return (str(infographics_path / 'familia_tetragnathidae.jpg'))
        
        elif first_pred == 'anyphaenidae':
            return (str(infographics_path / 'familia_anyphaenidae.jpg'))
        
        elif first_pred == 'argiope argentata' or first_pred == 'argiope trifasciata':
            return (str(infographics_path / 'genero_argiope.jpg'))
        
        elif first_pred == 'ariadna sp':
            return (str(infographics_path / 'genero_ariadna.jpg'))
        
        elif first_pred == 'austrochilidae':
            return (str(infographics_path / 'familia_austrochilidae.jpg'))
        
        elif first_pred == 'doliomalus cimicoides':
            return (str(infographics_path / 'especie_doliomalus_cimicoides.jpg'))
        
        elif first_pred == 'dysdera crocata':
            return (str(infographics_path / 'especie_dysdera_crocata.jpg'))
        
        elif first_pred == 'euathlus manicata':
            return (str(infographics_path / 'especie_euathlus_manicata.jpg'))
        
        elif first_pred == 'euathlus truculentus':
            return (str(infographics_path / 'especie_euathlus_truculentus.jpg'))
        
        elif first_pred == 'gnaphosidae':
            return (str(infographics_path / 'familia_gnaphosidae.jpg'))
        
        elif first_pred == 'gnolus sp':
            return (str(infographics_path / 'genero_gnolus.jpg'))
        
        elif first_pred == 'grammostola rosea':
            return (str(infographics_path / 'especie_grammostola_rosea.jpg'))
        
        elif first_pred == 'homoeomma':
            return (str(infographics_path / 'genero_homoeomma.jpg'))
        
        elif first_pred == 'latrodectus sp':
            return (str(infographics_path / 'genero_latrodectus.jpg'))
        
        elif first_pred == 'loxosceles laeta':
            return (str(infographics_path / 'genero_loxosceles.jpg'))
        
        elif first_pred == 'lycosidae':
            return (str(infographics_path / 'familia_lycosidae.jpg'))
        
        elif first_pred == 'lyniphiidae':
            return (str(infographics_path / 'familia_linyphiidae.jpg'))
        
        elif first_pred == 'macerio':
            return (str(infographics_path / 'genero_macerio.jpg'))
        
        elif first_pred == 'mastophora sp':
            return (str(infographics_path / 'genero_mastophora.jpg'))
        
        elif first_pred == 'menemerus semilimbatus' or first_pred == 'saphrys rusticana':
            return (str(infographics_path / 'familia_salticidae.jpg'))
        
        elif first_pred == 'metepeira sp':
            return (str(infographics_path / 'genero_metepeira.jpg'))
        
        elif first_pred == 'misumenops sp' or first_pred == 'coenypha sp':
            return (str(infographics_path / 'familia_thomisidae.jpg'))
        
        elif first_pred == 'molinaranea clymene':
            return (str(infographics_path / 'especie_molinaranea_clymene.jpg'))
        
        elif first_pred == 'molinaranea magellanica':
            return (str(infographics_path / 'especie_molinaranea_magellanica.jpg'))
        
        elif first_pred == 'ocrepeira sp':
            return (str(infographics_path / 'especie_ocrepeira_venustula.jpg'))
        
        elif first_pred == 'oecobius sp':
            return (str(infographics_path / 'genero_oecobius.jpg'))
        
        elif first_pred == 'pachylus' or first_pred == 'sadocus sp':
            return (str(infographics_path / 'orden_opilones.jpg'))
        
        elif first_pred == 'petrichus sp':
            return (str(infographics_path / 'genero_petrichus.jpg'))
        
        elif first_pred == 'pholcidae':
            return (str(infographics_path / 'familia_pholcidae.jpg'))
        
        elif first_pred == 'phrixotrichus sp':
            return (str(infographics_path / 'familia_theraphosidae.jpg'))
        
        elif first_pred == 'plesionela bonneti':
            return (str(infographics_path / 'especie_plesiolena_bonneti.jpg'))
        
        elif first_pred == 'polybetes sp':
            return (str(infographics_path / 'genero_polybetes.jpg'))
        
        elif first_pred == 'scytodes globula':
            return (str(infographics_path / 'genero_scytodes.jpg'))
        
        elif first_pred == 'sicarius':
            return (str(infographics_path / 'genero_sicarius.jpg'))
        
        elif first_pred == 'steatoda grossa' or first_pred == 'steatoda nobilis' or first_pred == 'steatoda triangulosa':
            return (str(infographics_path / 'genero_steatoda.jpg'))
        
        elif first_pred == 'sybota sp':
            return (str(infographics_path / 'familia_uloboridae.jpg'))
        
        elif first_pred == 'zygiella x-notata':
            return (str(infographics_path / 'especie_zygiella_x-notata.jpg'))
        elif first_pred == 'solifugae':
            return (str(infographics_path / 'orden_solifugae.jpg'))
        else:
            return (str(infographics_path / 'no_afiche.png'))
    
    else:
        return str(random_img)
    

@app.callback(Output('img-1', 'src'),
              Output('img-2', 'src'),
              Output('img-container-1', 'class_name'),
              Output('warning-title', 'children'),
              Output('warning-text', 'children'),
              Input('imgs-idx-store', 'modified_timestamp'),
              State('imgs-idx-store', 'data'))
def get_nearest_imgs(timestamp, data):
    if data:
        nearest_imgs_list = []
        for num in data[1:3]:
            body = {'imgs_idxs': num}
            response = requests.post(urljoin(API, api_get_pred_imgs), json=body)
            img_decoded = 'data:image/png;base64,' + base64.b64encode(response.content).decode('utf-8')
            nearest_imgs_list.append(img_decoded)
        # print(response.content)
        return nearest_imgs_list[0], nearest_imgs_list[1], 'm-1 visible shadow-sm', about_classifications_title, about_classifications_text
    else:
        return no_update, no_update, no_update, no_update, no_update 


@app.callback(
    Output('download-image', 'data'),
    Input('img-button', 'n_clicks'),
    State('info-img-title', 'children'),
    prevent_initial_call=True
)
def download_infographic(n_clicks, pred):
    # 'Afiche aleatorio'
    if 'Sugerencia de clase:' in pred:
        first_pred = pred.partition(': ')[2]
        file_name = utils.infographics_dict.get(first_pred, None)
        if file_name:
            path_file = infographics_path / file_name
            return dcc.send_file(path_file)
        else:
            no_update
    else:
        no_update
    

# @app.callback(Output('user-info', 'children'),
#               Input('user-info', 'children'))
# def request_info(children):
#     host = request.headers['host'].partition(':')[0]
#     request_address = request.remote_addr
#     user_agent = request.user_agent
#     print(f'host info: {host}')
#     print(f'from user-agent: {user_agent}')
    
#     try:
#         request_info = DbIpCity.get(request_address, api_key='free')
#         region = request_info.region
#         country = request_info.country
#         latitude = request_info.latitude
#         longitude = request_info.longitude
#     except Exception as e:
#         print('An error has ocurred in getting user info:')
#         print(e)
#         region = None
#         country = None
#         latitude = None
#         longitude = None
    
#     query = text(
#         '''
#         INSERT INTO user_info (host, region, country, date, latitude, longitude)
#         VALUES (:host, :region, :country, :date, :latitude, :longitude)
#         ''')
#     row_data = dict(
#         host=request_address,
#         region=region,
#         country=country,
#         date=datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
#         latitude=latitude,
#         longitude=longitude
#     )
#     engine.execute(
#         query,
#         **row_data  
#     )

#     return no_update


if __name__ == "__main__":
    app.run_server(debug=False, port="9000")