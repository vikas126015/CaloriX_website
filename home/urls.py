from django.urls import path
from . import views



urlpatterns = [
   
    path('', views.home, name='home'),
    path('features/', views.features, name='features'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    path('meal_plan/', views.meal_plan, name='meal_plan'),
    path('workout_plan/', views.workout_plan, name='workout_plan'),
    path("nutrient_analysis/", views.nutrient_analysis, name="nutrient_analysis"),
    path("progress_tracking/", views.progress_tracking, name="progress_tracking"), 
    path('api/progress_data/',views.progress_data, name='progress_data'), 




    path("profile/", views.profile_view, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("hydration_calculator/", views.hydration_calculator, name="hydration_calculator"),
    path('workouts/', views.workouts, name='workouts'),path("contact/", views.contact, name="contact"),path("success/", views.success_page, name="success_page"),


]



