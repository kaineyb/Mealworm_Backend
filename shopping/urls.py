from cgitb import lookup
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

# Stores and Sections
router.register("stores", views.StoreViewSet, basename="store")
router.register("sections", views.SectionViewSet, basename="section")

section_router = routers.NestedDefaultRouter(router, "sections", lookup="section")
section_router.register("aisles", views.StoreAisleViewSet, basename="section-aisles")


# Plans and Nested Days
router.register("plans", views.PlanViewSet, basename="plans")
plans_router = routers.NestedDefaultRouter(router, "plans", lookup="plans")
plans_router.register("days", views.DayViewSet, basename="plan-days")

# Ingredients and Meals
router.register("ingredients", views.IngredientViewSet, basename="ingredients")

router.register("meals", views.MealViewSet, basename="meals")
meals_router = routers.NestedDefaultRouter(router, "meals", lookup="meals")
meals_router.register(
    "ingredients", views.MealIngredientViewSet, basename="meal-ingredients"
)

urlpatterns = router.urls + plans_router.urls + section_router.urls + meals_router.urls
