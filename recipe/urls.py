from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ResetPasswordView
from .views import recipe_list, more_comments, recipe_list_by_search
from .views import (
    home,
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    logout_view,
    register,
    recipe_list_by_category,
)

urlpatterns = [
    path('', home, name='home.html'),
]

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]


urlpatterns += [
    path('', recipe_list, name='recipe_list'),
    path('',home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(),name='recipe_detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe_new'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('accounts/logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('register/', register, name='register'),
    path('more-comments/', more_comments, name='more_comments'),
    path('recipes/category/<slug:category_slug>/', recipe_list_by_category, name='recipes_by_category'),
    path('recipes/', recipe_list_by_search, name='recipes_search'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
