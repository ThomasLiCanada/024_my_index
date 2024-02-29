# project urls.py

from django.contrib import admin
from django.urls import path, include
from websites.views import *
from django.http import HttpResponse
from django.shortcuts import render


def urls_list(request):
    return render(request, 'urls_list.html', {})  # templates/urls_list.html


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', urls_list, name='urls_list'),
    path('main_page/', main_page_view, name='main_page'),

    path('input_index/', input_index_view, name='input_index'),
    path('input_index_category/', input_index_category_view, name='input_index_category'),
    path('input_index_and_index_category/', input_index_and_index_category_view, name='input_index_and_index_category'),

    path('output_index_list/', output_index_list_view, name='output_index_list'),
    # path('', output_index_list_view, name='output_index_list'),  # as home page

    path('record_click/<int:index_id>/', record_click, name='record_click'),  # recode click date and times

    path('input_todotask/', input_todotask_view, name='input_todotask'),
    path('mark-done/<int:task_id>/', mark_task_done, name='mark-task-done'),  # mark to do task done
    path('update_todotask_view/<str:pk>', update_todotask_view, name="update_todotask_view"),

    path('index_view_new/', index_view_new, name='index_view_new'),
    path('', index_view_new, name='index_view_new'), # as new home page
    path('index_view_new_category/<str:category_pk>', index_view_new_category, name='index_view_new_category'),

    path('update_index/<str:pk>', update_index, name="update_index"),

    path('export_index_to_excel/', export_data_to_excel, name='export_index_to_excel'),
    path('import_data_from_excel_to_model_index/', import_data_from_excel_to_model_index, name='import_data_from_excel_to_model_index'),

    path('reorder_categories/', reorder_categories, name='reorder_categories'),
]
