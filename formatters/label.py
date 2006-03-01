def author_year(e):
    return e.authors[0].format('ll')[:3] + e['year'][-2:]

def number(e):
    return str(e.number)
