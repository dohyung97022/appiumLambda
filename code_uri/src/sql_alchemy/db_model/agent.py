from sqlalchemy import Column, String
from sqlalchemy_serializer import SerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base


class Agent(Base, SerializerMixin):
    __tablename__ = 'agent'
    agent_email: str = Column(String(50), primary_key=True, comment='요원 이메일')
    agent_password: str = Column(String(50), comment='요원 비밀번호')

    is_job_finished: bool = False

    def __init__(self,
                 agent_email: str = None,
                 agent_password: str = None,
                 is_job_finished: bool = None
                 ):
        self.agent_email = agent_email
        self.agent_password = agent_password
        self.is_job_finished = is_job_finished
