# @title Importo data
import numpy as np
import pandas as pd
from datetime import datetime, time
import matplotlib.pyplot as plt

#import da un unico foglio csv
file_csv = f"/content/drive/MyDrive/BlackCarbon/BC_AMAT_006_min.csv"

# Leggi il file fino alla riga 2173 per non usare troppa memoria
df = pd.read_csv(file_csv, sep=",", skiprows=5)

df['Field'] = pd.to_datetime(df['Field'], format='%d/%m/%Y %H:%M')

# Identificare le colonne di tipo float
float_columns = df.select_dtypes(include=['float64']).columns

# Sostituire i valori minori o uguali a 0 con NaN nelle colonne di tipo float
df[float_columns] = df[float_columns].applymap(lambda x: x if x != 0 else np.nan)

df[float_columns] = df[float_columns].applymap(lambda x: x if x != -999 else np.nan)

#df[float_columns] = df[float_columns].applymap(lambda x: x if x < 20000 else np.nan)

df.info()

# @title Calcolo dell'EMA con periodo di 15 minuti
df['Aver'] = df['Aver'].interpolate()
periodo = 15
df['EMA'] = df['Aver'].ewm(span=periodo, adjust=False).mean()
# Calcolare l'EMA sull'EMA
df['EMA_of_EMA'] = df['EMA'].ewm(span=periodo, adjust=False).mean()
# Calcolare la DEMA
df['DEMA'] = 2 * df['EMA'] - df['EMA_of_EMA']

# # Imposta la colonna 'DATA' come indice
#df.set_index('Field', inplace=True)

plt.figure(figsize=(20, 6))
plt.plot(df['Aver'], label='Valori originali', color="black")
plt.plot(df['DEMA'], label='DEMA (Periodo = 15 minuti)', linestyle='-', color="red")
#plt.plot(df['EMA'], label='EMA (Periodo = 15 minuti)', linestyle='-', color="red")
plt.legend()
plt.title('Double Exponential Moving Average (DEMA)')
plt.xlabel('Data')
plt.ylabel('Concentrazione IR BC [ng/m3]')
plt.grid()
plt.show()

# @title calcolare la media oraria
df_AMAT = df.resample('h').mean()

# Reset dell'indice se necessario
df_AMAT.reset_index('Field', inplace=True)

# Rinomina la colonna 'Field' in 'Data'
df_AMAT.rename(columns={'Field': 'Data'}, inplace=True)

# @title import ARPA
file_csv = f"/content/drive/MyDrive/BlackCarbon/BC_ARPA_orari.csv"

# Leggi il file fino alla riga 2173 per non usare troppa memoria
df_ARPA = pd.read_csv(file_csv, sep=";", thousands=".")

df_ARPA['Data'] = pd.to_datetime(df_ARPA['Data'], format='%d/%m/%Y %H:%M')

df_ARPA['ARPA_Senato']=df_ARPA['ARPA_Senato']

# Identificare le colonne di tipo float
float_columns = df_ARPA.select_dtypes(include=['float64']).columns

# Sostituire i valori minori o uguali a 0 con NaN nelle colonne di tipo float
df_ARPA[float_columns] = df_ARPA[float_columns].applymap(lambda x: x if x !=0 else np.nan)

df_ARPA.head()

# @title statistica descrittiva oraria

# Unione dei dataset sulla colonna 'DATA-ORA'
df_unico = pd.merge(df_AMAT, df_ARPA, on='Data', how='outer')

# Rinomina la colonna 'Field' in 'Data'
df_unico.rename(columns={'Aver': 'AMAT_006'}, inplace=True)

data_fine = pd.Timestamp('2024-11-06 01:00:00')
df_unico = df_unico[df_unico['Data'] <= data_fine]

df_unico.describe()

# @title Scatterplot con ARPA

from scipy.stats import linregress

# Variabili indipendenti e dipendente
variabili = ['AMAT_006', 'EMA', 'DEMA']
target = 'ARPA_Senato'

# Creazione del grafico
plt.figure(figsize=(18, 12))

# Tabella per i risultati della regressione
tabella_regressione = []

for i, col in enumerate(variabili, 1):
    # Calcolo della regressione (scambiando x e y)
    slope, intercept, r_value, _, _ = linregress(df_unico[target], df_unico[col])
    equation = f"y = {slope:.2f}x + {intercept:.2f}"
    r_squared = f"$R^2$ = {r_value**2:.2f}"

    # Aggiungi i risultati della regressione alla tabella
    tabella_regressione.append([col, slope, intercept, r_value**2])

    # Creazione sottoplot
    plt.subplot(2, 2, i)
    sns.scatterplot(x=df_unico[target], y=df_unico[col], alpha=0.6, label='Dati osservati')
    plt.plot(df_unico[target], slope * df_unico[target] + intercept, color='red', label='Regressione')

    # Annotazione dell'equazione e di R^2
    plt.text(0.05, 0.95, f"{equation}\n{r_squared}", transform=plt.gca().transAxes,
             fontsize=12, bbox=dict(facecolor='white', alpha=0.6, edgecolor='black'))

    # Etichette e titolo
    #plt.title(f'Regressione lineare: {target} vs {col}')
    plt.xlabel(target)
    plt.ylabel(col)
    plt.legend(loc='lower right')  # Posizione della legenda in basso a sinistra
    plt.grid()

# Aggiungi la tabella dei risultati fuori dal grafico
colonne_tabella = ['Variabile', 'Pendenza', 'Intercetta', '$R^2$']
plt.figure(figsize=(8, 3))
plt.table(cellText=tabella_regressione, colLabels=colonne_tabella, loc='center', cellLoc='center')
plt.axis('off')  # Nascondi gli assi per la tabella
plt.title('Dettagli della regressione')

# Ottimizza lo spazio tra i grafici
plt.tight_layout()
plt.show()
