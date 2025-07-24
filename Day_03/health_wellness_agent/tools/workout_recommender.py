# tools/workout_recommender.py

from agents import function_tool

@function_tool
async def WorkoutRecommenderTool(input: str) -> dict:
    goal_type = input.lower()

    if "weight" in goal_type:
        return {
            "Monday": "Cardio (Running 30 min)",
            "Tuesday": "HIIT (20 min)",
            "Wednesday": "Yoga (40 min)",
            "Thursday": "Cycling (30 min)",
            "Friday": "Strength Training (Full Body)",
            "Saturday": "Rest",
            "Sunday": "Walk 5km + Light Stretching"
        }
    elif "muscle" in goal_type:
        return {
            "Monday": "Chest + Triceps",
            "Tuesday": "Back + Biceps",
            "Wednesday": "Legs",
            "Thursday": "Shoulders + Abs",
            "Friday": "Full Body Circuit",
            "Saturday": "Rest",
            "Sunday": "Light Cardio + Stretch"
        }
    else:
        return {
            "Monday": "Mixed workout",
            "Tuesday": "Yoga",
            "Wednesday": "Walk",
            "Thursday": "Stretch",
            "Friday": "Light Cardio",
            "Saturday": "Rest",
            "Sunday": "Cycling"
        }
