from django.conf.urls import include, url
from django.contrib import admin
from zfwechat.views import *



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wechat/logout$',logout),
    url(r'^wechat/marks$',getMark),
    url(r'^wechat/login$',login),
    url(r'^wechat/wx.do$',doWechat),
    url(r'^wechat/lessons$',getLesson),
    url(r'^wechat/index$',getMain),
    url(r'^wechat/gradepoint$',getGradePoint),
    url(r'^wechat/hosts$',getHosts),
    #url(r'^wechat/sendemail$',sendEmailToStudent),
    url(r'^wechat/email$',enableEmail),


]

handler404 = pageNoFound
handler500 = pageError