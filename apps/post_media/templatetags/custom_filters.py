from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Ambil item dari dictionary berdasarkan key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0


@register.filter
def split(value, delimiter=","):
    """Memecah string berdasarkan delimiter"""
    return value.split(delimiter)


@register.filter
def replace(value, arg):
    """
    Ganti substring dalam string.
    Contoh: {{ text|replace:"_, " }} akan mengganti "_" dengan spasi.
    """
    try:
        old, new = arg.split(',')
        return value.replace(old.strip(), new.strip())
    except Exception:
        return value


@register.filter
def metric_label(channel, key):
    """Ambil label metrik sesuai channel"""
    try:
        return channel.t_metric_label(key)
    except Exception:
        return key
