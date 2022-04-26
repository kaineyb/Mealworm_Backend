from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.


class Section(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f"Section(id={self.id}, name={self.name})"


class StoreAisle(models.Model):
    store = models.ForeignKey("Store", on_delete=models.CASCADE)
    section = models.ForeignKey("Section", on_delete=models.CASCADE)
    aisle_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"In {self.store} {self.section} is on Aisle {self.aisle_number}"

    def __repr__(self):
        return f"StoreAisle(store={self.store}, section={self.section}, aisle_number={self.aisle_number})"


class Store(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Store(id={self.id}, name={self.name})"


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Ingredient(id={self.id}, name={self.name}, section={self.section})"

    class Meta:
        ordering = ["section", "name"]


class MealIngredient(models.Model):
    measurements = [
        (" x ", "Items"),
        ("g", "Grams"),
        ("kg", "Kilograms"),
        ("ml", "Millilitres"),
        ("l", "Litres"),
    ]
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, related_name="actual_ingredient"
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit = models.CharField(max_length=255, choices=measurements)
    meal = models.ForeignKey(
        "Meal", blank=True, on_delete=models.CASCADE, related_name="meal_ingredients"
    )
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient} "

    def __repr__(self):
        return f"{self.quantity}{self.unit} {self.ingredient}"


class Meal(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Meal(name={self.name}, id={self.id})"


class Plan(models.Model):
    days = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    ]

    last_update = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_day = models.CharField(max_length=255, choices=days)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Plan(id={self.id}, name={self.name}, start_day={self.start_day})"


class Day(models.Model):
    """
    Model for a Day, used in Plans.
    Bridges Meals and Plans
    """

    # plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan_days")
    # meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="plan_meals")

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan_days")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="plan_meals")

    order = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Day: {self.order}"

    def __repr__(self):
        return f"Day(id={self.id}, plan_id={self.plan.id}, order={self.order}, meal_id={self.meal})"

    class Meta:
        ordering = ["order"]
