from rest_framework import serializers

from .day import *
from .ingredients import *
from .meal import *
from .meal_ingredients import *
from .plan import *
from .section import *
from .store import *


class GetAllSerializer(serializers.Serializer):
    stores = StoreSerializer(many=True)
    sections = SectionSerializer(many=True)
    plans = PlanSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    meals = MealSerializer(many=True)
