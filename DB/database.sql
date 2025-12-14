CREATE DATABASE gestion_db;
CREATE TABLE VILLE (
    nom_ville VARCHAR(200) NOT NULL,
    longi REAL NOT NULL,
    lati REAL NOT NULL,
    region VARCHAR(200) NOT NULL,
    pays VARCHAR(200) NOT NULL,
    PRIMARY KEY (nom_ville)
);
CREATE TABLE CHAMBRE (
    code_c INTEGER NOT NULL,
    surface REAL NOT NULL,
    PRIMARY KEY (code_c)
);
CREATE TABLE AGENCE_DE_VOYAGE (
    code_a INTEGER NOT NULL,
    site_web TEXT NOT NULL,
    telephone VARCHAR(200) NOT NULL,
    Adresse_code_postal INTEGER NOT NULL,
    Adresse_rue_a VARCHAR(200) NOT NULL,
    Adresse_num_a INTEGER NOT NULL,
    Adresse_pays_a VARCHAR(200) NOT NULL,
    VILLE_nom_ville VARCHAR(200) NOT NULL,
    PRIMARY KEY (code_a),
    FOREIGN KEY (VILLE_nom_ville) REFERENCES VILLE (nom_ville)
);
CREATE TABLE RESERVATION (
    CHAMBRE_code_c INTEGER NOT NULL,
    data_d DATE NOT NULL,
    data_f DATE NOT NULL,
    prix REAL NOT NULL,
    AGENCE_DE_VOYAGE_code_a INTEGER NOT NULL,
    PRIMARY KEY (CHAMBRE_code_c, data_d),
    FOREIGN KEY (CHAMBRE_code_c) REFERENCES CHAMBRE (code_c),
    FOREIGN KEY (AGENCE_DE_VOYAGE_code_a) REFERENCES AGENCE_DE_VOYAGE (code_a)
);
CREATE TABLE SUITE (
    CHAMBRE_code_c INTEGER NOT NULL,
    PRIMARY KEY (CHAMBRE_code_c),
    FOREIGN KEY (CHAMBRE_code_c) REFERENCES CHAMBRE (code_c)
);
CREATE TABLE HAS_ESPACE_DISPO (
    ESPACE_DISPO_espace_dispo VARCHAR(200) NOT NULL,
    SUITE_CHAMBRE_code_c INTEGER NOT NULL,
    PRIMARY KEY (ESPACE_DISPO_espace_dispo, SUITE_CHAMBRE_code_c),
    FOREIGN KEY (SUITE_CHAMBRE_code_c) REFERENCES SUITE (CHAMBRE_code_c)
);
CREATE TABLE HAS_EQUIPEMENT (
    CHAMBRE_code_c INTEGER NOT NULL,
    EQUIPEMENT_equipement VARCHAR(200) NOT NULL,
    PRIMARY KEY (CHAMBRE_code_c, EQUIPEMENT_equipement),
    FOREIGN KEY (CHAMBRE_code_c) REFERENCES CHAMBRE (code_c)
);
/* =========================
   VILLE
========================= */
INSERT INTO VILLE (nom_ville, longi, lati, region, pays) VALUES
('Rabat', -6.8498, 34.0209, 'Rabat-Salé-Kénitra', 'Maroc'),
('Kénitra', -6.5802, 34.2610, 'Rabat-Salé-Kénitra', 'Maroc'),
('Casablanca', -7.5898, 33.5731, 'Casablanca-Settat', 'Maroc'),
('Marrakech', -7.9811, 31.6295, 'Marrakech-Safi', 'Maroc'),
('Fès', -5.0078, 34.0331, 'Fès-Meknès', 'Maroc'),
('Paris', 2.3522, 48.8566, 'Île-de-France', 'France'),
('Lyon', 4.8357, 45.7640, 'Auvergne-Rhône-Alpes', 'France'),
('Marseille', 5.3698, 43.2965, 'PACA', 'France'),
('Nice', 7.2619, 43.7102, 'PACA', 'France');

