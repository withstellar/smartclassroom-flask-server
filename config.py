# encoding: utf-8
# _*_ coding: utf-8 _*_
# author: wong
# date: 2019-08-16

# dialect+driver://username:password@host:port/database

DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '********'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'facedata'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
