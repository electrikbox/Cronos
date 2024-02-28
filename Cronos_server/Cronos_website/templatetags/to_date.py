from django import template

register = template.Library()

@register.filter
def to_date(value):
    mappings = {
        "*": "every",
        "mon": "Monday",
        "tue": "Tuesday",
        "wed": "Wednesday",
        "thu": "Thursday",
        "fri": "Friday",
        "sat": "Saturday",
        "sun": "Sunday",
        "jan": "January",
        "feb": "February",
        "mar": "March",
        "apr": "April",
        "may": "May",
        "jun": "June",
        "jul": "July",
        "aug": "August",
        "sep": "September",
        "oct": "October",
        "nov": "November",
        "dec": "December",
    }
    return mappings.get(value, value)


@register.filter
def to_double_digit(value):
    return str(value).zfill(2)


@register.filter
def rm_http(value: str):

    new_value = value.split(" ")[-1]

    if new_value.startswith("http://www."):
        value = value.replace("http://www.", " ")

    elif new_value.startswith("https://www."):
        value = value.replace("https://www.", " ")

    elif new_value.startswith("https://"):
        value = value.replace("https://", " ")

    elif new_value.startswith("http://"):
        value = value.replace("http://", " ")

    return value
