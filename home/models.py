from django.db import models
from django.contrib.auth.models import User

# Fitness Goals Choices
FITNESS_GOALS = [
    ('weight_loss', 'Weight Loss'),
    ('muscle_gain', 'Muscle Gain'),
    ('endurance', 'Endurance Training'),
    ('general_fitness', 'General Fitness'),
]

# Workout Plan Model
class WorkoutPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=50, choices=FITNESS_GOALS, default='general_fitness')
    experience_level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner')
    workout_days = models.PositiveIntegerField(default=3)
    workouts = models.TextField()  # Store workout details as JSON or plain text

    def __str__(self):
        return f"{self.user.username} - {self.fitness_goal}"




class MealPlan(models.Model):
    meal_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    details = models.TextField()

    def __str__(self):
        return self.meal_name



class ProgressTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    calories_burned = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.calories_burned}"
    



    from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")], null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # in cm
    weight = models.FloatField(null=True, blank=True)  # in kg
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username





from django.db import models
from django.contrib.auth.models import User

class HydrationCalorieTracker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, blank=True, help_text="Enter your weight in kg")
    height = models.FloatField(null=True, blank=True, help_text="Enter your height in cm")
    bmi = models.FloatField(default=0)  # Body Mass Index
    health_status = models.CharField(max_length=100, default="Unknown")
    daily_water_requirement = models.FloatField(default=0)  # Liters
    daily_calorie_requirement = models.IntegerField(default=0)  # Calories

    def calculate_bmi(self):
        if self.weight and self.height:
            return round(self.weight / ((self.height / 100) ** 2), 2)
        return 0

    def get_health_status(self):
        bmi = self.calculate_bmi()
        if bmi == 0:
            return "Unknown"
        elif bmi < 18.5:
            return "Underweight - Increase calorie intake"
        elif 18.5 <= bmi < 24.9:
            return "Healthy - Maintain balanced diet"
        elif 25 <= bmi < 29.9:
            return "Overweight - Reduce calorie intake"
        else:
            return "Obese - Follow strict diet & exercise"

    def calculate_water_requirement(self):
        return round(self.weight * 0.033, 2) if self.weight else 0

    def calculate_calorie_requirement(self):
        return int(self.weight * 30) if self.weight else 0

    def save(self, *args, **kwargs):
        if self.weight and self.height:
            self.bmi = self.calculate_bmi()
            self.health_status = self.get_health_status()
            self.daily_water_requirement = self.calculate_water_requirement()
            self.daily_calorie_requirement = self.calculate_calorie_requirement()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg - {self.bmi} BMI - {self.health_status}"


