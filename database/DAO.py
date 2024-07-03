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
    def getYearAndSight():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select year (s.`datetime`) as y, count(id) as tot
                    from sighting s 
                    group by year (s.`datetime`)
                    order by year (s.`datetime`) desc"""

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append((row['y'], row['tot']))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getStatesBy(year, Map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct s.state 
                    from sighting s 
                    where year (s.`datetime`) = %s"""

        cursor.execute(query, (year, ))
        result = []
        for row in cursor:
            result.append(Map[row['state'].upper()])

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
                    from neighbor n 
                    where state1 < state2"""

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append((Map[row['state1']], Map[row['state2']]))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getPesoBy(year, shape, s1: State):
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

    @staticmethod
    def getAllPesi(idMap, year, shape):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select n.state1 , n.state2, count(*) as peso 
                        from sighting s , neighbor n 
                        where (n.state1 = s.state or n.state2 = s.state) 
                        and year (s.`datetime`) = %s and s.shape = %s and n.state1 < n.state2
                        group by n.state1 , n.state2  
                        order by n.state1 , n.state2  """

        cursor.execute(query, (year, shape))

        result = []
        for row in cursor:
            result.append((idMap[row['state1']], idMap[row['state2']], row['peso']))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAllPesiDeltDay(idMap, day, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select n.state1 , n.state2 , (count(distinct s.id) + count(distinct s2.id)) as peso
                    from sighting s , sighting s2 , neighbor n 
                    where datediff(s.`datetime`, s2.`datetime`) <= %s and s.id != s2.id 
                    and year (s.`datetime`) = year (s2.`datetime`) and year (s2.`datetime`) = %s
                    and s2.state = n.state2 and s.state = n.state1 and n.state1 < n.state2 
                    group by n.state1 , n.state2  """

        cursor.execute(query, (day, year))

        result = []
        for row in cursor:
            result.append((idMap[row['state1']], idMap[row['state2']], row['peso']))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getSightings(year, Map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select id , state , `datetime` as date
                    from sighting s 
                    where year (s.`datetime`) = %s"""

        cursor.execute(query, (year, ))
        result = []
        for row in cursor:
            result.append((Map[row['state'].upper()], (row['id'], row['date'])))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getArchi(year, Map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select s.state as s1, s2.state as s2
                    from sighting s , sighting s2 
                    where s.state != s2.state and s2.`datetime` > s.`datetime` 
                    and year (s.`datetime`) = %s and year (s2.`datetime`) = %s """

        cursor.execute(query, (year, year))
        result = []
        for row in cursor:
            result.append((Map[row['s1'].upper()], Map[row['s2'].upper()]))

        cursor.close()
        cnx.close()
        return result


