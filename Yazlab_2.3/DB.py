from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class DB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_arastirmaci(self, ArastirmaciAdi,ArastirmaciSoyadi):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_arastirmaci, ArastirmaciAdi, ArastirmaciSoyadi)
    
    @staticmethod
    def _create_arastirmaci(tx,  ArastirmaciAdi, ArastirmaciSoyadi):
        query = (
            "CREATE (p1:Arastirmaci { ArastirmaciAdi:$ArastirmaciAdi, ArastirmaciSoyadi:$ArastirmaciSoyadi}) "
        )
        result = tx.run(query,  ArastirmaciAdi=ArastirmaciAdi, ArastirmaciSoyadi=ArastirmaciSoyadi)
        try:
            return [{"p1": row["p1"]["ArastirmaciAdi"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def arastirmaci_sorgu(self, ArastirmaciAdi,ArastirmaciSoyadi):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._arastirmaci_sorgu, ArastirmaciAdi, ArastirmaciSoyadi)
            i=0
            for w in result:
                i+=1
            if i == 0:
                return True
            return False
    @staticmethod
    def _arastirmaci_sorgu(tx,  ArastirmaciAdi, ArastirmaciSoyadi):
        query = (
            "MATCH (n:Arastirmaci) "
            "WHERE n.ArastirmaciAdi=$ArastirmaciAdi AND n.ArastirmaciSoyadi=$ArastirmaciSoyadi "
            "RETURN n "
        )
        result = tx.run(query,  ArastirmaciAdi=ArastirmaciAdi, ArastirmaciSoyadi=ArastirmaciSoyadi)
        return [row["n"] for row in result]

    def create_tur(self,  YayinTuru, YayinYeri):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_tur,  YayinTuru, YayinYeri)
    
    @staticmethod
    def _create_tur(tx,  YayinTuru, YayinYeri):
        query = (
            "CREATE (p1:Tur {  YayinTuru:$YayinTuru, YayinYeri:$YayinYeri}) "
        )
        result = tx.run(query,  YayinTuru=YayinTuru, YayinYeri=YayinYeri)
        try:
            return [{"p1": row["p1"]["YayinTuru"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    def tur_sorgu(self,  YayinTuru, YayinYeri):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._tur_sorgu,  YayinTuru, YayinYeri)
            i=0
            for w in result:
                i+=1
            if i == 0:
                return True
            return False
    
    @staticmethod
    def _tur_sorgu(tx,  YayinTuru, YayinYeri):
        query = (
            "MATCH (n:Tur) "
            "WHERE n.YayinTuru=$YayinTuru AND n.YayinYeri=$YayinYeri "
            "RETURN n "
        )
        result = tx.run(query,  YayinTuru=YayinTuru, YayinYeri=YayinYeri)
        return [row["n"] for row in result]


    def create_yayin(self,  YayinAdi, YayinYili):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_yayin, YayinAdi, YayinYili)
    
    @staticmethod
    def _create_yayin(tx,  YayinAdi, YayinYili):
        query = (
            "CREATE (p1:Yayin {  YayinAdi:$YayinAdi, YayinYili:$YayinYili}) "
        )
        result = tx.run(query,  YayinAdi=YayinAdi, YayinYili=YayinYili)
        try:
            return [{"p1": row["p1"]["YayinAdi"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def yayin_sorgu(self,  YayinAdi, YayinYili):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._yayin_sorgu, YayinAdi, YayinYili)
            i=0
            for w in result:
                i+=1
            if i == 0:
                return True
            return False
    
    @staticmethod
    def _yayin_sorgu(tx,  YayinAdi, YayinYili):
        query = (
            "MATCH (n:Yayin) "
            "WHERE n.YayinAdi=$YayinAdi AND n.YayinYili=$YayinYili "
            "RETURN n "
        )
        result = tx.run(query,  YayinAdi=YayinAdi, YayinYili=YayinYili)
        return [row["n"] for row in result]
    
    def a_y_c_sorgu(self,  ArastirmaciAdi, YayinAdi):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._a_y_c_sorgu, ArastirmaciAdi, YayinAdi)
            i=0
            for w in result:
                i+=1
            if i == 0:
                return True            
            return False
    
    @staticmethod
    def _a_y_c_sorgu(tx, ArastirmaciAdi, YayinAdi):
        
        query = (
            "MATCH (a:Arastirmaci WHERE a.ArastirmaciAdi= $ArastirmaciAdi)-[:WROTE]->(y:Yayin WHERE y.YayinAdi=$YayinAdi) "
            "RETURN a"
        )
        result = tx.run(query, ArastirmaciAdi=ArastirmaciAdi, YayinAdi=YayinAdi)
        return [row["a"] for row in result]

    def y_t_c_sorgu(self,   YayinAdi, YayinYeri,YayinTuru):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._y_t_c_sorgu, YayinAdi, YayinYeri,YayinTuru)
            i=0
            for w in result:
                i+=1
            if i == 0:
                return True
            return False
    
    @staticmethod
    def _y_t_c_sorgu(tx,  YayinAdi, YayinYeri,YayinTuru):
        query = (
        "MATCH (y:Yayin WHERE y.YayinAdi=$YayinAdi)-[:DIRECTED]->(t:Tur WHERE t.YayinYeri=$YayinYeri AND t.YayinTuru=$YayinTuru)"
        "RETURN y"
        )
        result = tx.run(query,  YayinAdi=YayinAdi, YayinYeri=YayinYeri, YayinTuru=YayinTuru)
        return [row["y"] for row in result]


    def create_yayin_to_tur_connection(self, YayinAdi, YayinYeri,YayinTuru):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_yayin_to_tur_connection,  YayinAdi, YayinYeri,YayinTuru)

    @staticmethod
    def _create_yayin_to_tur_connection(tx, YayinAdi, YayinYeri,YayinTuru):
        query = (
            "MATCH (y:Yayin), (t:Tur) "
            "WHERE y.YayinAdi = $YayinAdi "
            "AND t.YayinYeri = $YayinYeri AND t.YayinTuru =$YayinTuru "
            "CREATE (y)-[d:DIRECTED]->(t) "
        )
        result = tx.run(query,  YayinAdi=YayinAdi, YayinYeri=YayinYeri, YayinTuru=YayinTuru)
        try:
            return [{"p1": row["p1"]["YayinAdi"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_arastirmacilar_to_yayin_connection(self, ArastirmaciAdi, YayinAdi):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_arastirmacilar_to_yayin_connection, ArastirmaciAdi, YayinAdi)

    @staticmethod
    def _create_arastirmacilar_to_yayin_connection(tx, ArastirmaciAdi, YayinAdi):
        query = (
            "MATCH (a:Arastirmaci), (y:Yayin) "
            "WHERE y.YayinAdi = $YayinAdi AND a.ArastirmaciAdi = $ArastirmaciAdi " 
            "CREATE (a)-[w:WROTE]->(y) "
        )
        result = tx.run(query,  ArastirmaciAdi=ArastirmaciAdi, YayinAdi=YayinAdi)
        try:
            return [{"p1": row["p1"]["ArastirmaciAdi"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_ArastirmaciAdi(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_ArastirmaciAdi)
            return result

    @staticmethod
    def _find_and_return_ArastirmaciAdi(tx):
        query = (
            "MATCH (a:Arastirmaci) "
            "WHERE exists(a.ArastirmaciAdi) "
            "RETURN a.ArastirmaciAdi"
        )
        result = tx.run(query)
        return [row["a.ArastirmaciAdi"] for row in result]
        
    def find_Arastirmaci_wrote_yayin(self,ArastirmaciAdi):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_Arastirmaci_wrote_yayin, ArastirmaciAdi)
            return result

    @staticmethod
    def _find_Arastirmaci_wrote_yayin(tx,ArastirmaciAdi):
        query = (
            "MATCH (a:Arastirmaci WHERE a.ArastirmaciAdi= $ArastirmaciAdi)-[:WROTE]->(y:Yayin) "
            "RETURN y.YayinAdi"
        )
        result = tx.run(query,ArastirmaciAdi=ArastirmaciAdi)
        data = []
        for re in result:
            veri={
                "YayinAdi":""
            }
            veri.update({"YayinAdi":re["y.YayinAdi"]})
            data.append(veri)
        return data

    def find_Yayin_to_everything(self,YayinAdi):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_Yayin_to_everything, YayinAdi)
            return result

    @staticmethod
    def _find_Yayin_to_everything(tx,YayinAdi):
        query = (
            "MATCH (a:Arastirmaci)-[:WROTE]->(y:Yayin WHERE y.YayinAdi=$YayinAdi)-[DIRECTED]->(t:Tur) "
            "RETURN a.ArastirmaciAdi,a.ArastirmaciSoyadi,y.YayinAdi,y.YayinYili,t.YayinTuru,t.YayinYeri"
        )
        result = tx.run(query,YayinAdi=YayinAdi)
        data = []
        for re in result:
            veri={
                "ArastirmaciAdi":"",
                "ArastirmaciSoyadi":"",
                "YayinAdi":"",
                "YayinYili":"",
                "YayinTuru":"",
                "YayinYeri":""
            }
            veri.update({"ArastirmaciAdi":re["a.ArastirmaciAdi"]})
            veri.update({"ArastirmaciSoyadi":re["a.ArastirmaciSoyadi"]})
            veri.update({"YayinAdi":re["y.YayinAdi"]})
            veri.update({"YayinYili":re["y.YayinYili"]})
            veri.update({"YayinTuru":re["t.YayinTuru"]})
            veri.update({"YayinYeri":re["t.YayinYeri"]})
            data.append(veri)
        return data

    def find_YayinYeri(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_YayinYeri)
            
            return result
                

    @staticmethod
    def _find_and_return_YayinYeri(tx):
        query = (
            "MATCH (t:Tur) "
            "WHERE exists(t.YayinYeri) "
            "RETURN t.YayinYeri"
        )
        result = tx.run(query)
        return [row["t.YayinYeri"] for row in result]
    
    
    def find_YayinTuru(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_YayinTuru)
            return result

    @staticmethod
    def _find_and_return_YayinTuru(tx):
        query = (
            "MATCH (t:Tur) "
            "WHERE exists(t.YayinTuru) "
            "RETURN t.YayinTuru"
        )
        result = tx.run(query)
        return [row["t.YayinTuru"] for row in result]

    def find_YayinAdi(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_YayinAdi)
            return result

    @staticmethod
    def _find_and_return_YayinAdi(tx):
        query = (
            "MATCH (y:Yayin) "
            "WHERE exists(y.YayinAdi) "
            "RETURN y.YayinAdi"
        )
        result = tx.run(query)
        return [row["y.YayinAdi"] for row in result]

    def search(self,tur,kelime):
        with self.driver.session() as session:
            result = session.read_transaction(self._search,tur,kelime)
            return result

    @staticmethod
    def _search(tx,tur,kelime):
        if tur == "ArastirmaciAdi":
            query = (
                    "MATCH (a:Arastirmaci WHERE a.ArastirmaciAdi CONTAINS $kelime)-[:WROTE]->(y:Yayin )-[:DIRECTED]->(t:Tur)"
                    "RETURN a,y,t"
            )
        if tur == "ArastirmaciSoyadi":
            query = (
                    "MATCH (a:Arastirmaci WHERE a.ArastirmaciSoyadi CONTAINS $kelime)-[:WROTE]->(y:Yayin )-[:DIRECTED]->(t:Tur)"
                    "RETURN a,y,t"
            )
        if tur == "YayinTuru":
            query = (
                    "MATCH (a:Arastirmaci)-[:WROTE]->(y:Yayin )-[:DIRECTED]->(t:Tur WHERE t.YayinTuru CONTAINS $kelime)"
                    "RETURN a,y,t"
            )
        if tur == "YayinYeri":
            query = (
                    "MATCH (a:Arastirmaci)-[:WROTE]->(y:Yayin )-[:DIRECTED]->(t:Tur WHERE t.YayinYeri CONTAINS $kelime)"
                    "RETURN a,y,t"
            )
        if tur == "YayinAdi":
            query = (
                    "MATCH (a:Arastirmaci)-[:WROTE]->(y:Yayin WHERE y.YayinAdi CONTAINS $kelime)-[:DIRECTED]->(t:Tur)"
                    "RETURN a,y,t"
            )
        if tur == "YayinYili":
            query = (
                    "MATCH (a:Arastirmaci)-[:WROTE]->(y:Yayin  WHERE y.YayinYili CONTAINS $kelime)-[:DIRECTED]->(t:Tur)"
                    "RETURN a,y,t"
            )
        result = tx.run(query,kelime=kelime)
        data = []
        for a,y,t in result:
            veri = {
                    "ArastirmaciAdi":"",
                    "ArastirmaciSoyadi":"",
                    "YayinYili":"",
                    "YayinAdi":"",
                    "YayinTuru":"",
                    "YayinYeri":""
                }
            veri.update({"ArastirmaciAdi":a["ArastirmaciAdi"]})
            veri.update({"ArastirmaciSoyadi":a["ArastirmaciSoyadi"]})
            veri.update({"YayinYili":y["YayinYili"]})
            veri.update({"YayinAdi":y["YayinAdi"]})
            veri.update({"YayinTuru":t["YayinTuru"]})
            veri.update({"YayinYeri":t["YayinYeri"]})
            data.append(veri)

        return data

if __name__ == "__main__":
    uri = "neo4j+s://7255dd1c.databases.neo4j.io:7687"
    user = "neo4j"
    password = "6_IY0TgpQv-_up8zfi7JsSd_2Sh-piLj6ZTJsZpcKmo"
    DB = DB(uri, user, password)
    DB.find_arastirmaci()
    DB.find_tur()
    DB.find_yayin()
    DB.close()

