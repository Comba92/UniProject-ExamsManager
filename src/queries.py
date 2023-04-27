populate = """
INSERT INTO Studenti (nome)
VALUES ('marco'), ('giulio'), ('andrea');

INSERT INTO Corsi (titolo)
VALUES ('informatica'), ('matematica');

INSERT INTO Prove (idCorso)
VALUES (1)

INSERT INTO Appelli (idProva)
VALUES (1)

INSERT INTO Compiti (idAppello, idStudente)
VALUES (1, 1), (1, 2), (1, 3)

INSERT INTO Compiti_Validi (idCompito)
VALUES (1), (2)
""".split('\n\n')

