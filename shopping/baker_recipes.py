from model_bakery.recipe import Recipe
from shopping.models import Ingredient, Meal, Plan, Section, Store

# Stores

store_one = Recipe(Store, name="Store 1", user_id=1)
store_two = Recipe(Store, name="Store 2", user_id=1)
store_three = Recipe(Store, name="Store 3", user_id=1)

# Sections

section_one = Recipe(Section, name="Section 1", user_id=1)
section_two = Recipe(Section, name="Section 2", user_id=1)
section_three = Recipe(Section, name="Section 3", user_id=1)

#  Ingredients

ingredient_one = Recipe(Ingredient, name="Chopped Tomatoes", user_id=1)
ingredient_two = Recipe(Ingredient, name="Garlic Bread", user_id=1)
ingredient_three = Recipe(Ingredient, name="Pasta", user_id=1)

# Meal

meal_one = Recipe(Meal, name="Meal 1", user_id=1)
meal_two = Recipe(Meal, name="Meal 2", user_id=1)
meal_three = Recipe(Meal, name="Meal 3", user_id=1)

# Plans

plan_one = Recipe(Plan, name="Plan 1", user_id=1, id=1)
plan_two = Recipe(Plan, name="Plan 2", user_id=1)
plan_three = Recipe(Plan, name="Plan 3", user_id=1)
