from src.sql_alchemy.db_model.action import Action
from src.sql_alchemy.domain.sql_alchemy import session


# 행동 반환
def select_action(action_seq) -> Action:
    return session().query(Action)\
                  .filter(Action.action_seq == action_seq)\
                  .one()
