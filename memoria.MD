# Estructura de la memoria del TFM

## Reparto total aproximado

| Apartado | Extensión aproximada |
|---|---:|
| Abstract + Keywords | 0.5 páginas |
| 1. Introduction | 2 páginas |
| 2. State of the art | 3 páginas |
| 3. Method | 6–7 páginas |
| 4. Experiments | 3–4 páginas |
| 5. Results | 4–5 páginas |
| 6. Conclusions | 2 páginas |
| Bibliography | 1 página |

**Total aproximado:** 21.5–24.5 páginas.

---

# Abstract + Keywords — 0.5 páginas aprox.

## Qué decir

- El TFM diseña e implementa un data warehouse.
- Tema: evolución de ventas, transacciones y precios de vivienda en España.
- Problema: datos en distintas fuentes, formatos y niveles de detalle.
- Solución: limpieza/ETL + modelo dimensional + Oracle.
- Resultado: almacén que permite consultas por tiempo, localización, régimen y condición.

## Keywords

- Data warehouse
- ETL
- Housing market
- Dimensional model
- Real estate
- Spain

---

# 1. Introduction — 2 páginas aprox.

## Qué decir

- Importancia social y económica de la vivienda.
- Interés de estudiar cómo evolucionan ventas y precios.
- Problema principal: la información está dispersa en distintas fuentes.
- Los datasets tienen formatos, granularidades y variables diferentes.
- Justificación: un data warehouse permite integrar esos datos y analizarlos mejor.

## Objetivo general

Design and implement a data warehouse for the analysis of housing sales, real estate transactions and housing prices in Spain.

## Objetivos específicos

- Seleccionar fuentes de datos relevantes.
- Limpiar y transformar los datasets.
- Diseñar un modelo dimensional.
- Implementar el modelo en Oracle.
- Cargar los datos mediante procesos ETL.
- Realizar consultas analíticas.

## Alcance

- Se trabaja con datos agregados, no con transacciones individuales.
- Se analiza por tiempo, territorio, régimen y condición de vivienda.
- No se predicen precios ni se estudian compradores/vendedores individuales.

---

# 2. State of the art — 3 páginas aprox.

## 2.1 Data warehouse

- Qué es un data warehouse.
- Diferencia con una base de datos operacional.
- Está orientado al análisis histórico.
- Integra datos de distintas fuentes.

## 2.2 Dimensional modelling

- Tablas de hechos.
- Dimensiones.
- Medidas.
- Grano de una tabla de hechos.
- Esquema en estrella.
- Constelación de hechos.

## 2.3 ETL

- Extract, Transform, Load.
- Extracción desde CSV/XLS.
- Transformación/limpieza.
- Carga final en Oracle.

## 2.4 Technologies

- Python/PySpark: limpieza y transformación.
- Jupyter Notebook: exploración.
- Pentaho Data Integration: carga y jobs ETL.
- Oracle Database: almacén de datos.
- SQL Developer: consultas y gestión.

## 2.5 Housing market data

- Variables habituales: ventas, transacciones, precio/m².
- Análisis por territorio y periodo.
- Vivienda nueva/usada.
- Vivienda libre/protegida.

---

# 3. Method — 6–7 páginas aprox.

Esta es la parte de **qué has hecho y cómo has diseñado la solución**.

## 3.1 General methodology

Explicar el flujo general del proyecto:

- Fuentes de datos.
- Limpieza y transformación.
- Diseño del modelo dimensional.
- Implementación en Oracle.
- Carga de datos.
- Explotación analítica.

Puedes poner una figura sencilla con este flujo:

Fuentes de datos → Limpieza → Modelo dimensional → Oracle → Carga → Análisis

## 3.2 Data sources

Hacer una tabla con los datasets usados:

