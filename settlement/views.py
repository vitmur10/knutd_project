from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Student


from django.shortcuts import render, redirect
from .forms import StudentForm, StudentParentsForm
from datetime import datetime


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # Перенаправити на сторінку зі списком студентів
    else:
        form = StudentForm()

    return render(request, 'swttlement/form.html', {'form': form})



