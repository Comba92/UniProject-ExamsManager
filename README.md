# Building
1. pip install pipenv
2. pipenv shell
3. flask --app src/main run

# TODO
1. Controller per certe query (studentExists, etc...)
2. Trigger per controllo una sola prova valida per appello
3. Trigger eliminazione prova valida dopo scadenza

4. Rifare schemi, la tabella NonValidi e' inutile e non e' necessaria

# Frontend
1. Studente:
  1. Visualizzazione libretto (voti)
  2. Visualizzaznioe/Iscrizione ad esami
  3. Visualizzione prenotazioni appelli
  4. Visualizzazione esiti (prove valide)
  5. Visualizzazione storico (prove invalide)
2. Docente:
  1. Creazione appelli
  2. Visualizzazione corso/appelli/prove
  3. Storico presenze appelli
  4. Assegnazione voti per prova
  - Anullamento manuale esami (possibile aggiunta)

# Environment
https://datascience.stackexchange.com/questions/24093/how-to-clone-python-working-environment-on-another-machine

```python
conda env export > environment.yml

conda env create -f environment.yml
```

# Supabase

If supabase fails to connect 

https://github.com/supabase/supabase/issues/7938

# Routes
* UniExamHandler.com/
  * Login
  * Register
  * Home
  * Profile
  * Statistics
  * Exams Subscription (student)
  * Reservations (student)
  * 

# Environment 

# Conda

# Poetry
C:\Users\PayThePizzo\AppData\Roaming\Python\Scripts\poetry

# Weak points
* Security - Login
* SQL Injection
* Timezone absent in dates