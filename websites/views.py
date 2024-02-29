# websites/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .forms import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import InputIndexForm
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from .models import IndexCategory
from django.shortcuts import render
from .models import Index, IndexCategory
from django.http import HttpResponse
import pandas as pd
from .models import Index  # Import your model here
from django.shortcuts import render
from django.http import HttpResponseRedirect
import pandas as pd
from .models import Index  # Import your model here
from django.shortcuts import render
from django.http import JsonResponse
from .models import IndexCategory
from datetime import datetime, timedelta
from django.db.models import Q  # Import the Q object
from django.utils import timezone

def main_page_view(request):
    return render(request, 'websites/main_page.html', {})


def input_index_view(request):
    index_form = InputIndexForm()

    if request.method == 'POST':
        if 'index_form_submit' in request.POST:
            index_form = InputIndexForm(request.POST)
            if index_form.is_valid():
                index_form.save()
                return redirect('/')

    context = {
        'index_form': index_form,
    }

    return render(request, 'websites/input_index.html', context)


def input_index_category_view(request):
    index_category_form = InputIndexCategoryForm()

    if request.method == 'POST':
        if 'index_category_form_submit' in request.POST:
            index_category_form = InputIndexCategoryForm(request.POST)
            if index_category_form.is_valid():
                index_category_form.save()
                return redirect('input_index')

    context = {
        'index_category_form': index_category_form,
    }

    return render(request, 'websites/input_index_category.html', context)


def input_index_and_index_category_view_old(request):
    index_form = InputIndexForm()

    if request.method == 'POST':
        if 'index_form_submit' in request.POST:
            index_form = InputIndexForm(request.POST)
            if index_form.is_valid():
                index_form.save()
                return redirect('/')

    index_category_form = InputIndexCategoryForm()

    if request.method == 'POST':
        if 'index_category_form_submit' in request.POST:
            index_category_form = InputIndexCategoryForm(request.POST)
            if index_category_form.is_valid():
                index_category_form.save()
                # return redirect('input_index')

    context = {
        'index_form': index_form,
        'index_category_form': index_category_form,
    }

    return render(request, 'websites/input_index_and_index_category.html', context)


def output_index_list_view(request):
    # frequent block
    indexes = Index.objects.all().order_by('-click_times')
    # indexes by 2 columns
    total_indexes = indexes.count()
    midpoint = total_indexes // 2
    indexes_first_column = indexes[:midpoint]
    indexes_second_column = indexes[midpoint:]

    # work block
    indexes_work = Index.objects.filter(category1__category_name="Work")

    # to do block
    if request.method == 'POST':
        todotask_form = ToDoTaskForm(request.POST)
        if todotask_form.is_valid():
            todotask_form.save()
            return redirect('output_index_list')
    else:
        todotask_form = ToDoTaskForm()

    tasks = ToDoTask.objects.filter(task_done=False)
    total_tasks = tasks.count()

    # news block
    indexes_news = Index.objects.filter(category1__category_name="News").order_by('-click_times')

    # study block
    indexes_study = Index.objects.filter(category1__category_name="Study")

    # tools block
    indexes_tools = Index.objects.filter(category1__category_name="Tools").order_by('-click_times')

    # shopping block
    indexes_shopping = Index.objects.filter(category1__category_name="Shopping")

    # music block
    indexes_music = Index.objects.filter(category1__category_name="Music")

    # Bank block
    indexes_bank = Index.objects.filter(category1__category_name="Bank")

    # Jobs block
    indexes_jobs = Index.objects.filter(category1__category_name="Jobs")

    # Others block
    indexes_others = Index.objects.filter(category1__category_name="Others")

    # context or data to webpage
    context = {
        'indexes': indexes,
        # frequent block indexes by 2 columns
        'indexes_first_column': indexes_first_column,
        'indexes_second_column': indexes_second_column,

        'indexes_work': indexes_work,

        'tasks': tasks,
        'todotask_form': todotask_form,
        'total_tasks': total_tasks,

        'indexes_news': indexes_news,
        'indexes_study': indexes_study,
        'indexes_tools': indexes_tools,
        'indexes_shopping': indexes_shopping,
        'indexes_music': indexes_music,
        'indexes_bank': indexes_bank,
        'indexes_jobs': indexes_jobs,

        'indexes_others': indexes_others,
    }
    return render(request, 'websites/main_page.html', context)


