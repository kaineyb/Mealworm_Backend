from django.urls import include, path
from rest_framework_nested import routers as nested_routers

from . import views

n_router = nested_routers.DefaultRouter()


# Stores and Sections
n_router.register("stores", views.StoreViewSet, basename="store")

store_router = nested_routers.NestedDefaultRouter(n_router, "stores", lookup="stores")
store_router.register("aisles", views.StoreAisleViewSet, basename="stores-aisles")

n_router.register("sections", views.SectionViewSet, basename="section")


# Plans and Nested Days
n_router.register("plans", views.PlanViewSet, basename="plans")
plans_router = nested_routers.NestedDefaultRouter(n_router, "plans", lookup="plans")
plans_router.register("days", views.DayViewSet, basename="plan-days")

# Ingredients and Meals
n_router.register("ingredients", views.IngredientViewSet, basename="ingredients")

n_router.register("meals", views.MealViewSet, basename="meals")
meals_router = nested_routers.NestedDefaultRouter(n_router, "meals", lookup="meals")
meals_router.register(
    "ingredients", views.MealIngredientViewSet, basename="meal-ingredients"
)


router_urls = n_router.urls + plans_router.urls + store_router.urls + meals_router.urls

urlpatterns = [path("get_all/", views.get_all), *router_urls]
