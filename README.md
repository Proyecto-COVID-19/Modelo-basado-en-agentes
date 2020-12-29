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

### 1. Crear la grilla a partir del archivo de geopandas:

A partir de un archivo geopandas con el mapa de la ciudad y sus correspondientes zonas/comunas/barrios creamos una grilla con el tamaño en metros especificado y seleccionamos una zona/barrio/comuna particular. En el siguiente ejemplo se encuentra en el mapa de la ciudad de Cartagena, en azul la zona/comuna/barrio escogido y en rosado una celda de la zona seleccionada aleatoreamente.

<img src="https://github.com/SISCOVID/Modelo-basado-en-agentes/blob/master/Mapa_ciudad.png" width="400">
<img src="https://github.com/SISCOVID/Modelo-basado-en-agentes/blob/master/Mapa_grilla.png" width="400">
