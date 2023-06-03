# Progetto Basi di dati 2023 - Spinello Ivan, Florian Sabani


# 1. Introduzione
Per la realizzazione di questo progetto, l’applicazione backend è stata sviluppata in Python con la libreria Flask, utilizzando SQLAlchemyCore come ORM per l’ interfacciamento con il DBMS sottostante SQLite. È stato scelto SQLite per la semplicita di utilizzo e portabilità, dato che tutto il database è contenuto in un singolo file. L'applicazione frontend invece è stata sviluppata in Javascript con il framework NextJS.
Le pagine HTML non vengono quindi renderizzate da Flask ma avviene una comunicazione tra back-end (flask) e front-end (angular) tramite il protocollo http in formato Json/REST. Perquanto riguarda il database e’ stato utiliz-zato DataGrip come ide per la visione e sim-ulazione delle query.
Le pagine HTML non vengono quindi renderizzate da Flask: il backend in Flask offre una API REST, che permette tramite il protocollo HTTP di ottenere i dati del database in formato JSON, facilmente manegiabile al lato frontend.

# 2. Architettura
Per la semplicita del progetto, abbiamo deciso di runnarlo esclusivamente il locale.
Il progetto è composto da un server backend, in ascolto delle richieste HTTP, ed il client frontend (il browser). È stato anche utilizzato Github per l'hosting del repository di sotware development e version control.

# 3. Installazione
### Backend
È necessario avere installato Python e il package manager pip.

#### Installazione
```bash
1. cd backend
2. pip install pipenv
```

#### Running
```bash
1. cd backend
2. pipenv shell
3. flask --app src/main run
```

### Frontend
È necessario avere installato Node.js

#### Installazione
```bash
1. cd frontend
2. npm install
```

#### Building
```bash
1. cd frontend
2. npm run build
```

#### Running (development)
```bash
1. cd frontend
2. npm run dev
```

# 5. Progetto
Il progetto si basa sulla realizzazione di un’applicazione web per la gestione degli esami universitari.
L'applicazione è riservata sia a studenti che a professori, e ha funzionalità diverse in base all'utenza. 
Gli studenti possono: 
- vedere le loro iscrizioni ai corsi di laurea, e iscriversi a nuovi
- vedere le loro iscrizioni agli appelli, e iscriviersi a nuovi
- vedere lo storico degli appelli svolti e delle prove attualmente valide
- poter accettare la verbalizzazione del voto finale
I professori possono:
- creare nuovi corsi
- creare nuovi appelli per i corsi
- vedere i corsi che gestiscono
- vedere gli appelli che gestiscono
- assegnare i voti alle prove degli studenti

La home permette agli utenti di fare il login. Il login viene salvato nel localstorage, e si puo fare logout in qualsiasi momento.

# 6. Progettazione del DB
É necessario progettare una base di dati adeguata per fornire un sistema di gestione dei dati. Per implementare una base di dati, per prima cosa si analizza la realtà che si vuole andare a descrivere, trasformandola in un modello. Si identificano di seguito le entità che fanno parte di questa realtà e si relazionano tra loro.

IMMAGINE SCHEMA AD OGGETTI QUI
IMMAGINE SCHEMA LOGICO QUI

## 6.1 Descizione diagramma ad Oggetti
## 6.2 Descrizione diagramma relazionale
## 6.3 Definizione delle entità nel DB 
```python
```
# 7. Query Principali
Le query vengono eseguite nel backend tramite l'ORM, e i dati vengono forniti tramite le rotte HTTP dell'API REST. Essendo necessario conoscere l'API, abbiamo steso una documentazione dell'API con Swagger.


# 8. Scelte progettuali
Sono necessarie delle scelte progettuali utili per poter delineare al meglio tutte le modalità per implementare nella maniera più efficiente e pulita tutto il codice. Per questo motivo ab- biamo deciso di implementare dei vincoli, trig- ger, check su attributi, transazioni utili per le prenotazioni e ruoli nella base di dati per ge- stire le autorizzazioni degli utenti.

## 8.1 Constraints
## 8.2 Triggers
## 8.3 Transactions
## 8.4 Ruoli e permessi
## 8.5 SQL Injections

# 9. Frontend