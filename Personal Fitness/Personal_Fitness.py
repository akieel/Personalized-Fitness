from tkinter import messagebox, simpledialog, Tk
from tkinter import ttk

class UserInterface:
    def __init__(self):
        self.app = Tk()
        self.app.title("Personalized Fitness & Nutrition Planner")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.input_frame = ttk.Frame(self.app)
        self.input_frame.pack(padx=10, pady=10)

        self.output_frame = ttk.Frame(self.app)
        self.output_frame.pack(padx=10, pady=10)

        
        self.style.configure("Input.TFrame", background="lightblue")
        self.style.configure("Output.TFrame", background="lightgreen")

        self.input_frame.config(style="Input.TFrame")
        self.output_frame.config(style="Output.TFrame")
        self.goal = simpledialog.askstring("Goal", "Enter your goal (weight_loss/muscle_gain/maintenance): ")
        self.dietary_preferences = simpledialog.askstring("Dietary Preferences", "Enter your dietary preferences (keto/vegan/other): ")
        self.allergies = simpledialog.askstring("Allergies", "Enter any allergies you have: ")
        self.activity_level = simpledialog.askstring("Activity Level", "Enter your activity level (sedentary/lightly_active/moderately_active/very_active/extra_active): ")
        self.age = simpledialog.askinteger("Age", "Enter your age: ")
        self.gender = simpledialog.askstring("Gender", "Enter your gender (male/female): ")
        self.height = simpledialog.askfloat("Height (cm)", "Enter your height in cm: ")
        self.weight = simpledialog.askfloat("Weight (kg)", "Enter your weight in kg: ")
        self.health_conditions = []
        while True:
            condition = simpledialog.askstring("Health Condition", "Enter any health conditions or 'done': ")
            if condition.lower() == 'done':
                break
            self.health_conditions.append(condition)
            
        self.style.configure("Custom.TButton", foreground="black", background="lightblue", font=("Arial", 12, "bold"))
        self.style.map("Custom.TButton", background=[("active", "cyan")])
        self.style.configure("CustomLabel.TLabel", font=("Arial", 14))

        self.personalized_planner = PersonalizedFitnessNutritionPlanner(self.goal, self.dietary_preferences, self.allergies, self.activity_level, self.age, self.gender, self.height, self.weight, self.health_conditions)

    def run(self):
        meal_plan = self.personalized_planner.suggest_meal_plan()
        workout_plan = self.personalized_planner.output_custom_fitness_plan()
        health_tips = self.personalized_planner.output_health_fitness_tips()

        messagebox.showinfo("Meal Plan", meal_plan)
        messagebox.showinfo("Workout Plan", workout_plan)
        messagebox.showinfo("Health Tips", health_tips)
        label_goal = ttk.Label(self.input_frame, text="Goal (weight_loss/muscle_gain/maintenance):", style="CustomLabel.TLabel")
        label_goal.pack()

        button_submit = ttk.Button(self.input_frame, text="Submit", style="Custom.TButton")
        button_submit.pack()

        
        label_meal_plan = ttk.Label(self.output_frame, text="Meal Plan:", style="CustomLabel.TLabel")
        label_meal_plan.pack()

        label_workout_plan = ttk.Label(self.output_frame, text="Workout Plan:", style="CustomLabel.TLabel")
        label_workout_plan.pack()

        label_health_tips = ttk.Label(self.output_frame, text="Health Tips:", style="CustomLabel.TLabel")
        label_health_tips.pack()

        self.app.mainloop()

