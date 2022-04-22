from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    search_fields = ["name__istartswith", "user__username"]
    list_filter = [
        "user__username",
    ]
    list_display = ["name", "added", "user"]


class StoreAisleInline(admin.TabularInline):
    model = models.StoreAisle


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    inlines = [StoreAisleInline]
    search_fields = ["name", "user__username"]
    list_filter = ["user__username"]
    list_display = ["name", "added", "user"]


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name__istartswith", "user__username__istartswith"]
    autocomplete_fields = ["section", "user"]
    list_filter = ["user__username", "section"]
    list_display = ["name", "section", "added", "user"]


class MealIngredientInline(admin.TabularInline):
    model = models.MealIngredient
    autocomplete_fields = ["ingredient"]


@admin.register(models.Meal)
class MealAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    inlines = [MealIngredientInline]
    list_filter = ["user__username"]
    list_display = ["name", "added", "user"]


class DayInline(admin.TabularInline):
    model = models.Day
    ordering = ["order"]


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    search_fields = ["name__istartswith", "user__username__istartswith"]
    autocomplete_fields = ["user"]
    list_filter = ["user__username", "start_day", "last_update"]
    list_display = ["name", "start_day", "added", "user"]
    inlines = [DayInline]
