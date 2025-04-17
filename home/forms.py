
from django import forms

class WorkoutPlanForm(forms.Form):
    FITNESS_GOALS = [
        ("muscle_gain", "Muscle Gain"),
        ("weight_loss", "Weight Loss"),
        ("flexibility", "Flexibility"),
        ("endurance", "Endurance"),
        ("athletic_performance", "Athletic Performance"),
        ("general_fitness", "General Fitness"),
    ]
    
    DAYS_CHOICES = [(str(i), f"{i} Days") for i in range(1, 8)]  # 1 to 7 days

    fitness_goal = forms.ChoiceField(choices=FITNESS_GOALS, label="Select Your Fitness Goal")
    workout_days = forms.ChoiceField(choices=DAYS_CHOICES, label="Select Workout Duration")




from django import forms
from .models import MealPlan

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['meal_name', 'calories', 'details']
        widgets = {
            'meal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meal Name'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calories'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Meal Details', 'rows': 4}),
        }



from django import forms
from .models import UserProfile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "age", "gender", "height", "weight", "bio"]
