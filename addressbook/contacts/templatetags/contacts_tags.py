from django import template

register = template.Library()


@register.filter(name='grader_reveal')
def grader_reveal(value):
    """
    Return a width to a control that will reveal the underlying image to X units.

    value is the number of powers and this will assume a max of 7 (over which the all units
    are shown).
    """
    cut_off = {
        7: 100,
        6: 0,
        5: 0,
        4: 48,
        3: 32,
        2: 22,
        1: 13,
        0: 8}

    if value >= 7:
        return cut_off[7]
    elif 0 <= value < 7:
        return cut_off[int(value)]
    else:
        return 0
