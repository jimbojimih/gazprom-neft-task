import json
import os
import datetime
from pathlib import Path
from rest_framework import viewsets, views, status, generics, mixins
from .models import Category, Quote
from .serializers import CategorySerializer, QuoteSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer


class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class QuoteViewSet(viewsets.ModelViewSet):
	http_method_names = ['get', 'patch']
	serializer_class = QuoteSerializer
	queryset = Quote.objects.all()
	lookup_field = 'slug'

	def retrieve(self, request, slug): 
		pretty = request.query_params
		item = get_object_or_404(self.queryset, slug=slug)
		serializer = QuoteSerializer(item)
		response_data = serializer.data
		if pretty.keys() and list(pretty.keys())[0] == 'pretty':		
			return Response(data=response_data)

		return JsonResponse(response_data, json_dumps_params={'ensure_ascii':False})


class ImporterView(views.APIView):
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request):
		return Response(template_name='button.html')

	def post(self, request):
		folder = Path(__file__).parent.parent
		path = os.path.join(
				folder, "ruwikiquote-20230213-cirrussearch-general.json")
		with open(path, 'r', encoding='utf-8') as json_file:
			counter = 0
			for line in json_file:
				counter += 1
				if counter % 2 == 0:
					data = json.loads(line)
					self._db_create(data)                        
				else:
					continue  
		return Response(template_name='done.html')

	def _db_create(self, data):
		categories = data.get('category', None)
		create_timestamp = data.get('create_timestamp', None)
		timestamp = data.get('timestamp', None)
		language = data.get('language', None)
		wiki = data.get('wiki', None)
		title = data.get('title', None)
		auxiliary_text = data.get('auxiliary_text', None)

		category_obj_list = list()
		for category in categories:
			category_obj = Category.objects.get_or_create(
					title_category=category)[0]
			category_obj_list.append(category_obj)

		quote_obj = Quote.objects.create(
				language=language, 
				create_timestamp=create_timestamp, 
				timestamp=timestamp, 
				wiki=wiki, 
				title=title,
				auxiliary_text=auxiliary_text
		)

		for category_obj in category_obj_list:
			quote_obj.category.add(category_obj)