/* =========================
   CHAMBRE (BEAUCOUP)
========================= */
INSERT INTO CHAMBRE (code_c, surface) VALUES
(101,18),(102,20),(103,22),(104,24),(105,26),
(106,28),(107,30),(108,32),(109,34),(110,36),
(201,38),(202,40),(203,42),(204,45),(205,48),
(206,50),(207,55),(208,60),(209,65),(210,70),
(301,16),(302,17),(303,18),(304,19),(305,20),
(306,21),(307,22),(308,23),(309,24),(310,25),
(401,26),(402,27),(403,28),(404,29),(405,30),
(406,31),(407,32),(408,33),(409,34),(410,35),
(501,36),(502,38),(503,40),(504,42),(505,44),
(506,46),(507,48),(508,50),(509,55),(510,60);

/* =========================
   AGENCE_DE_VOYAGE
========================= */
INSERT INTO AGENCE_DE_VOYAGE
(code_a, site_web, telephone,
 Adresse_code_postal, Adresse_rue_a, Adresse_num_a, Adresse_pays_a,
 VILLE_nom_ville)
VALUES
(1,'https://rabat-voyage.ma','+212537000001',10000,'Av Mohammed V',10,'Maroc','Rabat'),
(2,'https://kenitra-trip.ma','+212537000002',14000,'Rue Hassan II',6,'Maroc','Kénitra'),
(3,'https://casa-travel.ma','+212522000003',20000,'Bd Zerktouni',22,'Maroc','Casablanca'),
(4,'https://marrakech-tour.ma','+212524000004',40000,'Route Ourika',8,'Maroc','Marrakech'),
(5,'https://fes-voyage.ma','+212535000005',30000,'Rue Fes Jdid',4,'Maroc','Fès'),
(6,'https://paris-holiday.fr','+33145000006',75001,'Rue Rivoli',15,'France','Paris'),
(7,'https://lyon-voyage.fr','+33472000007',69000,'Rue Lyon',20,'France','Lyon'),
(8,'https://marseille-trip.fr','+33491000008',13000,'Vieux Port',5,'France','Marseille'),
(9,'https://nice-tour.fr','+33493000009',6000,'Promenade Anglais',3,'France','Nice');

/* =========================
   SUITE
========================= */
INSERT INTO SUITE (CHAMBRE_code_c) VALUES
(203),(204),(205),(206),(207),(208),(209),(210),
(503),(504),(505),(506),(507),(508),(509),(510);

/* =========================
   HAS_EQUIPEMENT
========================= */
INSERT INTO HAS_EQUIPEMENT (CHAMBRE_code_c, EQUIPEMENT_equipement) VALUES
(101,'WiFi'),(101,'Climatisation'),
(103,'Télévision'),
(105,'Balcon'),
(203,'Jacuzzi'),
(205,'Vue sur mer'),
(207,'Piscine privée'),
(210,'Terrasse'),
(503,'Cuisine'),
(510,'Jacuzzi');

/* =========================
   HAS_ESPACE_DISPO
========================= */
INSERT INTO HAS_ESPACE_DISPO (ESPACE_DISPO_espace_dispo, SUITE_CHAMBRE_code_c) VALUES
('Salon privé',203),
('Terrasse',204),
('Piscine',205),
('Jardin',207),
('Rooftop',210),
('Salle à manger',503);

/* =========================
   RESERVATION
========================= */
INSERT INTO RESERVATION
(CHAMBRE_code_c, data_d, data_f, prix, AGENCE_DE_VOYAGE_code_a)
VALUES
(101,'2025-06-01','2025-06-05',400,1),
(102,'2025-06-10','2025-06-15',550,2),
(103,'2025-07-01','2025-07-07',700,3),
(104,'2025-07-10','2025-07-18',850,4),
(105,'2025-08-01','2025-08-10',1000,5),
(201,'2025-06-05','2025-06-12',1300,6),
(202,'2025-07-01','2025-07-10',1600,7),
(203,'2025-08-01','2025-08-15',2200,8),
(205,'2025-09-01','2025-09-20',3000,9),
(210,'2025-10-01','2025-10-25',4200,6);
