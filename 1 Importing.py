## Importando modulos de la Enaho-INEI
# Se va a importar la informacion de la encuesta Encuesta Nacional de los Hogares (Enaho) realizado por Inei que
# se encuentra en sus microdatos http://iinei.inei.gob.pe/microdatos/. Este codigo es una adaptacion y extension
# de uno creado y presentado en una clase por Angel Guillen y Erick Oré.

import pandas as pd
from functions import scraping_inei


# Todas las Enahos anuales con sus codigos
Enaho_anual = {
    2004: "280", #0
    2005: "281", #1
    2006: "282", #2
    2007: "283", #3 
    2008: "284", #4
    2009: "285", #5
    2010: "279", #6
    2011: "291", #7
    2012: "324", #8
    2013: "404", #9
    2014: "440", #10
    2015: "498", #11
    2016: "546", #12
    2017: "603", #13
    2018: "634", #14
    2019: "687", #15
    2020: "737", #16
    2021: "759"  #17
}

# Definiendo los modulos a usar y las fechas
Modulos = ["02", "03", "05", "34"]
FechaIni = 2019; FechaFin = 2019

Rango = list(range(FechaIni, FechaFin+1))
Enaho_anual = {key: Enaho_anual[key] for key in Rango}

Periodos = list(Enaho_anual.keys())
Encuestas = list(Enaho_anual.values())


# Importacion
scraping_inei.get_all_in_one(Encuestas, Modulos)