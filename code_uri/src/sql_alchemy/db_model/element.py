import enum

from selenium.webdriver.common.by import By
from sqlalchemy import Column, Integer, Enum, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base


class ElementType(enum.Enum):
    ID = "ID"
    XPATH = "XPATH"
    LINK_TEXT = "LINK_TEXT"
    PARTIAL_LINK_TEXT = "PARTIAL_LINK_TEXT"
    NAME = "NAME"
    TAG_NAME = "TAG_NAME"
    CLASS_NAME = "CLASS_NAME"
    CSS_SELECTOR = "CSS_SELECTOR"

    def to_element_by(self):
        if self is ElementType.ID: return By.ID
        if self is ElementType.XPATH: return By.XPATH
        if self is ElementType.LINK_TEXT: return By.LINK_TEXT
        if self is ElementType.PARTIAL_LINK_TEXT: return By.PARTIAL_LINK_TEXT
        if self is ElementType.NAME: return By.NAME
        if self is ElementType.TAG_NAME: return By.TAG_NAME
        if self is ElementType.CLASS_NAME: return By.CLASS_NAME
        if self is ElementType.CSS_SELECTOR: return By.CSS_SELECTOR


class Element(Base, SerializerMixin):
    serialize_rules = ('-macro',)

    __tablename__ = 'element'
    element_seq: int = Column(Integer, primary_key=True, comment='element 일렬번호')
    macro_seq: int = Column(Integer, ForeignKey("macro.macro_seq"), nullable=False, comment='macro 일렬번호')
    value: str = Column(String(500), nullable=False)
    index: int = Column(SmallInteger, nullable=False, default=0, comment='element 조회 인덱스, -1 일 경우 random')
    type: ElementType = Column(Enum(ElementType), nullable=False, default=ElementType.XPATH, comment='element 종류')
    order: int = Column(SmallInteger, nullable=False, default=0, comment='element 탐색 순서')

    macro = relationship("Macro", back_populates="elements", lazy="noload")

    def __init__(self,
                 element_seq: int = None,
                 macro_seq: int = None,
                 value: str = None,
                 index: int = None,
                 type: ElementType = None,
                 order: int = None,
                 element_json: dict = None
                 ):
        self.element_seq = element_seq
        self.macro_seq = macro_seq
        self.value = value
        self.index = index
        self.type = type
        self.order = order

        if element_json is not None:
            self.apply_json(element_json)

    def apply_json(self, element_json: dict):
        self.element_seq = element_json['element_seq']
        self.macro_seq = element_json['macro_seq']
        self.value = element_json['value']
        self.index = element_json['index']
        self.type = ElementType[element_json['type']]
        self.order = element_json['order']
