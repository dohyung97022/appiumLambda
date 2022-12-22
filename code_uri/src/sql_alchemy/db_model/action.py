from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.sql_alchemy.domain.sql_alchemy import Base
from sqlalchemy_serializer import SerializerMixin


class Action(Base, SerializerMixin):
    __tablename__ = 'action'
    action_seq: int = Column(Integer, primary_key=True, comment='행동 일렬번호')
    name: str = Column(String(100), index=True, comment='행동 이름')
    is_root: bool = Column(Boolean, comment='행동의 주체 여부')

    macros = relationship("Macro", back_populates="action", lazy="joined", order_by="Macro.macro_order")

    child_action_associations = relationship('ActionActionAssociation', foreign_keys='ActionActionAssociation.parent_action_seq', lazy="joined", order_by="asc(ActionActionAssociation.association_order)")
    parent_action_associations = relationship('ActionActionAssociation', foreign_keys='ActionActionAssociation.child_action_seq', lazy="noload")

    def __init__(self,
                 action_seq: int = None,
                 name: str = None,
                 is_root: bool = None,
                 action_json: dict = None
                 ):
        self.action_seq = action_seq
        self.name = name
        self.is_root = is_root

        if action_json is not None:
            self.apply_json(action_json)

    def apply_json(self, action_json: dict):
        self.action_seq = action_json['action_seq']
        self.name = action_json['name']
        self.is_root = action_json['is_root']

    def get_child_action_association_of_seq(self, child_action_seq: int):
        if child_action_seq is None:
            return None
        return next(filter(
            lambda child_action_association: child_action_association.child_action_seq == child_action_seq,
            self.child_action_associations), None)

    def get_child_action_associations_not_in(self, action_seqs: list):
        return list(filter(
            lambda child_action_association: child_action_association.child_action_seq not in action_seqs,
            self.child_action_associations))

    @classmethod
    def get_all_action_seq_from_action_json(cls, action_json: dict) -> list:
        all_actions = []

        for child_action_association_json in action_json['child_action_associations']:
            recursive_actions = Action.get_all_action_seq_from_action_json(child_action_association_json['child_action'])
            all_actions.extend(recursive_actions)

        if action_json['action_seq'] is not None:
            all_actions.append(action_json['action_seq'])

        return list(set(all_actions))

    @classmethod
    def get_action_of_seq_from_actions(cls, actions: list, action_seq: int):
        if action_seq is None:
            return None
        return next(filter(
            lambda requested_action: requested_action.action_seq == action_seq,
            actions), None)

    @classmethod
    def get_child_action_seqs_from_action_json(cls, action_json: dict):
        return list(map(
            lambda child_action_association: child_action_association['child_action_seq'],
            action_json['child_action_associations']))

    def get_macro_of_seq(self, macro_seq: int):
        if macro_seq is None:
            return None
        return next(filter(
            lambda macro: macro.macro_seq == macro_seq,
            self.macros), None)

    def get_macros_not_in(self, macro_seqs: list):
        return list(filter(
            lambda macro: macro.macro_seq not in macro_seqs,
            self.macros))

    @classmethod
    def get_macro_seqs_from_action_json(cls, action_json):
        return list(map(
            lambda macro: macro['macro_seq'],
            action_json['macros']))
