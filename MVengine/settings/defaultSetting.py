# -*-coding: utf-8-*-
import torndb



class defaultAetting():
    def __init__(self):
        self.sql_conn = torndb.Connection("47.92.75.190:3306", "test", user="zanhao", password="zanhao1212")