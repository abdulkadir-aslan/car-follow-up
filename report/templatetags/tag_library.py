from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return float(value)

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
