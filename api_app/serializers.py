from rest_framework import serializers
from .models import Category, Quote
from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    count_of_quotes  = serializers.IntegerField(
        source='quotes.count', 
        read_only=True
    )

    class Meta:
        model = Category
        fields = ('id', 'title_category','count_of_quotes')


class QuoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    UNIX_create_timestamp = serializers.SerializerMethodField()
    UNIX_timestamp = serializers.SerializerMethodField()

    def get_UNIX_create_timestamp(self, obj):
        return obj.create_timestamp.timestamp()

    def get_UNIX_timestamp(self, obj):
        return obj.timestamp.timestamp()

    class Meta:
        model = Quote
        fields = '__all__'
        fields = ['category', 'UNIX_create_timestamp', 'UNIX_timestamp',
                  'language', 'wiki', 'title', 'auxiliary_text']
        read_only_fields = ['UNIX_create_timestamp', 'UNIX_timestamp',
                            'language', 'wiki',]
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

    def update(self, instance, validated_data):
        categories = validated_data.pop('category')
        instance.category.clear()
        for category in categories:
            title_category = category['title_category']
            category_obj = Category.objects.get_or_create(
                    title_category=title_category)[0]
            instance.category.add(category_obj)

        #it is necessary that the slug is not updated
        flag = False
        if (not validated_data.get('title') or 
                validated_data.get('title') == instance.title):
            flag = True

        instance.title = validated_data.get('title', instance.title)
        instance.auxiliary_text = validated_data.get('auxiliary_text', instance.auxiliary_text)
        instance.timestamp = datetime.now()
        instance.save(flag)
        return instance
        