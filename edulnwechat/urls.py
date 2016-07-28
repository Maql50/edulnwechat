from django.conf.urls import include, url
from django.contrib import admin
from zfwechat.views import *



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wechat/logout$',logout),
    url(r'^wechat/marks$',getMark),
    url(r'^wechat/login$',login),
    url(r'^wechat/wx.do$',doGet),
    url(r'^wechat/lessons$',getLesson),
    url(r'^wechat/index$',main),
    url(r'^wechat/gradepoint$',getGradePoint),
]

handler404 = page_not_found
handler500 = page_error