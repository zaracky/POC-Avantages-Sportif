DROP TABLE IF EXISTS activites;
DROP TABLE IF EXISTS rh;
DROP TABLE IF EXISTS eligibilite;
DROP TABLE IF EXISTS indemnites;
DROP TABLE IF EXISTS tarif;

CREATE TABLE rh (
  id_salarie INTEGER PRIMARY KEY,
  nom TEXT,
  prenom TEXT,
  date_de_naissance DATE,
  bu TEXT,
  date_dembauche DATE,
  salaire_brut INTEGER,
  type_de_contrat TEXT,
  nombre_de_jours_de_cp INTEGER,
  adresse_du_domicile TEXT,
  moyen_de_deplacement TEXT,
  deplacement_normalise TEXT,
  mode_api TEXT,
  distance_km FLOAT,
  distance_valide BOOLEAN,
  sport_pratique_declare BOOLEAN,
  sport_pratique_nom TEXT
);

CREATE TABLE activites (
  id SERIAL PRIMARY KEY,
  id_salarie INTEGER REFERENCES rh(id_salarie),
  date_debut DATE,
  type TEXT,
  distance_m INTEGER,
  duree_s INTEGER,
  commentaire TEXT,
  source TEXT DEFAULT 'manuel'
);

CREATE TABLE eligibilite (
  id_salarie INTEGER PRIMARY KEY,
  nb_activites INTEGER,
  distance_totale_m INTEGER,
  duree_totale_s INTEGER,
  est_eligible BOOLEAN
);

CREATE TABLE indemnites (
  id_salarie INTEGER PRIMARY KEY,
  nom TEXT,
  prenom TEXT,
  distance_km FLOAT,
  nb_activites INTEGER,
  duree_totale_s INTEGER,
  est_eligible BOOLEAN,
  montant_rembourse FLOAT
);

CREATE TABLE tarif (
    id SERIAL PRIMARY KEY,
    montant_euro FLOAT
);

INSERT INTO tarif (montant_euro) VALUES (0.3);
