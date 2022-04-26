from rest_framework.viewsets import ModelViewSet
from .models import (
    Ingredient,
    MealIngredient,
    Store,
    Section,
    Plan,
    Day,
    Meal,
    StoreAisle,
)
from .serializers import (
    CreateDaySerializer,
    CreateMealIngredientSerializer,
    CreateMealSerializer,
    DaySerializer,
    IngredientSerializer,
    MealIngredientSerializer,
    MealSerializer,
    PlanSerializer,
    SectionSerializer,
    StoreAisleSerializer,
    StoreSerializer,
    UpdateDaySerializer,
    UpdateIngredientSerializer,
    UpdateMealIngredientSerializer,
    UpdateMealSerializer,
    UpdatePlanSerializer,
    UpdateSectionSerializer,
    UpdateStoreAisleSerializer,
    UpdateStoreSerializer,
)

# Create your views here.


class StoreViewSet(ModelViewSet):
    """
    Using StoreViewSet() which only uses StoreSerializer
    """

    serializer_class = StoreSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        return Store.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateStoreSerializer
        return StoreSerializer


class SectionViewSet(ModelViewSet):
    """
    Using SectionViewSet() which only uses SectionSerializer
    """

    serializer_class = SectionSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        """
        Only show sections that were created by that user
        """
        user = self.request.user
        return Section.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateSectionSerializer
        return SectionSerializer


class StoreAisleViewSet(ModelViewSet):
    """
    Using StoreAisleViewSet which only uses StoreAisleSerializer
    """

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateStoreAisleSerializer
        return StoreAisleSerializer

    def get_serializer_context(self):

        return {
            "user_id": self.request.user.id,
            "section_id": self.kwargs["section_pk"],
        }

    def get_queryset(self):
        """
        Only show Days that were created by that user
        """

        return StoreAisle.objects.filter(section_id=self.kwargs["section_pk"])


class PlanViewSet(ModelViewSet):
    """
    Using PlanViewSet() which only uses PlanSerializer
    """

    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdatePlanSerializer
        return PlanSerializer

    def get_queryset(self):
        """
        Only show Plans that were created by that user
        """

        user = self.request.user
        return Plan.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class DayViewSet(ModelViewSet):
    """
    Using DayViewSet() which uses DaySerializer and UpdateDaySerializer only for Patch Requests
    """

    serializer_class = DaySerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "plan_id": self.kwargs["plans_pk"]}

    def get_queryset(self):
        """
        Only show Days that were created by that user
        """

        return Day.objects.filter(plan_id=self.kwargs["plans_pk"]).select_related(
            "meal"
        )

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateDaySerializer
        elif self.request.method == "POST":
            return CreateDaySerializer
        return DaySerializer


class IngredientViewSet(ModelViewSet):
    """
    Using IngredientViewSet() which uses IngredientSerializer
    """

    serializer_class = IngredientSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        return Ingredient.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateIngredientSerializer
        return IngredientSerializer


class MealViewSet(ModelViewSet):
    """
    Using MealViewSet which uses MealSerializer and UpdateMealSerializer for PATCH
    """

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        return Meal.objects.filter(user_id=user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateMealSerializer
        elif self.request.method == "PATCH":
            return UpdateMealSerializer
        return MealSerializer


class MealIngredientViewSet(ModelViewSet):
    """
    Using MealIngredientViewSet which uses MealIngredientSerializer
    """

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_context(self):
        return {"user_id": self.request.user.id, "meals_pk": self.kwargs["meals_pk"]}

    def get_queryset(self):
        return MealIngredient.objects.filter(meal_id=self.kwargs["meals_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateMealIngredientSerializer
        elif self.request.method == "PATCH":
            return UpdateMealIngredientSerializer
        return MealIngredientSerializer