| Dataset | Source | Format | Periodicity | Geographical level | Main variables | Fact table |
|---|---|---|---|---|---|---|
| Housing sales | INE | CSV | Monthly | Province / region / national | total_sales, regime, condition | FACT_SALES |
| Real estate transactions | MIVAU / datos.gob.es | CSV | Quarterly | Province / region / national | total_transactions, total_transaction_price | FACT_TRANSACTIONS |
| Appraised housing value | MIVAU | XLS/CSV | Quarterly | Province / region / national | average_appraised_price_m2 | FACT_APPRAISALS |

Para cada dataset explicar:

- De dónde viene.
- Qué formato tenía.
- Qué periodicidad tenía.
- Qué nivel geográfico tenía.
- Qué variables principales aportaba.
- A qué tabla de hechos alimenta.

Frase importante para incluir:

The datasets contain aggregated data rather than individual transactions.

## 3.3 Data preprocessing

Explicar las transformaciones principales:

- Lectura de archivos CSV/XLS.
- Limpieza de columnas innecesarias.
- Normalización de nombres de columnas.
- Separación de fechas en `Year`/`Month` o `Year`/`Quarter`.
- Limpieza de regiones y provincias.
- Transformación de códigos tipo `01 Andalucía`.
- Cambio de nombres como `Rioja, La` a `La Rioja`.
- Conversión de valores numéricos si venían con formato español.
- Preparación de CSV finales limpios.

Aquí puedes meter un fragmento pequeño de código, por ejemplo para separar fecha:

    df = df.withColumn("Year", F.substring(F.col("Date"), 1, 4).cast("int")) \
           .withColumn("Month", F.substring(F.col("Date"), 6, 2).cast("int"))

No meter notebooks enteros en el cuerpo principal. El código largo puede ir al anexo.

## 3.4 Creation of Regime and Condition

Explicar que algunas columnas originales mezclaban información sobre régimen y condición de la vivienda.

Ejemplo:

- `Tipo = Protegida Nueva`

Se transforma en:

- `Regime = Protegida`
- `Condition = Nueva`

Tabla útil:

| Original value | Regime | Condition |
|---|---|---|
| Nueva | Libre | Nueva |
| Segunda Mano | Libre | Segunda Mano |
| Protegida Nueva | Protegida | Nueva |
| Protegida Segunda Mano | Protegida | Segunda Mano |

Explicar que esta separación permite analizar las viviendas desde dos dimensiones distintas:

- Régimen: libre o protegida.
- Condición: nueva o segunda mano.

## 3.5 Treatment of aggregated values

Explicar:

- Algunos datos venían ya agregados por comunidad autónoma o a nivel nacional.
- Otros datos venían desagregados por provincia.
- No todos los datasets tenían el mismo nivel de detalle.
- El modelo tuvo que respetar la granularidad original de cada fuente.

Punto importante sobre medidas:

- `total_sales`, `total_transactions` y `total_transaction_price` son medidas aditivas.
- `average_appraised_price_m2` es una medida no aditiva.

Frases importantes:

total_sales, total_transactions and total_transaction_price are additive measures.

average_appraised_price_m2 is a non-additive measure.

Explicación:

- En ventas y transacciones, los totales regionales pueden comprobarse sumando provincias.
- En el valor tasado medio por m², no se puede hacer una suma ni una media simple de provincias, porque se trata de una media agregada que depende de pesos no disponibles.

## 3.6 Dimensional model

Explicar que se usa una **fact constellation schema**, no una única estrella simple.

Motivo:

- Existen varios procesos analíticos diferentes.
- Las tablas tienen diferentes medidas.
- Algunas fuentes son mensuales y otras trimestrales.
- No todas las facts comparten exactamente las mismas dimensiones.

Frase importante:

A fact constellation schema was adopted because the warehouse integrates several analytical processes with different measures and temporal granularities.

## Dimensiones

### DIM_MONTH

- `idMonth`
- `Month`
- `Year`

Uso:

- Se utiliza para datos mensuales, principalmente ventas de viviendas.

