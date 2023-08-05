# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

from ..util import get_and_set_user_agent

register = template.Library()


@register.filter()
def is_mobile(request):
    return get_and_set_user_agent(request).is_mobile


@register.filter()
def is_pc(request):
    return get_and_set_user_agent(request).is_pc


@register.filter()
def is_tablet(request):
    return get_and_set_user_agent(request).is_tablet


@register.filter()
def is_bot(request):
    return get_and_set_user_agent(request).is_bot


@register.filter()
def is_touch_capable(request):
    return get_and_set_user_agent(request).is_touch_capable
