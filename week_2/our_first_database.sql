CREATE TABLE Ages (
    name VARCHAR(128),
    age INTEGER
);

DELETE FROM Ages;
INSERT INTO Ages (name, age) VALUES ('Kate', 31);
INSERT INTO Ages (name, age) VALUES ('Jamaal', 16);
INSERT INTO Ages (name, age) VALUES ('Corinn', 28);
INSERT INTO Ages (name, age) VALUES ('Inga', 36);
INSERT INTO Ages (name, age) VALUES ('Bayley', 38);
INSERT INTO Ages (name, age) VALUES ('Kadin', 18);

SELECT hex(name || age) AS X FROM Ages ORDER BY X;
