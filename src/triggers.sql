CREATE TRIGGER bloccaAbbassamentoStipendio
AFTER UPDATE OF stipendio ON dipendenti
REFERENCING OLD ROW AS oldRow, NEW ROW AS newRow
FOR EACH ROW
WHEN (oldRow.stipendio > newRow.stipendio)
UPDATE dipendenti
SET stipendio = oldRow.stipendio
WHERE id = newRow.id;

CREATE TRIGGER mediaStipendiSopra500mila
AFTER UPDATE OF stipendio ON dipendenti
REFERENCING OLD TABLE AS oldTable, NEW TABLE AS newTable
FOR EACH STATEMENT
WHEN (500000 > SELECT AVG(stipendio) FROM dipendenti)
BEGIN
  DELETE FROM dipendenti;
  INSERT INTO dipendenti (SELECT * FROM oldTable);
END;

CREATE TRIGGER dataFilmDefaultNonNull
AFTER UPDATE OF dataUscita ON films
REFERENCING NEW ROW AS newRow
FOR EACH ROW
WHEN (newRow.dataUscita IS NULL)
UPDATE films
SET dataUscita = 1915
WHERE id = newRow.id

CREATE TRIGGER NoPCLaptop
BEFORE INSERT OR UPDATE ON Product
FOR EACH ROW
EXECUTE FUNCTION NoPCLaptop();

CREATE FUNCTION NoPCLaptop() RETURNS trigger AS $$
BEGIN
  IF (NEW.type = 'pc' AND NEW.maker IN (
    SELECT maker FROM Product WHERE type = 'laptop'
  )) THEN RETURN NULL;
  END IF;

   IF (NEW.type = 'laptop' AND NEW.maker IN (
    SELECT maker FROM Product WHERE type = 'pc'
  )) THEN RETURN NULL;
  END IF;

  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER NoCheapLaptop
BEFORE INSERT OR UPDATE ON Pc
FOR EACH ROW
EXECUTE FUNCTION NoCheapLaptop();

CREATE FUNCTION NoCheapLaptop() RETURNS trigger AS $$
BEGIN 
  IF (EXISTS (
    SELECT * FROM Pc WHERE NEW.ram > ram AND NEW.price <= price
  )) THEN RETURN NULL;
  END IF;
  RETURN NEW;
END
$$ LANGUAGE plpsql;

CREATE TRIGGER Wellformed
BEFORE INSERT OR UPDATE ON Product
FOR EACH ROW
EXECUTE FUNCTION Wellformed();

CREATE FUNCTION Wellformed() RETURNS trigger AS $$
BEGIN
  IF (NEW.model IN (SELECT model FROM pc) OR
                IN (SELECT model FROM laptop) OR 
                IN (SELECT model FROM printer)
  ) RETURN NEW;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpsql;

