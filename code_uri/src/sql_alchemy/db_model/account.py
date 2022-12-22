from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from src.sql_alchemy.domain.sql_alchemy import Base


class Account(Base):
    __tablename__ = 'account'
    account_seq: int = Column(Integer, primary_key=True, comment='회원 일렬번호')
    account_email: str = Column(String(30), comment='회원 이메일')
    account_username: str = Column(String(50), comment='회원 이름')
    account_pw: str = Column(String(50), comment='회원 비밀번호')
    udid: str = Column(String(30), comment='핸드폰 고유번호')
    site: str = Column(String(100), comment='회원 자동화 사이트')
    cookies: str = Column(String(5000), comment='회원 쿠키')
    last_action_date: datetime = Column(DateTime, comment='회원 마지막 행동 시간')

    def __init__(self,
                 account_seq: int = None,
                 account_email: str = None,
                 account_username: str = None,
                 account_pw: str = None,
                 udid: str = None,
                 site: str = None,
                 cookies: str = None,
                 last_action_date: datetime = None
                 ):
        self.account_seq = account_seq
        self.account_email = account_email
        self.account_username = account_username
        self.account_pw = account_pw
        self.udid = udid
        self.site = site
        self.cookies = cookies
        self.last_action_date = last_action_date
