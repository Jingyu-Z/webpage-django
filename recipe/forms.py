from django import forms
from .models import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RecipeForm(forms.ModelForm):
    # Use a CharField for category input. You might instruct users to separate categories with commas.
    category_input = forms.CharField(label='Categories', required=False, help_text='Separate categories with commas')

    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'instructions', 'image', 'categories']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # If this is an update, prefill the category input with current categories
            self.fields['category_input'].initial = ', '.join([c.name for c in self.instance.categories.all()])

    def save(self, commit=True):
        instance = super(RecipeForm, self).save(commit=False)
        
        # Other processing if needed
        
        if commit:
            instance.save()  # Save the instance so it gets an ID necessary for many-to-many relationships
            
            # Assuming categories are optional, clear them only if category_input is provided
            if self.cleaned_data['category_input']:  # Check if category_input field is not empty
                instance.categories.clear()  # Clear existing categories after the instance is saved

                # Parse the category_input field
                category_names = [name.strip() for name in self.cleaned_data['category_input'].split(',')]
                for name in category_names:
                    # Create category if doesn't exist, then add to the recipe
                    category, created = Category.objects.get_or_create(name=name)
                    instance.categories.add(category)  

        return instance
    
from django import forms
from .models import PageComment

class PageCommentForm(forms.ModelForm):
    class Meta:
        model = PageComment
        fields = ['text']