def mark_task_done(request, task_id):
    task = ToDoTask.objects.get(pk=task_id)
    task.task_done = True
    task.save()
    return redirect('/')


def record_click(request, index_id):
    try:
        index = Index.objects.get(pk=index_id)
        if index.click_times is not None:
            index.click_times += 1
        else:
            index.click_times = 1
        index.last_click_date = timezone.now()
        index.save()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Index not found'})


def input_index_and_index_category_view(request):
    # Input index form
    index_form = InputIndexForm()

    if request.method == 'POST':
        if 'index_form_submit' in request.POST:
            index_form = InputIndexForm(request.POST)
            if index_form.is_valid():
                index_form.save()
                return redirect('/')

    # input index category form
    index_category_form = InputIndexCategoryForm()

    if request.method == 'POST':
        if 'index_category_form_submit' in request.POST:
            index_category_form = InputIndexCategoryForm(request.POST)
            if index_category_form.is_valid():
                index_category_form.save()
                return redirect('input_index_and_index_category')

    context = {
        'index_form': index_form,
        'index_category_form': index_category_form,
    }

    return render(request, 'websites/input_index_and_index_category.html', context)


# new try
def index_view_new(request):
    categories = IndexCategory.objects.all().order_by('category_order_num')
    indexes_by_category = {}

    for category in categories:
        indexes_category = Index.objects.filter(category1=category)
        indexes_by_category[category] = indexes_category

    indexes = Index.objects.all().order_by('-click_times')

    # for debug only
    category_pk = ""

    # to do block
    if request.method == 'POST':
        todotask_form = ToDoTaskForm(request.POST)
        if todotask_form.is_valid():
            todotask_form.save()
            return redirect('index_view_new')
    else:
        todotask_form = ToDoTaskForm()

# task list
# original task list (list all not complete tasks)
#     tasks = ToDoTask.objects.filter(task_done=False)
# new code for task list : task not done, no due_date or due_date will be within 2 weeks
    # Get today's date
    today_date = datetime.now()
    # Filter tasks based on your conditions
    tasks = ToDoTask.objects.filter(
        Q(task_done=False) & (Q(task_due_date__isnull=True) | Q(task_due_date__lte=today_date + timedelta(days=14)))
    )
    total_tasks = tasks.count()

# reminder tasks list
    # Get today's date and time
    today_date = timezone.now()
    # Filter reminder tasks based on conditions
    reminder_tasks = ToDoTask.objects.filter(task_done=False, task_reminder1_date__lte=today_date)

    context = {
        'indexes_by_category': indexes_by_category,
        'indexes': indexes,
        'category_pk': category_pk,  # debug only

        'tasks': tasks,
        'todotask_form': todotask_form,
        'total_tasks': total_tasks,
        'reminder_tasks': reminder_tasks,
    }

    return render(request, 'websites/main_page_new.html', context)


def index_view_new_category(request, category_pk):
    categories = IndexCategory.objects.all().order_by('category_order_num')
    indexes_by_category = {}

    for category in categories:
        indexes_category = Index.objects.filter(category1=category)
        indexes_by_category[category] = indexes_category

    indexes = Index.objects.all().order_by('-click_times')

    category_pk = category_pk

    # to do block
    if request.method == 'POST':
        todotask_form = ToDoTaskForm(request.POST)
        if todotask_form.is_valid():
            todotask_form.save()
            return redirect('index_view_new')
    else:
        todotask_form = ToDoTaskForm()

    tasks = ToDoTask.objects.filter(task_done=False)
    total_tasks = tasks.count()

    context = {
        'indexes_by_category': indexes_by_category,
        'indexes': indexes,
        'category_pk': category_pk,

        'tasks': tasks,
        'todotask_form': todotask_form,
        'total_tasks': total_tasks,
    }

    return render(request, 'websites/main_page_new.html', context)