### DIM_QUARTER

- `idQuarter`
- `Quarter`
- `Year`

Uso:

- Se utiliza para datos trimestrales, como transacciones y valor tasado medio.

### DIM_LOCATION

- `idLocation`
- `Province` o `City`
- `Region`
- `Location level`, si finalmente lo usas.

Uso:

- Permite analizar los datos por territorio.

Nota:

- Si tus datos van por provincias, lo ideal sería llamar al campo `Province`.
- Si el modelo ya está hecho con `City`, puedes explicar que representa el nivel geográfico disponible en la fuente.

### DIM_CONDITION

- `idCondition`
- `Condition`

Valores posibles:

- New
- Second-hand
- Total, si aplica.

### DIM_REGIME

- `idRegime`
- `Regime`

Valores posibles:

- Free
- Protected
- Total, si aplica.

## Tablas de hechos

### FACT_SALES

Grano:

- Month + location + condition + regime.

Medida:

- `total_sales`.

Descripción:

- Permite analizar la evolución mensual de las ventas de viviendas según territorio, régimen y condición.

### FACT_TRANSACTIONS

Grano:

- Quarter + location + condition + regime.

Medidas:

- `total_transactions`
- `total_transaction_price`

Descripción:

- Permite analizar el número de transacciones inmobiliarias y el precio total asociado.

### FACT_APPRAISALS

Grano:

- Quarter + location.

Medida:

- `average_appraised_price_m2`

Descripción:

- Permite analizar el valor tasado medio por metro cuadrado.
- Esta medida no es aditiva.

Aquí debe ir el diagrama del modelo.

## 3.7 Oracle implementation

Explicar:

- Se implementaron las tablas en Oracle.
- Se definieron claves primarias.
- Se definieron claves foráneas.
- Se creó el esquema mediante SQL Developer.
- Las dimensiones se relacionan con las tablas de hechos mediante identificadores.

Código:

- En el cuerpo principal: solo un fragmento corto de SQL.
- En anexo: script completo si hace falta.

Ejemplo de fragmento corto:

    CREATE TABLE quarter (
      idQuarter NUMBER(10) NOT NULL,
      quarter NUMBER(10),
      year NUMBER(10),
      PRIMARY KEY (idQuarter)
    );

---

# 4. Experiments — 3–4 páginas aprox.

Esta es la parte de **cómo ejecutas, cargas, validas y explotas** la solución.

## 4.1 Experimental environment

Decir herramientas usadas:

- Jupyter Notebook.
- Python.
- PySpark.
- Pentaho Data Integration.
- Oracle Database.
- SQL Developer.
- Power BI, si finalmente lo usas.

Explicar brevemente para qué se usó cada una:

| Tool | Use |
|---|---|
| Jupyter Notebook | Data exploration and preprocessing |
| PySpark | Data cleaning and transformation |
| Pentaho Data Integration | ETL jobs and data loading |
| Oracle Database | Data warehouse storage |
| SQL Developer | SQL execution and database management |
| Power BI | Visual analytics, if used |

## 4.2 Data loading with Pentaho

Explicar:

- Los CSV limpios se cargaron en Oracle usando jobs de Pentaho.
- Primero se cargaron las dimensiones.
- Después se cargaron las tablas de hechos.
- Este orden evita problemas con claves foráneas.
- Los jobs permitieron automatizar la carga de datos desde los CSV finales.

Frase útil:

The loading process was implemented through Pentaho jobs, which imported the cleaned CSV files into the corresponding Oracle dimension and fact tables.

## 4.3 Data validation

Decir que se comprobó:

- Ejecución correcta de jobs de Pentaho.
- Número de registros cargados.
- Ausencia de errores durante la carga.
- Valores distintos en dimensiones.
- Relación correcta entre facts y dimensions.
- Comprobación de claves primarias y foráneas.
- Comparación de totales autonómicos con suma de provincias para medidas aditivas.

