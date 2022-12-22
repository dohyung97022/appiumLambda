from operator import lt, le, eq, ne, ge, gt
from src.utils.operator.domain.parse_comparison_operator_res import ParseComparisonOperatorRes
from src.utils.string import string_utils

parse_to_comparison_operator = {'<': lt, '<=': le, '==': eq, '!=': ne, '>=': ge, '>': gt}


def parse_comparison_operator(string: str) -> (bool, ParseComparisonOperatorRes):

    for parse, operator in parse_to_comparison_operator.items():
        if parse not in string:
            continue

        _, before = string_utils.get_before(string=string, before=parse)
        _, after = string_utils.get_after(string=string, after=parse)

        return True, ParseComparisonOperatorRes(before=before, operator=operator, after=after)

    return False, None
