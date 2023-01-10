from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Topic, Note
from .forms import TopicForm, NoteForm, NoteFormDelete, TopicFormDelete

# Create your views here.


def index(request):
    return render(request, 'my_notes_app/index.html')


@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    notes = topic.note_set.order_by('-date')
    is_user_an_author(topic, request)
    context = {'topic': topic, 'notes': notes}
    return render(request, 'my_notes_app/topic.html', context)


@login_required
def topics(request):
    topics = Topic.objects.filter(author=request.user).order_by('-date')
    notes = Note.objects.filter(author=request.user).order_by('-date')
    context = {'topics': topics, 'notes': notes}
    return render(request, 'my_notes_app/topics.html', context)


@login_required
def notes(request):
    notes = Note.objects.filter(author=request.user).order_by('-date')
    context = {'notes': notes}
    return render(request, 'my_notes_app/notes.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.author = request.user
            new_topic.save()
            form.save()
            return redirect('my_notes_app:topics')
    context = {'form': form}
    return render(request, 'my_notes_app/new_topic.html', context)


@login_required
def new_note(request):
    if request.method != 'POST':
        form = NoteForm(author=request.user)
    else:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.author = request.user
            new_note.save()
            form.save()
            return redirect('my_notes_app:notes')
    context = {'form': form, 'topics': topics}
    return render(request, 'my_notes_app/new_note.html', context)


@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    is_user_an_author(topic, request)
    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_notes_app:topics')
    context = {'form': form, 'topic': topic}
    return render(request, 'my_notes_app/edit_topic.html', context)


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    topic = note.topic
    is_user_an_author(topic, request)
    if request.method != 'POST':
        form = NoteForm(instance=note, author=request.user)
    else:
        form = NoteForm(instance=note, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_notes_app:notes')
    context = {'form': form, 'note': note}
    return render(request, 'my_notes_app/edit_note.html', context)


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    topic = note.topic
    is_user_an_author(topic, request)
    if request.method != 'POST':
        form = NoteFormDelete(instance=note)
    else:
        form = NoteFormDelete(instance=note, data=request.POST)
        if form.is_valid():
            note.delete()
            return redirect('my_notes_app:notes')
    context = {'form': form, 'note': note}
    return render(request, 'my_notes_app/delete_note.html', context)


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    notes = topic.note_set.order_by('-date')
    is_user_an_author(topic, request)
    if request.method != 'POST':
        form = TopicFormDelete(instance=topic)
    else:
        form = TopicFormDelete(instance=topic, data=request.POST)
        if form.is_valid():
            topic.delete()
            return redirect('my_notes_app:topics')
    context = {'form': form, 'topic': topic, 'notes': notes}
    return render(request, 'my_notes_app/delete_topic.html', context)


def is_user_an_author(topic, request):
    if topic.author != request.user:
        raise Http404
