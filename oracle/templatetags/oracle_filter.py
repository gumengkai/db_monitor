from django import template
from assets.models import OracleList
register = template.Library()

@register.filter(name='oracle_version_choices')
def oracle_version_choices(value):
    return OracleList.DB_VERSION
