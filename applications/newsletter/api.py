from django.http import JsonResponse
from .models import Subscibers
import json

def api_add_subscriber(request):
	data = json.loads(request.body)
	email = data['email']
	Subscibers.objects.create(email=email)

	return JsonResponse({'SUCCESS':True})