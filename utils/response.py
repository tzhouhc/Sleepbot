def operate_on_strings(operator: str, sub_operand: str, operand: str) -> bool:
    if operator == "match":
        return sub_operand == operand
    elif operator == "prefix":
        return operand.startswith(sub_operand)
    elif operator == "suffix":
        return operand.endswith(sub_operand)
    elif operator == "contains":
        return sub_operand in operand
    else:  # operator not recognized
        # TODO: do actual logging instead of stdout print
        print(f"operator '{operator}' not recognized.")
        return False
