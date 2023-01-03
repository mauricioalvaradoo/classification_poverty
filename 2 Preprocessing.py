## Preprocesando las bases de la ENAHO
# Limpiare y modificare los modulos de la ENAHO anual del 2019 con la finalidad de contar con las
# principales variables que se usaran para la clasificacion

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


# Importacion ====================================================================
# Sumaria
set1 = pd.read_stata(
    "./data/sumaria-2019.dta",
    columns=["mes", "ubigeo", "conglome", "vivienda", "ingmo1hd", "pobreza"]
)

# Modulo 2: Características de los Miembros del Hogar
set2 = pd.read_stata(
    "./data/enaho01-2019-200.dta",
    columns=["mes", "ubigeo", "conglome", "vivienda", "estrato", "codperso", "p208a", "p207", "p209"]
)

# Modulo 3: Educacion
set3 = pd.read_stata(
    "./data/enaho01a-2019-300.dta",
    columns=["mes", "ubigeo", "conglome", "vivienda", "codperso", "p301a", "p301d"]
)

# Modulo 5: Empleo e Ingresos
set4 = pd.read_stata(
    "./data/enaho01a-2019-500.dta",
    columns=["mes", "ubigeo", "conglome", "vivienda", "codperso", "p512a", "p514"]
)


dta = set2.merge(set3, how='inner').merge(set4, how='inner')
dta = dta.merge(set1, how='inner')


# Data Wrangling =================================================================
dta.rename(
    {"p208a": "edad", "p207": "sexo", "p209": "estado_civil", "p301a": "nivel_educ",
    "p301d": "centro_estudios", "p512a": "tamano_empres", "p514": "ocupacion_secund",
    "ingmo1hd": "ingbrut"}, axis=1, inplace=True
)


categorias_urbana = list(dta["estrato"].cat.categories[:5])

dta["area"] = "rural"
dta.loc[dta["estrato"].isin(categorias_urbana), "area"] = "urbana"

dta = dta.drop(["mes", "ubigeo", "conglome", "vivienda", "estrato", "codperso"], axis=1)
dta.head()


"""""
Las variables que quedan por el momento son las siguientes:

# **edad**: edad
# **sexo**: dicotomica de hombre y mujer
# **estado_civil**: estado civil del encuestado
# **nivel_educ**: mayor nivel educativo aprobado
# **centro_estudios**: colegio de procedencia: estatal o no estatal
# **tamano_empres**: cantidad de trabajadores dentro de la empresa que trabaje
# **ocupacion_secud**: dicotomica si cuenta con un segundo trabajo o no
# **ingbrut**: ingresos monetarios brutos
# **pobreza**: dicotomica si es pobre o no
# **area**: categorias donde están los que viven en zona urbana o rural

"""""


# Revision de las variables ======================================================
print(f"La cantidad de observaciones son {dta.shape[0]}, y la cantidad de variables son: {dta.shape[1]}")

dta.dtypes

dta.describe()

# Missing values
missing_data = dta.isnull()
for i in missing_data.columns.values.tolist():
    print(f"{missing_data[i].value_counts()}\n")

dta = dta.dropna(subset=["tamano_empres", "centro_estudios", "estado_civil"], axis=0)

# Missing values CHECK
missing_data = dta.isnull()
for i in missing_data.columns.values.tolist():
    print(f"{missing_data[i].value_counts()}\n")


dta["sexo"].value_counts()
dta["estado_civil"].value_counts()
dta["nivel_educ"].value_counts()
dta["centro_estudios"].value_counts()
dta["tamano_empres"].value_counts()
dta["ocupacion_secund"].value_counts()
dta["pobreza"].value_counts()
dta["area"].value_counts()


# Reemplazo de las variables =====================================================
# Edad
dta_f = dta[["edad"]].copy()

# Hombre
dta_f["hombre"] = pd.get_dummies(dta["sexo"])["hombre"].astype("float")

# Estado civil
# dta_f["estado_civil"] = dta["estado_civil"].copy()

# Estudios superiores
estudios_superiores = ["superior no universitaria completa", "superior universitaria completa", "maestria/doctorado"]
dta_f["est_sup"] = 0.0
dta_f.loc[dta["nivel_educ"].isin(estudios_superiores), "est_sup"] = 1.0

# Colegio privado
dta_f["colegio_priv"] = pd.get_dummies(dta["centro_estudios"])["no estatal"].astype("float")

# Trabajar en gran empresa
gran_empresa = ["de 101 a 500 personas", "más de 500 personas"]
dta_f["gran_empresa"] = 0.0
dta_f.loc[dta["tamano_empres"].isin(gran_empresa), "gran_empresa"] = 1.0

# Tener segundo trabajo
dta_f["segundo_trab"] = pd.get_dummies(dta["ocupacion_secund"])["si"].astype("float")

# Ingresos brutos
dta_f["ingbrut"] = dta[["ingbrut"]].copy()/12

# Vivir en zona urbana
dta_f["urbano"] = pd.get_dummies(dta["area"])["urbana"].astype("float")

# Pobreza
pobreza = ["pobre extremo", "pobre no extremo"]
dta_f["no_pobre"] = 1.0
dta_f.loc[dta["pobreza"].isin(pobreza), "no_pobre"] = 0.0



# Check final ====================================================================
dta_f.head()
dta_f["no_pobre"].value_counts()



for file in os.listdir("data"):
    os.remove(f"data//{file}")

dta_f.to_csv("./data/data_f.csv", index_label=None)
