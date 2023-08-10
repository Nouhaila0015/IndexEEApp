import sqlite3

def create_tables():
    # Create Database or Connect to One
    conn = sqlite3.connect('releve.db')

    # Create a Cursor
    c = conn.cursor()

    # Create Tables
    c.execute("""CREATE TABLE IF NOT EXISTS AppData (
        Client_secteur INTEGER NOT NULL UNIQUE,
        localite TEXT,
        gerance TEXT,
        Police TEXT,
        PRIMARY KEY (Client_secteur)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS Gerance (
        id_gerance INTEGER NOT NULL UNIQUE,
        libelle TEXT,
        PRIMARY KEY (id_gerance)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS Nature_client (
        id_nature_client INTEGER NOT NULL UNIQUE,
        libelle_nat_clt TEXT,
        PRIMARY KEY (id_nature_client)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS Type_Anomalie (
        id_anomalie INTEGER NOT NULL UNIQUE,
        libelle_anom TEXT,
        PRIMARY KEY (id_anomalie)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS Releve (
        Localite INTEGER NOT NULL,
        secteur INTEGER,
        trn INTEGER,
        ord INTEGER,
        id_gerance INTEGER NOT NULL,
        id_categorie INTEGER,      
        numPolice INTEGER NOT NULL,
        nom TEXT,
        adresse TEXT,
        numCompteur INTEGER,
        NbrRoues INTEGER,
        index2 INTEGER,
        index1 INTEGER,
        CodeAnomalie INTEGER,
        last_update DATETIME,
        FOREIGN KEY (id_categorie) REFERENCES Nature_client (id_nature_client),
        FOREIGN KEY (CodeAnomalie) REFERENCES Type_Anomalie (id_anomalie),
        FOREIGN KEY (id_gerance) REFERENCES Gerance (id_gerance),
        FOREIGN KEY (Localite) REFERENCES AppData (Client_secteur),
        PRIMARY KEY (Localite, numPolice, id_gerance)
    )""")

    # Commit our changes
    conn.commit()

    # Close the connection
    conn.close()
