from django.contrib import admin
from django.urls import path

from quiz_app.views import question_list, home_page, result_view

admin.site.site_title = "Quiz ADMIN"
admin.site.site_header = "Quiz ADMIN"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('quiz/', question_list, name='question_list'),
    path('result/', result_view, name='result_view'),

    path('', home_page, name='home_page'),
]
