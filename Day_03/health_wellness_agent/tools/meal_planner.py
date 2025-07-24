# tools/meal_planner.py

from agents import function_tool
from typing import List

@function_tool
async def MealPlannerTool(input: str) -> List[str]:
    preference = input.lower()

    if "vegetarian" in preference:
        meals = [
            "Day 1: Veggie stir-fry with tofu and brown rice",
            "Day 2: Lentil soup with whole wheat bread",
            "Day 3: Chickpea salad with olive oil dressing",
            "Day 4: Paneer curry with quinoa",
            "Day 5: Vegetable biryani with raita",
            "Day 6: Grilled mushrooms with steamed broccoli",
            "Day 7: Rajma with brown rice and salad"
        ]
    elif "vegan" in preference:
        meals = [
            "Day 1: Quinoa bowl with black beans and avocado",
            "Day 2: Tofu scramble with toast",
            "Day 3: Vegan lentil curry with rice",
            "Day 4: Sweet potato and chickpea stew",
            "Day 5: Vegan pasta with tomato-basil sauce",
            "Day 6: Stir-fried veggies with sesame seeds",
            "Day 7: Mixed greens salad with hummus dressing"
        ]
    else:
        meals = [
            "Day 1: Grilled chicken with veggies",
            "Day 2: Baked salmon with brown rice",
            "Day 3: Egg omelet with whole grain toast",
            "Day 4: Tuna salad with olive oil",
            "Day 5: Turkey sandwich with lettuce and tomato",
            "Day 6: Beef stir-fry with bell peppers",
            "Day 7: Chicken biryani with yogurt"
        ]

    return meals
