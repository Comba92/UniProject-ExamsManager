INSERT INTO Utenti (username)
VALUES ('88001'), ('88002'), ('88003'), ('99001');

INSERT INTO Studenti (nome, idUtente)
VALUES ('marco', 1), ('giulio', 2), ('andrea', 3);

INSERT INTO Docenti (nome, idUtente)
VALUES ('prof', 4);

INSERT INTO Corsi (titolo)
VALUES ('informatica'), ('matematica'), ('statistica');

INSERT INTO Percorsi (proveDaSuperare)
VALUES (3), (2), (1), (2), (1);

INSERT INTO Prove (idCorso, idPercorso)
VALUES (1, 1), (1, 1), (1, 1), (1, 2), (1, 2), (1, 3), (2, 4), (2, 5);

INSERT INTO Appelli (idProva)
VALUES (1), (2), (3), (4), (5), (6), (7), (8);

INSERT INTO Compiti (idAppello, idStudente)
VALUES (1, 1), (1, 2), (3, 1), (8, 1), (2, 2), (2, 3), (4, 2), (1, 3), (4, 3), (5, 3);

INSERT INTO Compiti_Validi (idCompito)
VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);