import pandas as pd
import numpy as np
import os

def limpiar_tasaciones(ruta_archivo, years):
    quarters = [1, 2, 3, 4]
    col_names = ["City"] + [f"{y}_{q}" for y in years for q in quarters]

    df = pd.read_csv(ruta_archivo, skiprows=15, header=None)
    
    df = df.iloc[:, 1 : len(col_names) + 1] 
    df.columns = col_names

    df = df.dropna(subset=["City"])

    df_melted = pd.melt(df, id_vars=["City"], var_name="Year_Quarter", value_name="Total")
    df_melted[['Year', 'Quarter']] = df_melted['Year_Quarter'].str.split('_', expand=True)

    df_final = df_melted[['City', 'Year', 'Quarter', 'Total']].copy()

    df_final['City'] = df_final['City'].str.strip()
    df_final = df_final[df_final['City'] != 'TOTAL NACIONAL']

    df_final['Total'] = pd.to_numeric(df_final['Total'], errors='coerce')

    mapa_ccaa = {
        'Andalucía': 'Andalucía', 'Almería': 'Andalucía', 'Cádiz': 'Andalucía', 'Córdoba': 'Andalucía', 'Granada': 'Andalucía', 'Huelva': 'Andalucía', 'Jaén': 'Andalucía', 'Málaga': 'Andalucía', 'Sevilla': 'Andalucía',
        'Aragón': 'Aragón', 'Huesca': 'Aragón', 'Teruel': 'Aragón', 'Zaragoza': 'Aragón',
        'Asturias (Principado de )': 'Principado de Asturias', 
        'Balears (Illes)': 'Illes Balears', 
        'Canarias': 'Canarias', 'Palmas (Las)': 'Canarias', 'Santa Cruz de Tenerife': 'Canarias',
        'Cantabria': 'Cantabria',
        'Castilla y León': 'Castilla y León', 'Ávila': 'Castilla y León', 'Burgos': 'Castilla y León', 'León': 'Castilla y León', 'Palencia': 'Castilla y León', 'Salamanca': 'Castilla y León', 'Segovia': 'Castilla y León', 'Soria': 'Castilla y León', 'Valladolid': 'Castilla y León', 'Zamora': 'Castilla y León',
        'Castilla-La Mancha': 'Castilla - La Mancha', 'Albacete': 'Castilla - La Mancha', 'Ciudad Real': 'Castilla - La Mancha', 'Cuenca': 'Castilla - La Mancha', 'Guadalajara': 'Castilla - La Mancha', 'Toledo': 'Castilla - La Mancha',
        'Cataluña': 'Cataluña', 'Barcelona': 'Cataluña', 'Girona': 'Cataluña', 'Lleida': 'Cataluña', 'Tarragona': 'Cataluña',
        'Comunidad Valenciana': 'Comunitat Valenciana', 'Alicante/Alacant': 'Comunitat Valenciana', 'Castellón/Castelló': 'Comunitat Valenciana', 'Valencia/València': 'Comunitat Valenciana',
        'Extremadura': 'Extremadura', 'Badajoz': 'Extremadura', 'Cáceres': 'Extremadura',
        'Galicia': 'Galicia', 'Coruña (A)': 'Galicia', 'Lugo': 'Galicia', 'Ourense': 'Galicia', 'Pontevedra': 'Galicia',
        'Madrid (Comunidad de)': 'Comunidad de Madrid',
        'Murcia (Región de)': 'Región de Murcia',
        'Navarra (Comunidad Foral de)': 'Comunidad Foral de Navarra',
        'País Vasco': 'País Vasco', 'Araba/Alava': 'País Vasco', 'Gipuzkoa': 'País Vasco', 'Bizkaia': 'País Vasco',
        'Rioja (La)': 'La Rioja',
        'Ceuta y Melilla': np.nan, 
        'Ceuta': 'Ceuta', 'Melilla': 'Melilla'
    }

    mapa_provincias = {
        'Asturias (Principado de )': 'Asturias',
        'Balears (Illes)': 'Illes Balears',
        'Palmas (Las)': 'Las Palmas',
        'Coruña (A)': 'A Coruña',
        'Madrid (Comunidad de)': 'Madrid',
        'Murcia (Región de)': 'Murcia',
        'Navarra (Comunidad Foral de)': 'Navarra',
        'Araba/Alava': 'Araba/Álava',
        'Rioja (La)': 'La Rioja'
    }

    cabeceras_multi = ['Andalucía', 'Aragón', 'Canarias', 'Castilla y León', 'Castilla-La Mancha', 'Cataluña', 'Comunidad Valenciana', 'Extremadura', 'Galicia', 'País Vasco', 'Ceuta y Melilla']

    df_final['Region'] = df_final['City'].map(mapa_ccaa)
    df_final.loc[df_final['City'].isin(cabeceras_multi), 'City'] = np.nan
    df_final['City'] = df_final['City'].replace(mapa_provincias)

    df_final = df_final.dropna(subset=['Region', 'City'], how='all')

    df_final['City'] = df_final['City'].fillna('Total')
    
    return df_final[['Region', 'City', 'Year', 'Quarter', 'Total']]

def main():
    archivos_a_procesar = [
        {"ruta": "../datasets/dataset_appraisals1.csv", "years": [2010, 2011, 2012, 2013, 2014]},
        {"ruta": "../datasets/dataset_appraisals2.csv", "years": [2015, 2016, 2017, 2018, 2019]},
        {"ruta": "../datasets/dataset_appraisals3.csv", "years": [2020, 2021, 2022, 2023]},
        {"ruta": "../datasets/dataset_appraisals4.csv", "years": [2024, 2025]} 
    ]

    lista_dataframes = []

    try:
        for archivo in archivos_a_procesar:
            df_procesado = limpiar_tasaciones(archivo["ruta"], archivo["years"])
            lista_dataframes.append(df_procesado)

        if lista_dataframes:
            df_historico_completo = pd.concat(lista_dataframes, ignore_index=True)
            
            os.makedirs("../datasets_def/appraisals_clean", exist_ok=True)
            df_historico_completo.to_csv("../datasets_def/appraisals_clean/appraisals_clean.csv", index=False)
            
            print("Process executed successfully.")
            
    except Exception as e:
        print(f"Execution error: {e}")

if __name__ == "__main__":
    main()