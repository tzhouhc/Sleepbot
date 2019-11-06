import re


def operate_on_strings(operator: str, sub_operand: str, operand: str) -> bool:
    if operator == "match":
        return sub_operand == operand
    elif operator == "contains_word":
        return re.search(fr"\b{sub_operand}\b", operand) is not None
    elif operator == "prefix":
        return operand.startswith(sub_operand)
    elif operator == "suffix":
        return operand.endswith(sub_operand)
    elif operator == "contains":
        return sub_operand in operand
    elif operator == "regex":
        return re.search(fr"{sub_operand}", operand) is not None
    else:  # operator not recognized
        # TODO: do actual logging instead of stdout print
        print(f"operator '{operator}' not recognized.")
        return False
