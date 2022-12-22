from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from src.sql_alchemy.domain.sql_alchemy import Base


class ScrapedVideo(Base):
    __tablename__ = 'scraped_video'
    scraped_video_seq: int = Column(Integer, primary_key=True, comment='동영상 식별번호')
    video_url: str = Column(String(500), nullable=False, comment='동영상 url')
    s3_object: str = Column(String(500), comment='다운로드된 동영상 s3')
    origin: str = Column(String(20), nullable=False, comment='추출 위치')
    title: str = Column(String(200), default='', nullable=False, comment='동영상 제목')
    tags: str = Column(String(300), default='', nullable=False, comment='동영상 태그')
    duration: int = Column(Integer, default=0, nullable=False, comment='동영상 지속시간')
    uploaded_account_seq: int = Column(Integer, comment='업로드된 계정 식별번호')
    uploaded_views: int = Column(Integer, default=0, nullable=False, comment='업로드 조회수')
    is_scraped: bool = Column(Boolean, default=0, nullable=False, comment='스크래이핑 된 여부')
    is_deleted: bool = Column(Boolean, default=0, nullable=False, comment='스크레이핑시 삭제된 여부')
    is_uploaded: bool = Column(Boolean, default=0, nullable=False, comment='동영상 자동 업로드 여부')
    is_downloaded: bool = Column(Boolean, default=0, comment='동영상 s3 다운로드 여부')
    reg_date: DateTime = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_date: DateTime = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,
                 scraped_video_seq: int = None,
                 video_url: str = None,
                 s3_object: str = None,
                 origin: str = None,
                 title: str = None,
                 tags: str = None,
                 duration: int = None,
                 uploaded_account_seq: int = None,
                 uploaded_views: int = None,
                 is_scraped: bool = None,
                 is_deleted: bool = None,
                 is_uploaded: bool = None,
                 is_downloaded: bool = None,
                 reg_date: DateTime = None,
                 update_date: DateTime = None,
                 ):
        self.scraped_video_seq = scraped_video_seq
        self.video_url = video_url
        self.s3_object = s3_object
        self.origin = origin
        self.title = title
        self.tags = tags
        self.duration = duration
        self.uploaded_account_seq = uploaded_account_seq
        self.uploaded_views = uploaded_views
        self.is_scraped = is_scraped
        self.is_deleted = is_deleted
        self.is_uploaded = is_uploaded
        self.is_downloaded = is_downloaded
        self.reg_date = reg_date
        self.update_date = update_date

    def get_tags(self):
        tags = self.tags.replace('[', '')
        tags = tags.replace(']', '')
        tags = tags.replace("'", '')
        tags = tags.replace(" ", '')
        return tags.split(',')