Aclaración clave:

- Para ventas y transacciones, se puede comprobar sumando provincias.
- Para precio medio tasado por m², no se suma ni se promedia directamente.

Frase importante:

For additive measures, consistency checks were performed by comparing regional totals with the sum of their corresponding provinces. However, this validation was not applied to average appraised price per square metre, since it is a non-additive measure.

## 4.4 Analytical queries

Explicar qué consultas hiciste o harás:

- Evolución de ventas por mes y año.
- Transacciones por trimestre y región.
- Comparación entre vivienda nueva y segunda mano.
- Comparación entre vivienda libre y protegida.
- Evolución del precio tasado medio por m².
- Ranking de provincias o comunidades por ventas/transacciones.
- Comparación territorial de precios.

Aquí puedes meter 2 o 3 consultas SQL representativas.

Ejemplo:

    SELECT q.year, q.quarter, l.region, SUM(t.total_transactions) AS total_transactions
    FROM transactions t
    JOIN quarter q ON t.quarter_idQuarter = q.idQuarter
    JOIN location l ON t.location_idLocation = l.idLocation
    GROUP BY q.year, q.quarter, l.region
    ORDER BY q.year, q.quarter;

---

# 5. Results — 4–5 páginas aprox.

Esta es la parte de **qué muestran las consultas y visualizaciones**.

## 5.1 Resulting data warehouse

Decir:

- Número de tablas creadas.
- Dimensiones finales.
- Tablas de hechos finales.
- Número de registros cargados, si lo tienes.
- Granularidad final de cada fact table.

Puedes poner una tabla resumen:

| Table | Type | Grain | Main measures |
|---|---|---|---|
| sales | Fact | Month + location + condition + regime | total_sales |
| transactions | Fact | Quarter + location + condition + regime | total_transactions, total_transaction_price |
| appraisals | Fact | Quarter + location | average_appraised_price_m2 |
| month | Dimension | Month/year | - |
| quarter | Dimension | Quarter/year | - |
| location | Dimension | Geographical level | - |
| condition | Dimension | Housing condition | - |
| regime | Dimension | Housing regime | - |

## 5.2 Housing sales evolution

Comentar:

- Evolución temporal de ventas.
- Diferencias por año o mes.
- Comparación entre vivienda nueva y segunda mano, si se analiza.
- Identificación de posibles periodos con mayor o menor actividad.

Meter gráfico o tabla.

## 5.3 Real estate transactions

Comentar:

- Evolución trimestral de transacciones.
- Comparación por regiones o provincias.
- Volumen de operaciones.
- Precio total de transacciones.
- Posible cálculo derivado del precio medio por transacción si decides hacerlo.

## 5.4 Appraised price per square metre

Comentar:

- Evolución del precio tasado medio por m².
- Diferencias entre territorios.
- Comparación entre comunidades o provincias.
- Recordar que no es una medida aditiva.

Frase útil:

The average appraised price per square metre was analysed using the official aggregated values, since this measure cannot be obtained by simply summing or averaging lower geographical levels.

## 5.5 Geographical comparison

Comentar:

- Provincias o comunidades con más ventas.
- Provincias o comunidades con más transacciones.
- Zonas con mayor precio tasado medio.
- Diferencias territoriales relevantes.

Aquí pueden ir rankings, mapas o gráficos de barras.

## 5.6 Power BI visualisations, si lo usas

Si haces Power BI, puedes incluir:

- Captura general del dashboard.
- Gráficas principales.
- Filtros usados.
- Explicación de qué permite analizar el dashboard.

No hace falta meter todas las capturas en el cuerpo principal.

Recomendación:

- Gráficas principales en Results.
- Gráficas secundarias o capturas adicionales en Appendix.

---

# 6. Conclusions — 2 páginas aprox.

## 6.1 Objectives achieved

Decir:

