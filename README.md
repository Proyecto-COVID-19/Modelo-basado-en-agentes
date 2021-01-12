# SISCOVID - Modelo basado en agentes en python (ABM)
![](logo-main.png)

El modelo de agentes desarrollado en python del proyecto SISCOVID permite apoyar la toma de decisiones para el control y mitigación de la pandemia causada por la transmisión de SARS-CoV-2.

## Objetivo del modelo basado en agentes
Simular el comportamiento de la pandemia en contextos urbanos a través de un modelo computacional que incorpora la movilidad de los ciudadanos y las dinámicas de infección por grupos de edad y estratos socioeconómicos específicos a 4 ciudades de Colombia.

Esta librería permite:
- Generar la grilla de una ciudad a partir de un archivo geopandas
- Simular la mobilidad de multiples agentes en la grilla
- Simular diferentes decisiones de movimiento y estados de infección de los agentes
- Diseñar y simular intervenciones de mitigación de la transmisión de infecciones.

## Tabla de contenidos:

1. [Documentación](#documentacion)  
2. [Citación](#citacion) 
3. [Colabore con nosotros](#colaboracion)
4. [Instalación](#instalacion)
    - [Con pip](#pip)
    - [Con conda](#conda)
    - [Problemas comunes](#problemas)
    - [Test de instalación](#tests)
    - [Colaboración en Google colab](#colab)
5. [Tutoriales](#tutoriales)
5. [Ejemplos](#ejemplos)


<a name="documentacion"/>

## Documentación
La documentación de las clases y funciones de SISCOVID-ABM está disponible en: https://siscovid.com/


<a name="citacion"/>

## Citación
Si usted utiliza la librería por favor citar el siguiente paper:

> Felipe Montes, Jose D. Meisel, Pablo Lemoine, Diana R. Higuera, Andrés F. Useche, Sofía del C. Baquero, Juliana Quintero, Diego A. Martínez, Laura Idrobo, Ana M. Jaramillo, Juan D. Umaña, Diana Erazo, Daniel Duque, Andrea Alarcón, Carolina Rojas, Olga L. Sarmiento, Santiago Ortiz, Julián Castro, Gustavo Martínez, Juan Sosa, John K. Giraldo, Fabián C. Peña, Camilo Montes, Juan S. Guerrero & Esperanza Buitrago. **SISCOVID: modelos de sistemas complejos para contribuir a disminuir la transmisión de SARS-CoV-2 en contextos urbanos de colombia**, 2020

<a name="colaboracion"/>

## Colabore con nosotros
`SISCOVID-ABM` es un proyecto activo y las colaboraciones son bienvenidas. 
Si usted quiere ser parte del proyecto o crear colaboraciones para otras intervenciones no dude en contactarnos.

<a name="instalacion"/>

## Instalación

<a name="pip"/>

### Con pip

<a name="conda"/>

### Con conda

<a name="problemas"/>

### Problemas comunes

<a name="tests"/>

### Test de instalación

<a name="colab"/>

### Colaboración en Google colab

<a name="tutoriales"/>

## Tutoriales

<a name="ejemplos"/>

## Ejemplos

Librerías que usamos para el modelo:
```python
import os
import sys
import pickle
import json
from collections import defaultdict
from itertools import product
import numpy as np
import geopandas as gpd
from geopy import distance
from shapely.geometry import Polygon
```

### 1. Crear la grilla a partir del archivo de geopandas:

A partir de un archivo geopandas con el mapa de la ciudad y sus correspondientes zonas/comunas/barrios creamos una grilla con el tamaño en metros especificado y seleccionamos una zona/barrio/comuna particular. En el siguiente ejemplo se encuentra en el mapa de la ciudad de Cartagena, en azul la zona/comuna/barrio escogido, en rosado una celda de la zona seleccionada aleatoreamente y la cada cuadro de  la grilla con 1 km de ancho/largo.

Leer el archivo shapes de la ciudad y guardar las comunas:
```python
shp2 = gpd.read_file(os.path.join('..','Datos',ciudad,'Shapes','ucg.shp'))
comunas = []
ucgs = shp2['UCG'].values
for ucg in ucgs:
    comunas.append('COMUNA ' + str(int(ucg)))
shp2['comuna'] = comunas
```
Objeto geopandas:
```
    UCG LOC  AREA_HA                                           geometry  comuna
0    3.0  LH   202.00  POLYGON ((-75.52126 10.44286, -75.52123 10.442...   COMUNA 3
1    2.0  LH   367.69  POLYGON ((-75.52572 10.44107, -75.52626 10.438...   COMUNA 2
2    1.0  LH   741.96  MULTIPOLYGON (((-75.53969 10.41866, -75.53962 ...   COMUNA 1
3    6.0  LV   974.82  MULTIPOLYGON (((-75.45372 10.41313, -75.45337 ...   
```
Con la función de crear_grilla se crea un diccionario con las llaves de las comunas/localidades y las celdas que están dentro:
```
{'COMUNA 1': [(0, 11),
  (0, 12),
  (0, 13),
  (1, 11),
  (1, 12),
  (1, 13),
  (1, 14),
  (1, 15),
  (1, 16),
  (2, 11)
```
Este objeto de guarda en el archivo _Casillas_comunas_Ciudad_Tamaño_casilla.json_ para ingresar en el modelo.

<img src="https://github.com/SISCOVID/Modelo-basado-en-agentes/blob/master/Mapa_ciudad.png" width="400">
<img src="https://github.com/SISCOVID/Modelo-basado-en-agentes/blob/master/Mapa_grilla.png" width="400">




