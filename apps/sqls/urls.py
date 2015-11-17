# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include

urlpatterns = patterns('sqls.views',
    (r'^admin/do_sql/', 'do_sql'),  # ajax admin method
)