def export_data_to_excel(request):
    # Fetch all data from the Index model
    queryset = Index.objects.all()

    # Convert queryset to a Pandas DataFrame
    data = {
        'key_words': [item.key_words for item in queryset],
        'address': [item.address for item in queryset],
        'category1': [item.category1 for item in queryset],
        # 'date_created': [item.date_created for item in queryset],
        # 'last_click_date': [item.last_click_date for item in queryset],
        # 'click_times': [item.click_times for item in queryset],
    }

    df = pd.DataFrame(data)

    # Export DataFrame to Excel file
    excel_file_path = 'index_data.xlsx'  # Set your desired file path/name
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

    # Create a response with the Excel file
    with open(excel_file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{excel_file_path}"'

    return response


def import_data_from_excel_to_model_index(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')

        try:
            df = pd.read_excel(excel_file)

            # Iterate through DataFrame rows and create Index objects
            for _, row in df.iterrows():
                Index.objects.create(
                    key_words=row['key_words'],
                    address=row['address'],
                    # category1=row['category1'],
                    # Add other fields accordingly
                )

            return HttpResponse("Import successful!")
        except Exception as e:
            return HttpResponse(f"Import failed. Error: {str(e)}")

    return render(request, 'websites/import_excel_to_model_index.html')


def update_index(request, pk):
    index = Index.objects.get(id=pk)
    index_form = InputIndexForm(instance=index)

    if request.method == 'POST':
        index_form = InputIndexForm(request.POST, instance=index)
        if index_form.is_valid():
            index_form.save()
            return redirect('/')

    context = {'index_form': index_form}

    return render(request, 'websites/input_index_and_index_category.html', context)


def reorder_categories(request):
    if request.method == 'POST':
        new_order = request.POST.getlist('category_order[]')
        for idx, category_id in enumerate(new_order, start=1):
            category = IndexCategory.objects.get(pk=category_id)
            category.category_order_num = idx
            category.save()

        return JsonResponse({'success': True})

    categories = IndexCategory.objects.all().order_by('category_order_num')
    return render(request, 'websites/reorder_categories.html', {'categories': categories})


def input_todotask_view(request):
    todotask_form = ToDoTaskForm()

    if request.method == 'POST':
        if 'todotask_form_submit' in request.POST:
            todotask_form = ToDoTaskForm(request.POST)
            if todotask_form.is_valid():
                todotask_form.save()
                return redirect('/')

    context = {
        'todotask_form': todotask_form,
    }

    return render(request, 'websites/input_todo_tasks.html', context)


def update_todotask_view_rev0(request, pk):
    todotask = ToDoTask.objects.get(id=pk)
    todotask_form = ToDoTaskForm(instance=todotask)

    if request.method == 'POST':
            todotask_form = ToDoTaskForm(request.POST, instance=todotask)
            if todotask_form.is_valid():
                todotask_form.save()
                return redirect('/')

    context = {
        'todotask_form': todotask_form,
    }

    return render(request, 'websites/edit_todo_tasks.html', context)


def update_todotask_view(request, pk):
    todotask = ToDoTask.objects.get(id=pk)

    if request.method == 'POST':
        todotask_form = ToDoTaskForm(request.POST, instance=todotask)
        if todotask_form.is_valid():
            todotask_form.save()
            return redirect('/')

    else:
        todotask_form = ToDoTaskForm(instance=todotask)

    context = {
        'todotask_form': todotask_form,
        'todotask': todotask,  # Add this line to pass the instance to the template
    }

    return render(request, 'websites/edit_todo_tasks.html', context)

