from collections import OrderedDict

from rest_framework import serializers

from ..models import Day, Meal


class NewListSerializer(serializers.ListSerializer):
    def update(self, validated_data, instance):

        list_of_instances = []

        for each_update in validated_data:
            id = each_update.get("id")

            example_table_object: Day = Day.objects.filter(pk=id).first()

            del validated_data["id"]

            if id and example_table_object:
                list_of_instances.append(
                    Day.objects.update(example_table_object, validated_data)
                )

            else:
                list_of_instances.append(Day.objects.create(validated_data))

        return list_of_instances
