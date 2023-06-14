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

Se ha utilizado la técnica de *metric learning*, en concreto, *deep metric deep learning*, para obtener predicciones de clases de las fotografías de consulta usando búsqueda por similitud. A grandes rasos, el grupo de técnicas englobadas bajo el concepto de *distance metric learning* buscan cuyo objetivo es producir médidas de distancias específicas para algún problema en particular a partir de los datos de entrenamiento. Para el caso específico de *deep metric learning*, su objetivo es ajustar una red neuronal (denominada *feature extactor*) para producir representaciones vectoriales (*embeddings*) tal que, en el nuevo espacio embebido aprendido a través del ajuste, los *embeddings* de instancias pertenecientes a una misma clase estén a menor distancia entre sí respecto a *embeddings* de clases diferentes. Para un mayor detalle de estas últimas técnicas, [este blog](https://hav4ik.github.io/articles/deep-metric-learning-survey) es una excelente referencia. Para métodos tradicionales, tal vez es buena idea revisar la documentación de []()     
Se ha utilizado la técnica de *metric learning*, en concreto, *deep metric deep learning*, para obtener predicciones de clases de las fotografías de consulta usando búsqueda por similitud. A grandes rasos, el grupo de técnicas englobadas bajo el concepto de *distance metric learning* buscan cuyo objetivo es producir médidas de distancias específicas para algún problema en particular a partir de los datos de entrenamiento. Para el caso específico de *deep metric learning*, su objetivo es ajustar una red neuronal (denominada *feature extactor*) para producir representaciones vectoriales (*embeddings*) tal que, en el nuevo espacio embebido aprendido a través del ajuste, los *embeddings* de instancias pertenecientes a una misma clase estén a menor distancia entre sí respecto a *embeddings* de clases diferentes. Para un mayor detalle de estas últimas técnicas, [este blog](https://hav4ik.github.io/articles/deep-metric-learning-survey) es una excelente referencia. Para métodos tradicionales, tal vez es buena idea revisar la documentación de [metric-learn](https://hav4ik.github.io/articles/deep-metric-learning-survey).     

Para este caso en particular, se ha utilizado un red *ResNet50* como *feature extractor* con pesos pre entrenados más una serie de capas lineales y funciones de activación entre estas últimas como cabeceras, con pesos iniciados aleatoriamente. El entrenamiento ajusta los pesos (a los cuales no se les hace *freeze*) usando la función de pérdida *triplet loss* [(Schroff et al. 2015)](https://arxiv.org/abs/1503.03832), usando [esta implementación](https://omoindrot.github.io/triplet-loss) como referencia:

$$\mathcal{L}_{triplet}=max \left(0, \mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{p}) - \mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{n}) + \alpha \right)$$

<img src="https://latex.codecogs.com/gif.latex?\mathcal{L}_{triplet}=max\left(0,\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{p})-\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{n})+\alpha \right)"/>
<img src="https://render.githubusercontent.com/render/math?math=\mathcal{L}_{triplet}=max\left(0,\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{p})-\mathcal{D}^{2}_{f_{\theta}}(x_{a}, x_{n})+\alpha \right)">

Las nuevas fotografías son pre procesadas y "pasadas" por el *feature extractor* ya ajustdo, para obtener las representaciones de las mismas. Para asignar una clase (de entrenamiento) al nuevo vector, se ha utilizado la clase `NearestNeighbors` del paquete `sklearn.neighbors` para realizar la búsqueda del *embedding* más cercano al vector de consulta, asigándo a este último la clase del vecino más cercano. También se hicieron pruebas con motores de *similaruty search* tales como [**Qdrant**](https://qdrant.tech/). Sin embargo, al tratarse de relativamente pocos datos de entrenamiento (aproximadamente 15.000 ejemplos), la implementación de [**Scikit-learn**](https://scikit-learn.org/stable/modules/neighbors.html) resultó sencilla y rápida.