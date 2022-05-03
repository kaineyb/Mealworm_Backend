from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from shopping.serializers import ingredients
from shopping.serializers.meal import MealSerializer

from . import models, serializers

# Create your views here.


@api_view()
def get_all(request):
    user = request.user

    stores = models.Store.objects.filter(user_id=user.id)
    sections = models.Section.objects.filter(user_id=user.id)

    plans = models.Plan.objects.filter(user_id=user.id).prefetch_related("day_set")
    ingredients = models.Ingredient.objects.filter(user_id=user.id)
    meals = models.Meal.objects.filter(user_id=user.id).prefetch_related(
        "meal_ingredients"
    )

    data = {
        "stores": stores,
        "sections": sections,
        "plans": plans,
        "ingredients": ingredients,
        "meals": meals,
    }

    serializer = serializers.GetAllSerializer(data)

    return Response(serializer.data)


class StoreViewSet(ModelViewSet):
    """
    Using StoreViewSet() which only uses StoreSerializer
    """

    serializer_class = serializers.StoreSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        return models.Store.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return serializers.UpdateStoreSerializer
        return serializers.StoreSerializer


class SectionViewSet(ModelViewSet):
    """
    Using SectionViewSet() which only uses SectionSerializer
    """

    serializer_class = serializers.SectionSerializer
    http_method_names = ["get", "post", "patch", "put", "delete", "head", "options"]

    def get_queryset(self):
        """
        Only show sections that were created by that user
        """
        user = self.request.user
        return models.Section.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return serializers.UpdateSectionSerializer
        return serializers.SectionSerializer


class StoreAisleViewSet(ModelViewSet):
    """
    Using StoreAisleViewSet which only uses StoreAisleSerializer
    """

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return serializers.UpdateStoreAisleSerializer
        return serializers.StoreAisleSerializer

    def get_serializer_context(self):

        return {
            "user_id": self.request.user.id,
            "section_id": self.kwargs["section_pk"],
        }

    def get_queryset(self):
        """
        Only show Days that were created by that user
        """

        return models.StoreAisle.objects.filter(section_id=self.kwargs["section_pk"])


class PlanViewSet(ModelViewSet):
    """
    Using PlanViewSet() which only uses PlanSerializer
    """

    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return serializers.UpdatePlanSerializer
        return serializers.PlanSerializer

    def get_queryset(self):
        """
        Only show Plans that were created by that user
        """

        user = self.request.user
        return models.Plan.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class DayViewSet(ModelViewSet):
    """
    Using DayViewSet() which uses DaySerializer and UpdateDaySerializer only for Patch Requests
    """

    serializer_class = serializers.DaySerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "plan_id": self.kwargs["plans_pk"]}

    def get_queryset(self):
        """
        Only show Days that were created by that user
        """

        return models.Day.objects.filter(
            plan_id=self.kwargs["plans_pk"]
        ).select_related("meal")

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return serializers.UpdateDaySerializer
        elif self.request.method == "POST":
            return serializers.CreateDaySerializer
        return serializers.DaySerializer


class IngredientViewSet(ModelViewSet):
    """
    Using IngredientViewSet() which uses IngredientSerializer
    """

    serializer_class = serializers.IngredientSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        return models.Ingredient.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return serializers.UpdateIngredientSerializer
        return serializers.IngredientSerializer


class MealViewSet(ModelViewSet):
    """
    Using MealViewSet which uses MealSerializer and UpdateMealSerializer for PATCH
    """

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    serializer_class = MealSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Meal.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    # def get_serializer_class(self):
    #     if self.request.method == "POST":
    #         return serializers.CreateMealSerializer
    #     elif self.request.method == "PATCH":
    #         return serializers.UpdateMealSerializer
    #     return serializers.MealSerializer


class MealIngredientViewSet(ModelViewSet):
    """
    Using MealIngredientViewSet which uses MealIngredientSerializer
    """

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "meals_pk": self.kwargs["meals_pk"]}

    def get_queryset(self):
        return models.MealIngredient.objects.filter(meal_id=self.kwargs["meals_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateMealIngredientSerializer
        elif self.request.method == "PATCH":
            return serializers.UpdateMealIngredientSerializer
        return serializers.MealIngredientSerializer