- Se seleccionaron fuentes de datos relevantes.
- Se limpiaron y transformaron los datasets.
- Se diseñó un modelo dimensional.
- Se implementó el modelo en Oracle.
- Se cargaron los datos mediante procesos ETL.
- Se realizaron consultas analíticas.
- Se obtuvo una estructura útil para estudiar el mercado inmobiliario español.

## 6.2 Main contributions

- Integración de datos heterogéneos.
- Modelo en constelación de hechos.
- Separación de datos mensuales y trimestrales.
- Tratamiento de medidas aditivas y no aditivas.
- Base preparada para análisis temporal y geográfico.
- Posibilidad de explotación mediante SQL y visualizaciones.

## 6.3 Limitations

- Los datos son agregados, no transacciones individuales.
- Existen diferentes granularidades temporales entre datasets.
- Algunas categorías dependen de cómo las define la fuente original.
- El precio tasado medio por m² no puede agregarse directamente.
- El análisis está limitado por la disponibilidad y calidad de las fuentes públicas.
- No se analiza el perfil de compradores o vendedores.
- No se realiza predicción avanzada de precios.

## 6.4 Future work

- Añadir más fuentes de datos.
- Crear dashboards completos en Power BI.
- Incorporar variables socioeconómicas, como renta, población o empleo.
- Ampliar el análisis a nivel municipal si se encuentran datos adecuados.
- Aplicar clustering para agrupar territorios con comportamientos similares.
- Aplicar modelos predictivos si las series temporales son suficientemente completas.
- Automatizar completamente el proceso ETL.

Frase final posible:

Overall, the project demonstrates that a data warehouse approach is suitable for integrating and analysing heterogeneous housing market data in Spain, providing a structured basis for future analytical and decision-support applications.

---

# Bibliography — 1 página aprox.

Incluir referencias a:

- INE.
- MIVAU.
- datos.gob.es.
- Documentación oficial de Apache Spark.
- Documentación oficial de Oracle.
- Documentación de Pentaho Data Integration.
- Referencias de data warehouse.
- Referencias de dimensional modelling.
- Documentación de Power BI, si lo usas.

---

# Appendix — opcional / al final

Meter aquí:

- Código SQL completo.
- Transformaciones largas de PySpark.
- Consultas SQL completas.
- Diccionario de datos.
- Capturas adicionales de Power BI.
- Capturas de Pentaho jobs.
- Tablas auxiliares.
- Código usado para generar CSV finales.

En el cuerpo principal solo deben ir fragmentos pequeños y representativos.

---

# Resumen final de la lógica de la memoria

## 1. Introduction

Explica el problema y el objetivo.

## 2. State of the art

Explica los conceptos y tecnologías necesarios.

## 3. Method

Explica qué has construido y cómo está diseñada la solución.

## 4. Experiments

Explica cómo ejecutas, cargas, validas y explotas el almacén.

## 5. Results

Explica qué muestran las consultas y visualizaciones.

## 6. Conclusions

Explica qué has conseguido, limitaciones y trabajo futuro.

---

# Diferencia clave entre Method, Experiments y Results

## Method

Diseño y construcción.

Ejemplo:

- Se diseñó una tabla de hechos para ventas.
- Se separaron las fechas en año y mes.
- Se creó una dimensión geográfica.
- Se implementó el modelo en Oracle.

## Experiments

Ejecución, validación y consultas.

Ejemplo:

- Se cargaron los CSV mediante Pentaho.
- Se comprobó el número de registros.
- Se validaron relaciones entre hechos y dimensiones.
- Se ejecutaron consultas SQL analíticas.

## Results

Interpretación de lo obtenido.

Ejemplo:

- Las ventas evolucionan de cierta manera.
- Algunas regiones presentan mayor volumen de transacciones.
- El precio tasado medio muestra diferencias territoriales.
- El almacén permite responder a las preguntas planteadas.