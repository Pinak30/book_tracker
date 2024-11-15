from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book
from .forms import BookForm, LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in.')
                return redirect('book_list')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        messages.error(request, "The book you're looking for does not exist.")
        return redirect('book_list')
    return render(request, 'book_detail.html', {'book': book})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})


@login_required
def edit_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        messages.error(request, "The book you're trying to edit does not exist.")
        return redirect('book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('book_detail', id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})


@login_required
def delete_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        messages.error(request, "The book you're trying to delete does not exist.")
        return redirect('book_list')

    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})


@login_required
def update_progress(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        messages.error(request, "The book you're trying to update progress for does not exist.")
        return redirect('book_list')

    if request.method == 'POST':
        progress = request.POST.get('progress')
        if progress:
            book.progress = progress
            book.save()
            messages.success(request, "Progress updated successfully.")
        else:
            messages.error(request, "Progress cannot be empty.")
        return redirect('book_detail', id=book.id)
    return render(request, 'update_progress.html', {'book': book})


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('book_list')  