def format_thousands(num: int | float) -> str:
    return f"{num:_}".replace("_", " ")
