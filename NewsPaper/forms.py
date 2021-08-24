from django.forms import ModelForm
from .models import Author, Post

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'type', 'categories', 'title', 'text')
        

class PostFormCreate(ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'type', 'categories', 'title', 'text')
        
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        user = self.initial['created_by']
        if user.is_superuser:
            pass
        else:
            authors = Author.objects.filter(user=user)
            if authors:
                self.fields['author'].initial = authors[0]
                self.fields['author'].disabled = True