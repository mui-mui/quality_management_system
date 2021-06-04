from jinja2 import Template

def main(query, data):
    return Template(query).render(pieceIdList=[f"'{item}'" for item in data])