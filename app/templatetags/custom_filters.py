from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """
    获取字典中的值，如果不存在则返回 '-'
    """
    return dictionary.get(key, '-') 

@register.filter
def get_item(dictionary, key):
    """从字典中获取指定键的值"""
    if dictionary is None:
        return '-'
    return dictionary.get(key, '-') 

@register.filter
def split_lines(text):
    """将文本按行分割"""
    if not text:
        return []
    return text.split('\n')

@register.filter
def strip(text):
    """去除文本首尾的空白字符"""
    if not text:
        return ''
    return text.strip() 