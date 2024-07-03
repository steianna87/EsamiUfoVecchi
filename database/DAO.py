from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct year(`datetime`) as y
                    from sighting s 
                    order by y desc"""

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['y'])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAllShape():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct shape 
                    from sighting s 
                    order by shape  """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getStateSight():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct state 
                        from sighting s 
                        order by state  """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['state'])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getCity(state):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct s.city 
                    from sighting s 
                    where s.state = %s"""

        cursor.execute(query, (state, ))
        result = []
        for row in cursor:
            result.append(row['city'])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getCity2(shape, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct s.city 
                        from sighting s 
                        where s.shape = %s and year (s.`datetime`) = %s"""

        cursor.execute(query, (shape, year))
        result = []
        for row in cursor:
            result.append(row['city'])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getEdgeW(shape, state):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select s.city as c1 , s2.city as c2, count(*) as peso
                    from sighting s , sighting s2 
                    where s.city < s2.city and year (s2.`datetime`) = year (s.`datetime`)
                    and s2.shape = %s and s.shape = s2.shape 
                    and s2.state = %s and s.state = s2.state
                    group by s.city , s2.city """

        cursor.execute(query, (shape, state))
        result = []
        for row in cursor:
            result.append((row['c1'], row['c2'], row['peso']))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getEdgeW2(shape, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select s.city as c1, s2.city as c2, (count(distinct s.id) + count(distinct s2.id)) as peso 
                    from sighting s , sighting s2 
                    where s.id < s2.id and s.city != s2.city and month (s.`datetime`) = month (s2.`datetime`)
                    and s.shape = s2.shape and s2.shape = %s
                    and year (s.`datetime`) = year (s2.`datetime`) and year (s2.`datetime`) = %s
                    group by s.city , s2.city """

        cursor.execute(query, (shape, year))
        result = []
        for row in cursor:
            result.append((row['c1'], row['c2'], row['peso']))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAllStates():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select *
                    from state s """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(State(**row))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAllVicini(Map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select state1 , state2 
                    from neighbor n """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append((Map[row['state1']], Map[row['state2']]))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getPeso(year, shape, s1: State):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select s.state , count(*) as peso
                    from sighting s
                    where year(s.`datetime`) = %s 
                    and s.shape = %s 
                    and s.state = %s"""

        cursor.execute(query, (year, shape, s1.id))
        result = []
        for row in cursor:
            result.append(row['peso'])

        cursor.close()
        cnx.close()
        return result
