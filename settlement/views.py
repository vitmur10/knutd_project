from .models import Hostel
from django.shortcuts import render, redirect
from .forms import StudentForm, StudentParentsForm
from django.http import Http404


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        parent_form = StudentParentsForm(request.POST)
        if form.is_valid() and parent_form.is_valid():
            parent_form.save()
            form.save()
    else:
        form = StudentForm()
        parent_form = StudentParentsForm()

    return render(request, 'swttlement/form.html', {'form': form,
                                                    'parent_form': parent_form})


def hostel(request):
    try:
        h = Hostel.objects.all()
    except:
        raise Http404('Сталася помилка(')
    return render(request, 'swttlement/dormitories.html', {'hostel': h})