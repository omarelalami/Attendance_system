import mysql.connector

class Etudiant:
    def __init__(self, id_etudiant, nom, prenom, date_naissance):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance

class Filiere:
    def __init__(self, id_filiere, nom):
        self.id_filiere = id_filiere
        self.nom = nom


class Seance:
    def __init__(self, id_seance, date_seance, heure_debut, heure_fin):
        self.id_seance = id_seance
        self.date_seance = date_seance
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin


class Matiere:
    def __init__(self, id_matiere, nom_matiere):
        self.id_matiere = id_matiere
        self.nom_matiere = nom_matiere

class Inscription:
    def __init__(self, id_inscription, annee_universitaires, niveau, diplome, id_fil, id_etu):
        self.id_inscription = id_inscription
        self.annee_universitaires = annee_universitaires
        self.niveau = niveau
        self.diplome = diplome
        self.id_fil = id_fil
        self.id_etu = id_etu

class Presence:
    def __init__(self, id_presence, status, date_presence, heure_presence, id_etu, id_se):
        self.id_presence = id_presence
        self.status = status
        self.date_presence = date_presence
        self.heure_presence = heure_presence
        self.id_etu = id_etu
        self.id_se = id_se

class Gerer:
    def __init__(self,id_matiere,id_filiere,id_seance):
        self.id_gerer=None
        self.id_matiere = id_matiere
        self.id_filiere = id_filiere
        self.id_seance=id_seance


