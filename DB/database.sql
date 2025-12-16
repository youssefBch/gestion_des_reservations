DROP DATABASE gestion_db;
CREATE DATABASE hotel;
USE hotel;
-- --------------------------------------------------------

--
-- Structure de la table `CITY`
--

CREATE TABLE CITY (
  Name VARCHAR(32) NOT NULL,
  Latitude FLOAT,
  Longitude FLOAT,
  Country VARCHAR(32),
  Region VARCHAR(32) NOT NULL,
  PRIMARY KEY (Name)
);


-- --------------------------------------------------------


CREATE TABLE TRAVEL_AGENCY (
  `CodA` int NOT NULL,
  `WebSite` varchar(32) DEFAULT NULL,
  `Tel` varchar(32) NOT NULL,
  `Street_Address` varchar(32) NOT NULL,
  `ZIP_Address` int NOT NULL,
  `City_Address` varchar(32) NOT NULL,
  `Num_Address` int NOT NULL,
  `Country_Address` varchar(32) NOT NULL,
  PRIMARY KEY (`CodA`),
  FOREIGN KEY (`City_Address`) REFERENCES `CITY` (`Name`)
);


-- --------------------------------------------------------

--
-- Structure de la table `ROOM`
--

CREATE TABLE ROOM (
  `CodR` int NOT NULL,
  `Floor` int NOT NULL,
  `SurfaceArea` int NOT NULL,
  `Type` varchar(32) NOT NULL,
  PRIMARY KEY (`CodR`)
);


-- Structure de la table `HAS_AMENITIES`
--

CREATE TABLE HAS_AMENITIES (
  `AMENITIES_Amenity` varchar(32) NOT NULL,
  `ROOM_CodR` int NOT NULL,
  PRIMARY KEY (AMENITIES_Amenity, ROOM_CodR),
  FOREIGN KEY (ROOM_CodR) REFERENCES ROOM(CodR)
);


-- --------------------------------------------------------

--
-- Structure de la table `HAS_SPACES`
--

CREATE TABLE HAS_SPACES (
  `SPACES_Space` varchar(32) NOT NULL,
  `ROOM_CodR` int NOT NULL,
  PRIMARY KEY (SPACES_Space, ROOM_CodR),
  FOREIGN KEY (ROOM_CodR) REFERENCES ROOM(CodR)
);


-- --------------------------------------------------------

--
-- Structure de la table `BOOKING`
--

CREATE TABLE BOOKING (
  ROOM_CodR INT NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE NOT NULL,
  Cost DOUBLE NOT NULL,
  TRAVEL_AGENCY_CodA INT NOT NULL,
  PRIMARY KEY (ROOM_CodR, StartDate),
  FOREIGN KEY (ROOM_CodR) REFERENCES ROOM(CodR),
  FOREIGN KEY (TRAVEL_AGENCY_CodA) REFERENCES TRAVEL_AGENCY(CodA)
);


-- --------------------------------------------------------