class PersonalizedFitnessNutritionPlanner:
    def __init__(self, goal, dietary_preferences, allergies, activity_level, age, gender, height, weight, health_conditions):
        self.goal = goal
        self.dietary_preferences = dietary_preferences
        self.allergies = allergies
        self.activity_level = activity_level
        self.age = age
        self.gender = gender
        self.height = height  # in cm
        self.weight = weight  # in kg
        self.health_conditions = health_conditions
        


    def calculate_bmr(self):
        if self.gender.lower() == 'male':
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)
        return bmr

    def calculate_tdee(self):
        bmr = self.calculate_bmr()
        activity_levels = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        activity_factor = activity_levels.get(self.activity_level.lower(), 1.2)
        tdee = bmr * activity_factor
        return tdee

    def generate_nutrition_plan(self):
        tdee = self.calculate_tdee()
        if self.goal == 'weight_loss':
            daily_caloric_intake = tdee - 500
        elif self.goal == 'muscle_gain':
            daily_caloric_intake = tdee + 500
        else:
            daily_caloric_intake = tdee
        if self.dietary_preferences == 'keto':
            macros = {'protein': 20, 'carbs': 5, 'fats': 75}
        elif self.dietary_preferences == 'vegan':
            macros = {'protein': 25, 'carbs': 50, 'fats': 25}
        else:
            macros = {'protein': 30, 'carbs': 40, 'fats': 30}
        return {'daily_caloric_intake': daily_caloric_intake, 'macros': macros}




    def suggest_meal_plan(self):
        nutrition_plan = self.generate_nutrition_plan()
        daily_caloric_intake = nutrition_plan['daily_caloric_intake']
        macros = nutrition_plan['macros']

        weekly_meal_plan = {
            day: {'breakfast': None, 'lunch': None, 'dinner': None, 'snacks': []}
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        }

        meal_distribution = {
            'breakfast': 0.25,
            'lunch': 0.35,
            'dinner': 0.30,
            'snacks': 0.10
        }

        for day, meals in weekly_meal_plan.items():
            meals['breakfast'] = self.get_meals_for_criteria(daily_caloric_intake * meal_distribution['breakfast'], macros, 'breakfast')
            meals['lunch'] = self.get_meals_for_criteria(daily_caloric_intake * meal_distribution['lunch'], macros, 'lunch')
            meals['dinner'] = self.get_meals_for_criteria(daily_caloric_intake * meal_distribution['dinner'], macros, 'dinner')
            meals['snacks'].append(self.get_meals_for_criteria(daily_caloric_intake * meal_distribution['snacks'], macros, 'snack'))

        return weekly_meal_plan

    def get_meals_for_criteria(self, calories, macros, meal_type):
        protein_calories = calories * (macros['protein'] / 100)
        carbs_calories = calories * (macros['carbs'] / 100)
        fats_calories = calories * (macros['fats'] / 100)

        protein_grams = protein_calories / 4
        carbs_grams = carbs_calories / 4
        fats_grams = fats_calories / 9

        meal_description = f"Sample {meal_type} meal - Calories: {calories:.2f}, Protein: {protein_grams:.2f}g, Carbs: {carbs_grams:.2f}g, Fats: {fats_grams:.2f}g"
        return meal_description


    def create_workout_routine(self):
        workout_routine = {
            'Monday': {'exercises': [], 'duration': 0},
            'Wednesday': {'exercises': [], 'duration': 0},
            'Friday': {'exercises': [], 'duration': 0},
        }

        if self.goal == 'weight_loss':
            workout_type = 'cardio'
            intensity = 'moderate'
            duration = 30
        elif self.goal == 'muscle_gain':
            workout_type = 'strength'
            intensity = 'high'
            duration = 45
        else:
            workout_type = 'mixed'
            intensity = 'moderate'
            duration = 30

        for day, details in workout_routine.items():
            details['exercises'] = self.get_exercises_for_day(workout_type, intensity)
            details['duration'] = duration

        return workout_routine

    def get_exercises_for_day(self, workout_type, intensity):
        cardio_exercises = [
            {'name': 'Running', 'intensity': intensity, 'reps': '30 mins', 'sets': 1},
            {'name': 'Cycling', 'intensity': intensity, 'reps': '30 mins', 'sets': 1}
        ]
        strength_exercises = [
            {'name': 'Squats', 'intensity': intensity, 'reps': 12, 'sets': 3},
            {'name': 'Deadlifts', 'intensity': intensity, 'reps': 10, 'sets': 3}
        ]
        mixed_exercises = cardio_exercises[:1] + strength_exercises[:1]

        if workout_type == 'cardio':
            selected_exercises = cardio_exercises
        elif workout_type == 'strength':
            selected_exercises = strength_exercises
        else:
            selected_exercises = mixed_exercises

        return selected_exercises

    def suggest_exercise_modifications(self):
        modifications = {
            'knee_pain': [
                {'original': 'Squats', 'modified': 'Chair Squats', 'reason': 'Reduces strain on knees'},
                {'original': 'Running', 'modified': 'Speed Walking', 'reason': 'Lowers impact on knees'}
            ],
            'lower_back_issues': [
                {'original': 'Deadlifts', 'modified': 'Kettlebell Swings', 'reason': 'Minimizes lower back stress'},
                {'original': 'Sit-ups', 'modified': 'Planks', 'reason': 'Strengthens core with less spine pressure'}
            ]
        }

        applicable_modifications = []
        for condition in self.health_conditions:
            if condition.lower() in modifications:
                applicable_modifications.extend(modifications[condition.lower()])

        return applicable_modifications

    def output_personalized_nutrition_guide(self):
        nutrition_plan = self.generate_nutrition_plan()
        return {
            'daily_caloric_intake': nutrition_plan['daily_caloric_intake'],
            'macro-nutrient_ratios': nutrition_plan['macros'],
            'meal_timing': '3 main meals and 2 snacks, adjust based on schedule and hunger levels.',
            'hydration_guidelines': 'Aim for 8 glasses of water per day, more if active.',
            'supplement_recommendations': 'Based on dietary preferences; e.g., B12 for vegans.',
            'actionable_tips': ['Prepare meals in advance', 'Keep healthy snacks on hand', 'Read labels to stay within targets'],
            'adaptation_and_feedback': 'Regularly review and adjust your plan, consult a professional for significant changes.'
        }

    def output_custom_fitness_plan(self):
        workout_routine = self.create_workout_routine()
        exercise_modifications = self.suggest_exercise_modifications()

  
        fitness_plan = {
            'workout_schedule': workout_routine,
            'exercise_modifications': exercise_modifications,
            'progressive_overload_suggestions': 'Gradually increase weights or intensity every 2 weeks to continue making progress.',
            'recovery_and_rest': 'Include at least 2 rest days per week to allow for muscle recovery and growth.',
            'visual_aids': 'Links to exercise demonstrations will be provided in the final app.'
        }

    
        for day, session in fitness_plan['workout_schedule'].items():
            session['exercises'] = [f"{exercise['name']} - Sets: {exercise['sets']}, Reps: {exercise['reps']}" for exercise in session['exercises']]
      
            for mod in exercise_modifications:
                if any(exercise['name'] == mod['original'] for exercise in session['exercises']):
                    session['exercises'].append(f"Modification for {mod['original']}: {mod['modified']} - {mod['reason']}")

        return fitness_plan


    def output_health_fitness_tips(self):
        return {
            'general_wellness': ['Aim for 7-9 hours of sleep', 'Practice stress-reducing activities'],
            'nutritional_advice': ['Stay hydrated', 'Incorporate a variety of fruits and vegetables'],
            'exercise_and_activity': ['Incorporate stretching or yoga', 'Use a fitness tracker for daily steps'],
            'injury_prevention': ['Always warm up and cool down', 'Maintain proper form'],
            'motivation_and_habit_building': ['Set SMART goals', 'Celebrate small victories'],
            'community_and_support': ['Join fitness groups', 'Work with a fitness coach or nutritionist']
        }
  
    def initialize_progress_tracker(self):
        self.progress_tracker = {
            'weight': [],
            'body_measurements': {'chest': [], 'waist': [], 'hips': []},
            'workout_performance': {},
            'dietary_adherence': []
        }

    def log_progress(self, date, weight=None, measurements=None, workout_performance=None, dietary_adherence=None):
        if weight:
            self.progress_tracker['weight'].append((date, weight))
        if measurements:
            for key, value in measurements.items():
                self.progress_tracker['body_measurements'][key].append((date, value))
        if workout_performance:
            self.progress_tracker['workout_performance'][date] = workout_performance
        if dietary_adherence:
            self.progress_tracker['dietary_adherence'].append((date, dietary_adherence))
        
    def collect_user_feedback(self, feedback):
        self.user_feedback = feedback

    def analyze_feedback_and_progress(self):
        analysis_results = "Analysis of feedback and progress data"
        return analysis_results

    def adjust_plans_based_on_feedback(self):
        analysis_results = self.analyze_feedback_and_progress()
        adjustments_made = "Adjustments made based on feedback"
        return adjustments_made
    
    def integrate_community_support(self):
        return {
            'forum_access': 'URL_to_Fitness_Forum',
            'group_challenges': 'List_of_Upcoming_Group_Challenges',
            'success_stories': 'Featured_Success_Stories',
            'expert_qa_sessions': 'Schedule_of_Upcoming_Q&A_Sessions',
            'peer_support_groups': 'Links_to_Join_Peer_Support_Groups'
        }
    
    def integrate_mindfulness_and_mental_health_support(self):
        return {
            'stress_management_techniques': 'Effective stress management techniques.',
            'mindfulness_exercises': 'Guided mindfulness exercises.',
            'sleep_improvement_tips': 'Advice on improving sleep quality.'
        }

    def integrate_injury_prevention_and_rehab_support(self):
        return {
            'warm_up_routines': 'Warm-up exercises to prevent injuries.',
            'cool_down_routines': 'Cooldown routines for recovery.',
            'rehab_exercises': {
                'knee_injuries': 'Exercises for knee injuries.',
                'back_injuries': 'Routines for back strength.'
            }
        }



    def community_support(self):
        
        pass

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
