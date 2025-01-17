## Descrizione del Codice

### 1. **Importazione dei Dati**

Il codice importa due file CSV contenenti dati relativi alla concentrazione di black carbon (BC) acquisiti da AMAT e ARPA:

- `BC_AMAT_006_min.csv`: Dati da stazione AMAT.
- `BC_ARPA_orari.csv`: Dati da stazione ARPA.

I dati vengono importati con la funzione `pandas.read_csv()`, saltando le righe non necessarie e convertendo il campo temporale `Field` in formato `datetime`.

### 2. **Pre-elaborazione dei Dati**

Il codice esegue diverse operazioni di pulizia sui dati:

- Converte il campo `Field` in formato `datetime`.
- Sostituisce i valori uguali a 0 o -999 con `NaN` nelle colonne di tipo `float64`.
- Interpola i valori mancanti nella colonna `Aver` (media).

### 3. **Calcolo della Media Mobile Esponenziale (EMA) e della Media Mobile Esponenziale Doppia (DEMA)**

Il codice calcola la media mobile esponenziale (EMA) con un periodo di 15 minuti utilizzando la funzione `ewm().mean()` di Pandas. Successivamente, viene calcolata la doppia media mobile esponenziale (DEMA).


### 4. **Calcolo della Media Oraria**

I dati vengono resi orari mediante la funzione `resample('h').mean()`, creando un nuovo DataFrame `df_AMAT` contenente la media per ogni ora.

### 5. **Unione dei Dataset**

I dati di AMAT e ARPA vengono uniti in un unico DataFrame `df_unico` sulla base della colonna `Data`. Le righe con timestamp superiori alla data di fine specificata vengono rimosse, per concentrarsi sui dati fino a una data specifica.

### 6. **Statistica Descrittiva**

Il codice esegue una statistica descrittiva sui dati unificati, visualizzando una panoramica delle principali metriche come media, deviazione standard, minimi e massimi con `df_unico.describe()`.

### 7. **Regressione Lineare**

Per analizzare la relazione tra le variabili di AMAT (e.g., `AMAT_006`, `EMA`, `DEMA`) e i dati ARPA (`ARPA_Senato`), viene calcolata una regressione lineare tra ogni variabile e il target. I risultati della regressione (pendenza, intercetta, valore di $R^2$) vengono visualizzati in un grafico scatterplot con la retta di regressione sovrapposta.

### 8. **Visualizzazioni**

Il codice genera diverse visualizzazioni:

- **Grafico della DEMA e dei valori originali**: Mostra i valori originali di `Aver` e la DEMA calcolata.
- **Scatterplot con regressione**: Un grafico a dispersione che mostra la relazione tra i dati ARPA (`ARPA_Senato`) e le variabili di AMAT (e.g., `AMAT_006`, `EMA`, `DEMA`), con la retta di regressione tracciata sopra i dati.
- **Tabella dei risultati della regressione**: Visualizza i dettagli della regressione per ogni variabile, inclusi la pendenza, l'intercetta e il valore di $R^2$.

### 9. **Output**

I risultati della regressione lineare vengono visualizzati sia in un grafico scatterplot che in una tabella. La tabella riporta i dettagli della regressione, inclusi la pendenza, l'intercetta e il valore di $R^2$ per ogni variabile.

