def nth(n) -> str:
    "Return the ordinal form of a number"
    number_string = str(n)
    if number_string.endswith("1"):
        return f"{number_string}st"
    elif number_string.endswith("2"):
        return f"{number_string}nd"
    elif number_string.endswith("3"):
        return f"{number_string}rd"
    else:
        return f"{number_string}th"
