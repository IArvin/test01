# -*-coding: utf-8-*-
import torndb



class defaultAetting():
    def __init__(self):
        self.sql_conn = torndb.Connection("127.0.0.1:3306", "test", user="root", password="root_pwd")