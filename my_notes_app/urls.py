from django.urls import path
from . import views

app_name = 'my_notes_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('topics/', views.topics, name='topics'),
    path('notes/', views.notes, name='notes'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_note/', views.new_note, name='new_note'),
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('delete_topic/<int:topic_id>/', views.delete_topic,
         name='delete_topic'),
]
