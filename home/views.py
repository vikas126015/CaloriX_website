
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def features(request):
    return render(request, 'features.html')

def about(request):  # Add this function
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')



from django.core.mail import send_mail


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        subject = f"New Contact Form Submission from {name}"

        email_message = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """

        send_mail(subject, email_message, "your_email@example.com", ["vikas126018@gmail.com"])
        return redirect("success_page")  # Redirect after successful submission

    return render(request, "contact.html")



def success_page(request):
    return render(request, "success.html")



# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # Redirect to home after login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect("/login")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, "signup.html")
# Logout View
def logout_view(request):
    logout(request)
    return redirect("/")



from django.shortcuts import render
from .forms import WorkoutPlanForm
import random

# Expanded workout database
WORKOUT_DATABASE = {
    "muscle_gain": [
        {"name": "Bench Press", "category": "Strength", "benefits": "Builds chest and arm muscles",
         "description": "Lie on a bench, grip the barbell, lower it to your chest, then push back up.",
         "tips": "Keep your feet flat, and avoid bouncing the bar off your chest."},
        {"name": "Squats", "category": "Strength", "benefits": "Improves leg and core strength",
         "description": "Stand with feet shoulder-width, lower yourself as if sitting, then rise.",
         "tips": "Keep your knees aligned with your toes, and maintain a straight back."},
        {"name": "Deadlifts", "category": "Full Body", "benefits": "Strengthens back, legs, and core",
         "description": "Lift a barbell from the ground while keeping your back straight.",
         "tips": "Engage your core and avoid rounding your back."},
    ],
    "weight_loss": [
        {"name": "Jump Rope", "category": "Cardio", "benefits": "Burns calories, improves agility",
         "description": "Hold the rope handles, swing it over your head, and jump over it.",
         "tips": "Use your wrists, not arms, to turn the rope."},
        {"name": "Burpees", "category": "Full Body", "benefits": "High-calorie burn, full-body workout",
         "description": "Squat, jump into a push-up position, do a push-up, return to squat, jump up.",
         "tips": "Engage your core and avoid rounding your back."},
        {"name": "Running", "category": "Cardio", "benefits": "Improves stamina and burns fat",
         "description": "Run at a moderate pace for 20-30 minutes daily.",
         "tips": "Maintain a steady breathing rhythm and use proper footwear."},
    ],
    "flexibility": [
        {"name": "Yoga Stretching", "category": "Flexibility", "benefits": "Increases mobility and reduces stiffness",
         "description": "Perform slow, controlled stretches to improve flexibility.",
         "tips": "Hold each stretch for 20-30 seconds and avoid bouncing."},
        {"name": "Dynamic Lunges", "category": "Flexibility & Strength", "benefits": "Enhances leg flexibility and strength",
         "description": "Step forward into a deep lunge, hold for a second, then switch legs.",
         "tips": "Keep your back straight and avoid letting your knee go past your toes."},
    ],
    "endurance": [
        {"name": "Cycling", "category": "Cardio", "benefits": "Improves leg endurance and cardiovascular health",
         "description": "Cycle at a moderate pace for 30-60 minutes daily.",
         "tips": "Use proper posture and adjust seat height for comfort."},
        {"name": "Rowing Machine", "category": "Full Body", "benefits": "Improves endurance and upper body strength",
         "description": "Pull the handle towards your chest while pushing with your legs.",
         "tips": "Maintain a steady pace and avoid leaning too far back."},
    ],
    "athletic_performance": [
        {"name": "Agility Drills", "category": "Speed & Agility", "benefits": "Improves quickness and coordination",
         "description": "Perform ladder drills and cone drills to enhance agility.",
         "tips": "Keep your movements light and fast."},
        {"name": "Sprint Intervals", "category": "Cardio & Speed", "benefits": "Boosts speed and cardiovascular health",
         "description": "Sprint for 30 seconds, rest for 1 minute, and repeat.",
         "tips": "Maintain explosive power and keep proper sprinting form."},
    ],
    "general_fitness": [
        {"name": "Plank", "category": "Core Strength", "benefits": "Strengthens core muscles and improves posture",
         "description": "Hold a plank position with elbows and toes on the ground.",
         "tips": "Keep your back straight and engage your core."},
        {"name": "Jump Squats", "category": "Strength & Cardio", "benefits": "Builds leg muscles and improves endurance",
         "description": "Perform a squat, then jump explosively upwards.",
         "tips": "Land softly and immediately transition into the next rep."},
    ],
}

def workout_plan(request):
    form = WorkoutPlanForm()
    plan = {}

    if request.method == "POST":
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            goal = form.cleaned_data["fitness_goal"]
            days = int(form.cleaned_data["workout_days"])

            # Get workouts for selected goal
            selected_workouts = WORKOUT_DATABASE.get(goal, [])

            # Ensure we have enough workouts for 7 days
            if len(selected_workouts) < 7:
                selected_workouts *= (7 // len(selected_workouts)) + 1  # Duplicate workouts if needed

            # Shuffle and pick workouts based on selected days
            random.shuffle(selected_workouts)
            selected_workouts = selected_workouts[:days]

            # Assign workouts to days
            plan = {i+1: workout for i, workout in enumerate(selected_workouts)}

    return render(request, "workout_plan.html", {"form": form, "plan": plan})




import requests
from django.shortcuts import render

def meal_plan(request):
    meal_data = None
    error_message = None

    if request.method == "POST":
        calories = request.POST.get("calories")
        api_key = "426111ff5c7d456e8d896a1bcc55695e"  # Replace with your API key

        # Fetch meal plan
        url = f"https://api.spoonacular.com/mealplanner/generate?timeFrame=day&targetCalories={calories}&apiKey={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            
            # Filter for Indian foods based on common Indian dish names or tags
            indian_keywords = ["curry", "dal", "roti", "paratha", "biryani", "paneer", "masala", "sambar", "idli", "dosa", "pulao", "chutney", "tandoori"]
            indian_meals = [meal for meal in data.get("meals", []) if any(keyword in meal["title"].lower() for keyword in indian_keywords)]

            if indian_meals:
                meal_data = {"meals": indian_meals}
            else:
                error_message = "⚠️ No Indian meals found. Try a different calorie range!"
        else:
            error_message = "❌ Failed to fetch meal plan. Try again later."

    return render(request, "meal_plan.html", {"meal_data": meal_data, "error_message": error_message})



import requests
from django.shortcuts import render

def nutrient_analysis(request):
    nutrition_data = None
    error_message = None

    if request.method == "POST":
        food_item = request.POST.get("food_item")
        api_key = "C/ZYYIIZUK14rmIRlhLJFQ==SoQZoJYiFn8xVhpz"  # Replace with your actual API key
        url = "https://api.calorieninjas.com/v1/nutrition"

        headers = {"X-Api-Key": api_key}
        params = {"query": food_item}

        response = requests.get(url, headers=headers, params=params)
        print("API Response Status:", response.status_code)
        print("API Response JSON:", response.json())  # Debugging

        if response.status_code == 200:
            data = response.json()
            if "items" in data and data["items"]:
                nutrition_data = data["items"][0]  # Get first item from response
            else:
                error_message = "No nutrition data found for the given food item."
        else:
            error_message = f"API request failed: {response.status_code}, {response.text}"

    return render(request, "nutrient_analysis.html", {"nutrition_data": nutrition_data, "error": error_message})








from django.http import JsonResponse
from .models import ProgressTracking

def progress_data(request):
    user_progress = ProgressTracking.objects.filter(user=request.user).order_by('date')
    
    labels = [entry.date.strftime('%Y-%m-%d') for entry in user_progress]
    values = [entry.calories_burned for entry in user_progress]

    return JsonResponse({'labels': labels, 'values': values})



def progress_tracking(request):
    return render(request, "progress_tracking.html") 



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile_view(request):
    # Get the user's profile, create one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'profile.html', {'profile': profile})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import ProfileUpdateForm

@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to profile page
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HydrationCalorieTracker

@login_required
def hydration_calculator(request):
    hydration, created = HydrationCalorieTracker.objects.get_or_create(user=request.user)

    if request.method == "POST":
        weight = request.POST.get("weight")
        height = request.POST.get("height")

        if weight and height:
            hydration.weight = float(weight)
            hydration.height = float(height)
            hydration.save()
            messages.success(request, "Your hydration and health details have been updated!")

    return render(request, "hydration_calculator.html", {"hydration": hydration})






from django.shortcuts import render

def workouts(request):
    workouts_data = [
        {
            "name": "Push-ups",
            "image_url": "https://www.shutterstock.com/shutterstock/videos/1100018993/thumb/1.jpg?ip=x480",
            "benefits": "Strengthens upper body and core.",
            "age_limit": "12+ years",
            "process": "Lower your body until your chest nearly touches the floor, then push back up.",
            "video_url": "https://www.youtube.com/embed/IODxDxX7oi4"
        },
        {
            "name": "Squats",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvrQ0gwGBRkCxPVPvd83-kb6IMbMWFBUXndy3CQaZHOOn6WsxQMqui6IvDgkLmjX8gelA&usqp=CAU",
            "benefits": "Builds lower body strength and improves balance.",
            "age_limit": "12+ years",
            "process": "Lower your hips down while keeping your back straight, then stand back up.",
            "video_url": "https://www.youtube.com/embed/aclHkVaku9U"
        },
        {
            "name": "Plank",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQC9C3upUrpxJfsE2wcKekUVpxo7MyitTcl7A&s",
            "benefits": "Strengthens core muscles and improves posture.",
            "age_limit": "10+ years",
            "process": "Hold your body in a straight line, supporting yourself with your forearms and toes.",
            "video_url": "https://www.youtube.com/embed/pSHjTRCQxIw"
        },
        {
            "name": "Lunges",
            "image_url": "data:image/jpeg;base64,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",
            "benefits": "Improves leg strength and flexibility.",
            "age_limit": "12+ years",
            "process": "Step forward with one leg, lower your body, then push back up.",
            "video_url": "https://www.youtube.com/embed/QOVaHwm-Q6U"
        },
        {
            "name": "Jumping Jacks",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSY9N42KKmxt5-QSh3oPYxcW3J0oHRXzSs3v8qtgoZDdwZB_XCTOLVl3WDVgA_HmlaFyxs&usqp=CAU",
            "benefits": "Great for cardio and full-body warm-up.",
            "age_limit": "5+ years",
            "process": "Jump with arms and legs apart, then return to the starting position.",
            "video_url": "https://www.shutterstock.com/shutterstock/videos/3562901703/preview/stock-footage-high-speed-photography-for-dynamic-scenes-jumping-in-living-room-man-enjoying-exercise-in-casual.webm"
        },
        {
            "name": "Burpees",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKmfBZEEpwjktNAwvZBiEGtlE9W60DWAtViw&s",
            "benefits": "Improves cardiovascular fitness and full-body strength.",
            "age_limit": "15+ years",
            "process": "Drop into a squat, kick your feet back, do a push-up, then jump up.",
            "video_url": "https://www.youtube.com/embed/TU8QYVW0gDU"
        },
        {
            "name": "Mountain Climbers",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZIVzfpwT9qu1B98ScwpZwid9TWfTIsyQbkg&s",
            "benefits": "Strengthens core and improves endurance.",
            "age_limit": "12+ years",
            "process": "Bring your knees towards your chest alternately in a plank position.",
            "video_url": "https://www.youtube.com/embed/nmwgirgXLYM"
        },
        {
            "name": "Leg Raises",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrqNNLWiBSns6PKQxFEI7sehNrFAQxRUG_Hg&s",
            "benefits": "Strengthens lower abdominal muscles.",
            "age_limit": "14+ years",
            "process": "Lie on your back and raise your legs while keeping them straight.",
            "video_url": "https://www.youtube.com/embed/JB2oyawG9KI"
        },
        {
            "name": "Bicycle Crunches",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQV0O0YszZIrQogsNjkl0jWeoodVaql4q6AoA&s",
            "benefits": "Targets abs and obliques for a toned core.",
            "age_limit": "14+ years",
            "process": "Lie on your back, move your legs like pedaling a bike while touching opposite elbow to knee.",
            "video_url": "https://www.youtube.com/embed/9FGilxCbdz8"
        },
        {
            "name": "Pull-ups",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpG6C4XtiOLYAsYTx2GIN0rydr7IGtrPkwOw&s",
            "benefits": "Builds upper body and back strength.",
            "age_limit": "15+ years",
            "process": "Grip a bar, pull your body up until chin reaches over the bar, then lower down.",
            "video_url": "https://www.youtube.com/embed/eGo4IYlbE5g"
        },
        {
            "name": "Dips",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSejC88VwDGZ2650WL0I2BgqA9dN02nJhrf5w&s",
            "benefits": "Strengthens arms, shoulders, and chest.",
            "age_limit": "15+ years",
            "process": "Use parallel bars to lower and raise your body.",
            "video_url": "data:image/jpeg;base64,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"
        },
        {
            "name": "Russian Twists",
            "image_url": "data:image/jpeg;base64,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",
            "benefits": "Improves core strength and flexibility.",
            "age_limit": "12+ years",
            "process": "Sit with knees bent, twist your torso side to side while holding a weight.",
            "video_url": "https://www.youtube.com/embed/wkD8rjkodUI"
        },
        {
            "name": "Deadlifts",
            "image_url": "data:image/jpeg;base64,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",
            "benefits": "Enhances full-body strength and posture.",
            "age_limit": "18+ years",
            "process": "Lift a barbell from the ground to hip level while keeping a straight back.",
            "video_url": "https://www.youtube.com/embed/op9kVnSso6Q"
        },
        {
            "name": "Jump Rope",
            "image_url": "data:image/jpeg;base64,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",
            "benefits": "Boosts cardiovascular fitness and agility.",
            "age_limit": "8+ years",
            "process": "Jump over the rope while swinging it under your feet.",
            "video_url": "https://www.shutterstock.com/shutterstock/videos/1096671237/preview/stock-footage-fitness-health-and-man-skipping-rope-in-gym-motivation-and-mission-for-building-strength-with.webm"
        },
        
    ]

    return render(request, 'workouts.html', {'workouts': workouts_data})
