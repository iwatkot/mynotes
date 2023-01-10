from django import forms
from .models import Topic, Note


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
        labels = {'name': ''}


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'topic']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

    def __init__(self, author=None, **kwargs):
        super(NoteForm, self).__init__(**kwargs)
        if author:
            self.fields['topic'].queryset = Topic.objects.filter(author=author)


class NoteFormDelete(forms.ModelForm):
    class Meta:
        model = Note
        fields = []


class TopicFormDelete(forms.ModelForm):
    class Meta:
        model = Topic
        fields = []