class MySQLDatabase:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def insert_etudiant(self, etudiant):
        query = f"INSERT INTO ETUDIANT VALUES ('{etudiant.id_etudiant}', '{etudiant.nom}', '{etudiant.prenom}', '{etudiant.date_naissance}')"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_inscription (self, inscription):
        query = f"INSERT INTO INSCRIPTION VALUES ('{inscription.id_inscription}', '{inscription.annee_universitaires}', '{inscription.niveau}', '{inscription.diplome}', '{inscription.id_fil}', '{inscription.id_etu}')"
        self.cursor.execute (query)
        self.connection.commit ()



    # Define similar methods for the other tables
    def insert_matiere (self, matiere):
        """
        Inserts a Matiere object into the database.
        """
        query = "INSERT INTO matiere (id_matiere, nom_matiere) VALUES (%s, %s)"
        values = (matiere.id_matiere, matiere.nom_matiere)
        self.cursor.execute (query, values)
        self.connection.commit ()

    def insert_gerer (self, gerer):
        """
        Inserts a Gerer object into the database.
        """
        query = "INSERT INTO gerer (ID_MA, ID_FI, ID_SE) VALUES (%s, %s, %s)"
        values = (gerer.id_matiere, gerer.id_filiere, gerer.id_seance)
        self.cursor.execute (query, values)
        self.connection.commit ()

    def insert_seance (self, seance):
        """
        Inserts a Seance object into the database.
        """
        query = "INSERT INTO seance (id_seance, date_seance, heure_debut, heure_fin) VALUES (%s, %s, %s, %s)"
        values = (seance.id_seance, seance.date_seance, seance.heure_debut, seance.heure_fin)
        self.cursor.execute (query, values)
        self.connection.commit ()

    def get_all_etudiants(self):
        query = "SELECT * FROM ETUDIANT"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        etudiants = []
        for row in result:
            etudiant = Etudiant(row[0], row[1], row[2], row[3])
            etudiants.append(etudiant)
        return etudiants

    def insert_filiere(self, filiere):
        query = f"INSERT INTO FILIERE VALUES ('{filiere.id_filiere}', '{filiere.nom}')"
        self.cursor.execute(query)
        self.connection.commit()

    def getAllFiliere(self):
        query = "SELECT NOM FROM FILIERE"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        names = []
        for row in result:
            name = row [0]
            names.append(name)
        return names

    def getMatiere(self, filiere):
        query = "SELECT distinct M.NOM_MATIERE FROM FILIERE F, Matiere M, GERER G WHERE F.NOM=%s AND F.id_filiere=G.ID_FI AND G.id_ma=M.id_matiere"
        self.cursor.execute(query, (filiere,))
        result = self.cursor.fetchall()

        names = []
        for row in result:
            name = row [0]
            names.append(name)

        return names

    def getSeance(self, matiere, filiere):
        query = "SELECT S.DATE_SEANCE,HEURE_DEBUT,HEURE_FIN FROM FILIERE F, Matiere M, GERER G, SEANCE S WHERE M.nom_matiere=%s AND F.NOM=%s AND F.id_filiere=G.ID_FI AND G.id_ma=M.id_matiere AND S.id_seance=G.id_se"
        self.cursor.execute(query, (matiere, filiere))
        result = self.cursor.fetchall()

        seance_dates = []
        for row in result:
            seance_date = row [0]+' | '+row[1]+' - '+row[2]
            seance_dates.append(seance_date)

        return seance_dates

    def get_presence_data(self, matiere, filiere,seance,heure_debut,heure_fin):
        query = "SELECT distinct E.Id_etudiant, E.NOM, E.PRENOM, P.status FROM FILIERE F, Matiere M, GERER G, SEANCE S,\
         PRESENCE P, ETUDIANT E,INSCRIPTION I WHERE M.nom_matiere=%s AND F.NOM=%s AND F.id_filiere=G.ID_FI \
            AND G.id_ma=M.id_matiere AND S.id_seance=G.id_se AND F.id_filiere=I.ID_FIL AND P.id_etu=E.ID_ETUDIANT AND S.DATE_SEANCE=%s and  S.ID_SEANCE=P.ID_SE and HEURE_DEBUT=%s and HEURE_FIN=%s"

        self.cursor.execute(query, (matiere, filiere,seance,heure_debut,heure_fin))
        result = self.cursor.fetchall()

        presence_data = []
        for row in result:
            id_etudiant = row [0]
            nom = row [1]
            prenom = row [2]
            statut = row [3]

            presence_data.append((id_etudiant, nom, prenom, statut))

        return presence_data

    def set_presence_data(self,date_presence,heure_presence,id_etu):
        status='PR'
        query1="SELECT S.ID_SEANCE FROM ETUDIANT E,INSCRIPTION I,FILIERE F,GERER G,SEANCE S WHERE E.ID_ETUDIANT=%s \
              AND I.ID_FIL =F.ID_FILIERE AND F.ID_FILIERE=G.ID_FI AND S.ID_SEANCE =G.ID_SE AND E.ID_ETUDIANT=I.ID_ETU\
              AND TIMESTAMPDIFF(MINUTE, CONCAT(DATE_SEANCE, ' ', HEURE_FIN), NOW()) <=0 AND TIMESTAMPDIFF(MINUTE, CONCAT(DATE_SEANCE, ' ', HEURE_DEBUT), NOW())>=0 "
        self.cursor.execute(query1, (id_etu,))
        result = self.cursor.fetchall()

        if result:
            query = "INSERT INTO PRESENCE (status,date_presence,heure_presence,id_etu,id_se) VALUES (%s, %s, %s,%s,%s)"
            self.cursor.execute(query, (status,date_presence,heure_presence,id_etu,result[0][0]))

            self.connection.commit()



    # def get_etudiant_bytime(self):
    #
    #     query = "SELECT E.ID_ETUDIANT FROM ETUDIANT E,INSCRIPTION I,FILIERE F,GERER G,SEANCE S WHERE E.ID_ETUDIANT=I.ID_ETU \
    #     AND I.ID_FIL =F.ID_FILIERE AND F.ID_FILIERE=G.ID_FI AND S.ID_SEANCE =G.ID_SE AND DATEDIFF(STR_TO_DATE(DATE_SEANCE, '%Y-%m-%d'), CURDATE())=0\
    #      AND TIMESTAMPDIFF(MINUTE, STR_TO_DATE(HEURE_DEBUT, '%H:%i'), NOW()) <=60"
    #     self.cursor.execute(query)
    #     result = self.cursor.fetchall()
    #     etudiants = []
    #     for row in result:
    #
    #         etudiants.append(row [0])
    #     return etudiants

    def get_etudiant_byday(self):
        query = "SELECT E.ID_ETUDIANT FROM ETUDIANT E,INSCRIPTION I,FILIERE F,GERER G,SEANCE S WHERE E.ID_ETUDIANT=I.ID_ETU \
              AND I.ID_FIL =F.ID_FILIERE AND F.ID_FILIERE=G.ID_FI AND S.ID_SEANCE =G.ID_SE AND DATEDIFF(STR_TO_DATE(DATE_SEANCE, '%Y-%m-%d'), CURDATE())=0"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        etudiants = []
        for row in result:
            etudiants.append(row [0])
        return etudiants
    def if_etudiant(self, id_etudiant):
        query1="SELECT S.ID_SEANCE FROM ETUDIANT E,INSCRIPTION I,FILIERE F,GERER G,SEANCE S WHERE E.ID_ETUDIANT=%s \
              AND I.ID_FIL =F.ID_FILIERE AND F.ID_FILIERE=G.ID_FI AND S.ID_SEANCE =G.ID_SE AND E.ID_ETUDIANT=I.ID_ETU\
              AND TIMESTAMPDIFF(MINUTE, CONCAT(DATE_SEANCE, ' ', HEURE_FIN), NOW()) <=0 AND TIMESTAMPDIFF(MINUTE, CONCAT(DATE_SEANCE, ' ', HEURE_DEBUT), NOW())>=0 "

        query2 = "SELECT P.ID_ETU FROM SEANCE S, PRESENCE P WHERE (DATEDIFF(STR_TO_DATE(DATE_SEANCE, '%Y-%m-%d'), CURDATE()) = 0 AND \
        TIMESTAMPDIFF(MINUTE, STR_TO_DATE(HEURE_FIN, '%H:%i'), NOW()) <= 5 AND P.ID_ETU = %s AND P.ID_SE=S.ID_SEANCE )"


        self.cursor.execute(query1, (id_etudiant,))
        result = self.cursor.fetchall()
        self.cursor.execute(query2, (id_etudiant,))
        result1=self.cursor.fetchall()
        b=False
        a=False
        if result:
            a=True
        if result1:
            b=True


        if a==True and b==False:
            return True
        else :
            print(a,b)
            return False
    def close_connection(self):
        self.connection.close()











