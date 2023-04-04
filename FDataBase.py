import sqlite3
import time
import math
import re
from flask import url_for


class FDataBase:
    def __init__(self, db):
        # db - ссылка на связь с базой данных
        self.__db = db
        self.__cur = db.cursor() # через cursor работаем с БД

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addVacancy(self, name, city, salary, schedule, description):
        try:
            # Проверка на то, существует ли запись с таким id
            # Потому что каждая вакансия должна иметь уникальный url
            # Если id равен передаваемому id, то вакансия с таким именем уже существует
            '''
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM vacancy WHERE id = {id}")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Вакансия с таким id уже существует")
                return False
            '''
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO vacancy VALUES(NULL, ?, ?, ?, ?, ?, ?)",
                               (name, city, salary, schedule, description, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления вакансии в БД "+str(e))
            return False

        return True

    # Данный метод возвращает краткое описание вакансии на отдельной странице (с новыми полями после доменного имени)
    def getVacancy(self, vacancyId):
        try:
            self.__cur.execute(f"SELECT name, description FROM vacancy WHERE id = {vacancyId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения вакансии из БД "+str(e))

        return (False, False)


    #Краткий вывод статьи
    def getVacancyAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, name, description FROM vacancy ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения вакансии из БД "+str(e))

        return []

    def getResumeInfo_1Graph(self, request_from_form):
        try:
            self.__cur.execute(f"SELECT id, sending_date_month, AVG(CAST(desired_salary AS float)) AS desired_salary FROM resume WHERE resume_type = '{request_from_form}' GROUP BY sending_date_month ORDER BY id ASC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных резюме из БД "+str(e))

    def getResumeInfo_2Graph(self, request_from_form):
        try:
            self.__cur.execute(f"SELECT id, schedule, COUNT(id) AS vacancy_ammount FROM resume WHERE resume_type = '{request_from_form}' GROUP BY schedule")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных резюме из БД "+str(e))