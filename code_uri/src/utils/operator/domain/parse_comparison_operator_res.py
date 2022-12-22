class ParseComparisonOperatorRes:
    before: str
    operator: callable
    after: str

    def __init__(self, before: str, operator: callable, after: str):
        self.before = before
        self.operator = operator
        self.after = after
