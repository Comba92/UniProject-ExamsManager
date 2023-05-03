# Building Backend (da sistemare metodo building)
1. pip install pipenv
2. pipenv shell
3. flask --app src/main run

# Building Frontend
1. npm run dev

# TODO
1. Controller per certe query (studentExists, etc...)
2. Trigger per controllo una sola prova valida per appello
3. Trigger eliminazione prova valida dopo scadenza
4. Le view soffrono di SQL injection. Sistemare?

# Viste / Servizi
1. Studente:
  1. ~~Visualizzazione libretto (voti)~~ QUERY NEEDS TESTING
  2. ~~Visualizzazione/Iscrizione a corsi~~
  3. ~~Visualizzione/iscrizione appelli~~
  4. ~~Visualizzazione esiti (prove valide)~~
  5. ~~Visualizzazione storico (prove invalide)~~
2. Docente:
  1. ~~Creazione appelli~~
  2. ~~Visualizzazione corso/appelli/prove~~
  3. ~~Storico presenze appelli~~
  4. Assegnazione voti per prova
    - Anullamento manuale esami (possibile aggiunta)
