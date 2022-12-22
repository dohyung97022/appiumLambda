from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

import pymysql

# pymysql 사용
pymysql.install_as_MySQLdb()

# 연결 설정
engine = create_engine(
    f'mysql'
    f'://dohyung97022'
    f':9347314da!'
    f'@appium.c8lf74vqhony.ap-northeast-2.rds.amazonaws.com'
    f':3306'
    f'/appium_api'
    f'?charset=utf8')

# db 베이스
Base = declarative_base()

# 세션을 통해 db 와 연결
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
