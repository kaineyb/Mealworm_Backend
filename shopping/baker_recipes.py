from model_bakery.recipe import Recipe

from shopping.models import Ingredient, Meal, Plan, Section, Store

# Stores

store_one = Recipe(Store, name="Test Store 1")
store_two = Recipe(Store, name="Test Store 2")
store_three = Recipe(Store, name="Test Store 3")

# Sections

section_one = Recipe(Section, name="Test Section 1")
section_two = Recipe(Section, name="Test Section 2")
section_three = Recipe(Section, name="Test Section 3")

#  Ingredients

ingredient_one = Recipe(Ingredient, name="Test Ingredient 1")
ingredient_two = Recipe(Ingredient, name="Test Ingredient 2")
ingredient_three = Recipe(Ingredient, name="Test Ingredient 3")

# Meal

meal_one = Recipe(Meal, name="Test Meal 1")
meal_two = Recipe(Meal, name="Test Meal 2")
meal_three = Recipe(Meal, name="Test Meal 3")

# Plans

plan_one = Recipe(Plan, name="Test Plan 1", id=1)
plan_two = Recipe(Plan, name="Test Plan 2")
plan_three = Recipe(Plan, name="Test Plan 3")
