from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import Recipe, Comment, Category
from .forms import CommentForm, UserRegisterForm, RecipeForm
from django.shortcuts import render, redirect
from .models import Recipe, PageComment
from .forms import PageCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe/recipe_list.html'
    # widgets = {
    #         'categories': forms.CheckboxSelectMultiple(),
    # }

class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipe/recipe_detail.html'
    # widgets = {
    #         'categories': forms.CheckboxSelectMultiple(),
    # }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(recipe=self.object).order_by('-created_date')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the recipe object
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.recipe = self.object
            if request.user.is_authenticated:
                new_comment.author = request.user  # Set the author to the current user
            else:
                anonymous_user = User.objects.get_or_create(username='anonymous')[0]
                new_comment.author = anonymous_user  # Set the author to the anonymous user
            new_comment.save()
            return redirect(new_comment.recipe.get_absolute_url())  # Redirect back to the recipe detail page
        else:
            return HttpResponseNotAllowed(['GET'])  # Return an error for invalid forms or methods


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    # fields = ['name', 'ingredients', 'instructions', 'image', 'categories']
    template_name = 'recipe/recipe_form.html'
    success_url = reverse_lazy('recipe_list')
    # widgets = {
    #         'categories': forms.CheckboxSelectMultiple(),
    # }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()  # Save the Recipe instance
        return super().form_valid(form)

class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = ['name', 'ingredients', 'instructions', 'image', 'categories']
    # widgets = {
    #         'categories': forms.CheckboxSelectMultiple(),
    # }
    template_name = 'recipe/recipe_form.html'
    success_url = reverse_lazy('recipe_list')



class RecipeDeleteView(DeleteView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipe/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')



def logout_view(request):
    logout(request)
    return redirect('/accounts')

# from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registering
            return redirect('recipe_list')  # Redirect to a page of your choice
    else:
        form = UserRegisterForm()
    return render(request, 'recipe/register.html', {'form': form})

def recipe_list(request):
    recipes = Recipe.objects.all()
    comments = PageComment.objects.order_by('-created_date')[:5] 
    comment_form = PageCommentForm()

    if request.method == 'POST':
        comment_form = PageCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.save()
            return redirect('recipe_list')  # Redirect to avoid re-post on refresh

    return render(request, 'recipe/recipe_list.html', {
        'recipes': recipes,
        'comments': comments,
        'comment_form': comment_form,
    })
def more_comments(request):
    comments = PageComment.objects.order_by('-created_date')
    return render(request, 'recipe/more_comments.html', {'comments': comments})

def recipe_list_by_category(request, category_slug):
    category = get_object_or_404(Category, name__icontains=category_slug)
    recipes = Recipe.objects.filter(categories=category)
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes, 'category': category})

def recipe_list_by_search(request):
    keyword = request.GET.get('keyword')
    recipes = Recipe.objects.filter(name__contains=keyword)
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})


def profile(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email
    }
    return render(request, 'profile.html', context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    # email_template_name = 'password_reset_email.html'
    # # subject_template_name = 'password_reset_subject'
    # success_message = "We've emailed you instructions for setting your password, " \
    #                   "if an account exists with the email you entered. You should receive them shortly." \
    #                   " If you don't receive an email, " \
    #                   "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('recipe_list')