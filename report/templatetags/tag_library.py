from django import template
from datetime import datetime,timedelta
import re
import locale

register = template.Library()

@register.filter()

def plaka_duzenle(plaka):
    # Sayı ve harfleri ayırma
    plaka_duzenli = re.sub(r'(\d+)([a-zA-Z]+)(\d+)', r'\1 \2 \3', plaka)
    return plaka_duzenli

@register.filter()
def date_day(value):
    value = value + timedelta(hours=3)
    dateNow = datetime.now()
    dakika = int(dateNow.time().strftime('%M'))-int(value.time().strftime('%M'))
    saat =int(dateNow.time().strftime('%H'))-int(value.time().strftime('%H'))
    if (saat == 0) and (dakika <= 3):
        return True
    else:   
        return False

@register.filter()
def to_int(value):
    return float(value)

@register.simple_tag
def subtract(value, arg):
    return value - arg

@register.filter()
def to_start(value):
    return (value-1)*10

@register.simple_tag
def my_url(value,field_name,urlencode=None):
    url = '?{}={}'.format(field_name,value)
    
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0]!=field_name,querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url,encoded_querystring)
        
    return url


@register.filter
def format_number(value):
    """
    Sayıyı 1000'lik dilimlerle ayırır ve binlik ayırıcı (nokta) kullanır.
    """
    try:
        # Sayıyı formatla
        value = float(value)
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Amerikan İngilizcesi formatını kullan
        return locale.format_string("%0.0f", value, grouping=True)
    except (ValueError, TypeError):
        return value