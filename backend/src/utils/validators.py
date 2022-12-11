"""common validators"""


def validate_string(val):
    """do validation and checks before insert"""
    if val is not None:
        if type(val) is int:
            # for x in val:
            #   print(x)
            return str(val).encode("utf-8")
        else:
            return val
    return None
