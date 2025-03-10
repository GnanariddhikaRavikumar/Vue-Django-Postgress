from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Car  
from .serializers import CarSerializer
from django.http import JsonResponse
from django.core.exceptions import FieldError
from django.apps import apps


@csrf_exempt  
def CarList(request):
    if request.method == "GET":
        cars = Car.objects.all().values()  
        return JsonResponse(list(cars), safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)  
            car = Car.objects.create(
                name=data["name"],
                year=data["year"],
                selling_price=data["selling_price"],
                km_driven=data["km_driven"],
                fuel=data["fuel"],
                seller_type=data["seller_type"],
                transmission=data["transmission"],
                owner=data["owner"]
            )
            return JsonResponse({"message": "Car added successfully!", "id": car.id}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def CarDetail(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == "GET":
        return JsonResponse({
            "name": car.name,
            "year": car.year,
            "selling_price": car.selling_price,
            "km_driven": car.km_driven,
            "fuel": car.fuel,
            "seller_type": car.seller_type,
            "transmission": car.transmission,
            "owner": car.owner
        })

    elif request.method == "DELETE":
        car.delete()
        return JsonResponse({"message": "Car deleted successfully"}, status=204)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def db_check(request):
    return JsonResponse({"message": "Database is connected!"})


@api_view(['GET'])
def get_headers(request):
    """
    Returns the column headers for the Car model.
    """
    headers = [field.name for field in Car._meta.fields if field.name != 'id'] 
    return Response({"headers": headers})

@api_view(['GET'])
def group_cars(request, column):
    
    if column not in [field.name for field in Car._meta.fields]:
        return Response({"error": f"Invalid column name: {column}"}, status=400)

    cars = Car.objects.all()
    if not cars.exists():
        return Response({"message": "No cars found."}, status=404)

    grouped_dict = {}
    for car in cars:
        key = getattr(car, column, None)  
        if key is not None:
            if key not in grouped_dict:
                grouped_dict[key] = []
            grouped_dict[key].append(CarSerializer(car).data)

    all_items = [item for items in grouped_dict.values() for item in items]

    return Response({"grouped_data": all_items})



def distinct_values(request, column):
    if not column:
        return JsonResponse({"error": "Column name is required"}, status=400)

    # Validate if the column exists in the model
    model_fields = [field.name for field in Car._meta.get_fields()]
    if column not in model_fields:
        return JsonResponse({"error": f"Invalid column name: {column}"}, status=400)

    try:
        distinct_values = Car.objects.values_list(column, flat=True).distinct()
        return JsonResponse(list(distinct_values), safe=False)
    except FieldError:
        return JsonResponse({"error": "Invalid column name"}, status=400)
    

@api_view(["GET"])
def filter_cars(request):
    
    try:
        filters = {}
        for param, value in request.GET.items():
            if param in [field.name for field in Car._meta.get_fields()]:
                filters[f"{param}__icontains"] = value  

        filtered_cars = Car.objects.filter(**filters)

        serializer = CarSerializer(filtered_cars, many=True)
        return JsonResponse(serializer.data, safe=False)

    except FieldError:
        return JsonResponse({"error": "Invalid filter parameter"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)