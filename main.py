import base64
from datetime import datetime
import json
from pathlib import Path
import random
from urllib.parse import urljoin

import plotly
import dash
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import requests

API = 'http://127.0.0.1:8000'
api_upload_image = '/send_img/'
api_get_classes = '/get_train_classes/'
api_get_pred_imgs = '/send_nearest_imgs/'

infographics_path = Path('./static/afiches/')
spiders_classes = json.loads(requests.get(urljoin(API, api_get_classes)).text)

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SIMPLEX], # https://www.nelsontang.com/blog/2022-06-02-dash-tips
                title='Identifica tu araña',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Arañas de Chile", className='fw-bolder text-center'),
                width=12
            ),
            className='m-3'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(
                        id='pic-upload-1',
                        children=[
                            html.Div(
                                [
                                    "Arrastra la fotografía acá o ",
                                    html.A('haz click para seleciconar el archivo')
                                ]
                            )
                        ],
                        multiple=False
                    ),
                    style={
                        'width': '90%',
                        'height': '80px',
                        'lineHeight': '60px',
                        'borderWidth': '2px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    width={'size': 8, 'offset': 2}
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    id='img-1',
                                    class_name='m-1 shadow-sm'
                                ),
                                dbc.CardImg(
                                    id='img-2',
                                    class_name='m-1 shadow-sm'
                                ),
                                dbc.CardFooter(
                                    html.P('Créditos de las fotografías a quien corresponda.', className='card-text shadow-sm')
                                )
                            ],
                            id='img-container-1',
                            class_name='m-1 invisible'
                        ),
                    ],
                    width={'size': 2, 'offset': 0}
                ),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                            html.H4(
                                                'Afiche aleatorio',
                                                id='info-img-title',
                                                className='card-title'
                                            )
                                        ),
                                    dbc.CardBody(
                                        [
                                             html.P(
                                                id="cls-predictions",
                                                className='fw-bolder'
                                            ),
                                            dbc.CardImg(
                                            src="/static/afiches/familia_salticidae.jpg",
                                            id='info-img'
                                    ),
                                    dbc.CardFooter(
                                        [
                                            html.P(
                                                "Todos los créditos al equipo de Arañas de Chile detallado en la parte inferior del afiche.", className='card-text'),
                                            dcc.Store(id='imgs-idx-store') # html.P(id='imgs-idxs', className='invisible')
                                        ],
                                        className='m-2'
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
                    width={'size': 8, 'offset': 0}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                               dbc.CardHeader(html.H4('Atención', className='card-title')),
                               dbc.CardBody(
                                   [
                                       html.P('La clasificación puede ser desacertada. Considerar con precaución.', className='card-text')
                                   ]
                               ) 
                            ],
                            id='warning-msg',
                            color='warning',
                            class_name='invisible'
                        )
                    ]
                )
            ]
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
                                    'El algoritmo fue ajustado usando fotografías de sólo 50 clases, '
                                    'siendo este último término usado en forma general para distintos conceptos: '
                                    'Familia, género y especie.',
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
                    width={'size': 4}
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.H5('Clases de ajuste del algoritmo', className='card-title')),
                            dbc.CardBody(
                                html.P(
                                    ", ".join([name.replace('_', '') for name in spiders_classes['train_classes']]),
                                    className='card-text'
                                )
                            )
                        ],
                        className='m-2 mt-2 shadow-sm'
                    
                    ),
                    width={'size': 4}
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
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardFooter(
                                    html.P("2023 Lenardo Molina")
                                )
                            ],
                        )
                    ],
                    class_name='mt-4',
                    width={'size': 12}
                )
            ],
            class_name='text-end'
        )
    ],
)


@app.callback(Output('info-img-title', 'children'),
              Output('cls-predictions', 'children'),
              Output('main-card', 'className'),
              Output('imgs-idx-store', 'data'),
              Input('pic-upload-1', 'contents'))
def send_image(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        print(content_type)
        try:
            if 'jpeg' in content_type:
                decoded = base64.b64decode(content_string)
                files = {'file': decoded}
                response = requests.post(urljoin(API, api_upload_image), files=files)
                response_dict = json.loads(response.text)
                nearest_neighbors = ', '.join([name for name in response_dict['nearest_neighbors'][:3]])
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
                return 'Posibles clases:', nearest_neighbors, 'bg-success', response_dict['nearest_imgs_idx']
        except Exception as e:
            print(e)
            return "Hubo un problema al procesar la imagen, vuelve a intentar con un archivo de imagen válido.", '', '', None
    else:
        return 'Afiche aleatorio', '', '', None
        
    
@app.callback(Output('info-img', 'src'),
              Input('cls-predictions', 'children'))
def refresh_infographic(predictions):
    random_img = random.choice(list(infographics_path.glob('*.jpg')))
    first_pred = predictions.partition(', ')[0]
    if predictions:
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
        
        elif first_pred == 'pachylus' or first_pred == 'sadocus_sp':
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
        
        else:
            return (str(infographics_path / 'no_afiche.png'))
    
    else:
        return str(random_img)
    

@app.callback(Output('img-1', 'src'),
              Output('img-2', 'src'),
              Output('img-container-1', 'class_name'),
              Output('warning-msg', 'class_name'),
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
        return nearest_imgs_list[0], nearest_imgs_list[1], 'm-1 visible', 'm-1 visible shadow-sm'
    else:
        return no_update, no_update, no_update, no_update 


if __name__ == "__main__":
    app.run_server(debug=False, port="9000")