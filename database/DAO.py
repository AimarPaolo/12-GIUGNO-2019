from database.DB_connect import DBConnect
from model.condiment import Condiment


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNodi(calorie):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.condiment_code as condiment_code, c.display_name as display_name, c.condiment_calories as condiment_calories
from condiment c 
where c.condiment_calories < %s"""
        cursor.execute(query, (calorie, ))
        for row in cursor:
            result.append(
                Condiment(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArchi(n1, n2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct fc2.food_code) as cont
from food_condiment fc, food_condiment fc2, condiment c, condiment c2 
where fc.food_code = fc2.food_code 
and fc2.condiment_code = %s
and fc.condiment_code = %s
"""
        cursor.execute(query, (n1, n2, ))
        for row in cursor:
            result.append(row["cont"])
        cursor.close()
        conn.close()
        print(result)
        return result[0]
