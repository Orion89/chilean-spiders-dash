# Identifica esa araña

App desarrollada con Dash para servir un clasificador de fotografías de arácnidos de Chile basado en *deep distance metric learning*.

Disponible en: https://nearest-spiders-production.up.railway.app/

## A considerar 

* El *host* es railway.app
* No obtenemos datos de los usuarios
* No nos quedamos con las fotografías compartidas
* El algoritmo fue ajustado usando fotografías de sólo 51 **clases**, siendo este último término usado en forma general para distintos conceptos: orden, familia, género y especie.
* El modelo entregará un resultado aún cuando las fotografías no correspondan a arácnidos.

Las fichas que se muestran en la app fueron elaboradas por el equipo del grupo en Facebook de [Arañas de Chile](https://www.facebook.com/groups/aranasdechile). Los créditos de cada afiche aparecen en la parte inferior de los mismos.

## API

La app consume una pequeña API desarrollada usando FastAPI, la cual se puede ver en https://github.com/Orion89/chilean-spiders-api

## Modelo

Se ha utilizado un red *ResNet50* como *feature extractor* con pesos pre entrenados más una serie de capas lineales y funciones de activación entre estas últimas como cabeceras, con pesos iniciados aleatoriamente. El entrenamiento ajusta los pesos (a los cuales no se les hace *freeze*) usando la función de pérdida *triplet loss* [(Schroff et al. 2015)](https://arxiv.org/abs/1503.03832):

$$\mathcal{L}_{triplet}=max \left(0, \mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{p}) - \mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{n}) + \alpha \right)$$

<img src="https://latex.codecogs.com/gif.latex?\mathcal{L}_{triplet}=max\left(0,\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{p})-\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{n})+\alpha \right)"/>
<img src="https://render.githubusercontent.com/render/math?math=\mathcal{L}_{triplet}=max\left(0,\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{p})-\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{n})+\alpha \right)">
