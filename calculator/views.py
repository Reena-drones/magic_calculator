from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .utils import available_operations, wrap_available_operations
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from .models import Methods
from .Exceptions import NotValidOperation
import json
from .functions import *
from .forms import OperationForm, AddOperationForm

# Create your views here.


def index(request):
    form = OperationForm()
    return render(request, 'calculator.html', {'form': form})


@csrf_exempt
def functions(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)["type"]
            insert_function(data)
            return JsonResponse('Inserted successfully', safe=False)
        except KeyError:
            return HttpResponseBadRequest('Invalid data. Try type key')
        except NotValidOperation:
            return HttpResponseBadRequest('Not a valid mathematical operation. Please check /valid_operations')
        except Exception:
            return HttpResponseBadRequest('Error inserting data')

    if request.method == 'GET':
        out = get_function()
        return out

    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)['type']
            delete_function(data)
            return JsonResponse('Operation deleted successfully', safe=False)
        except Exception as e:
            return JsonResponse(e, safe=False)


def new_check(elem):
    try:
        float(elem)
        return True
    except ValueError:
        raise ValueError("Only float and integers allow")


def format_res(elem):
    if new_check(elem):
        try:
            o = int(elem)
            return o
        except ValueError:
            o = float(elem)
            return o

@csrf_exempt
def operate_function(request):
    op_form = OperationForm(request.POST)
    try:
        if op_form.is_valid():
            op = request.POST.get('operation')
            p = json.loads(request.POST.get('params'))
            if not isinstance(p, list):
                return render(request, 'calculator.html',
                              {'form': op_form, 'error': 'Invalid data. Send list of arguments only'})
            formatted_params = list(map(format_res, p))
            out = operate_math(op, *formatted_params)
            return render(request, 'calculator.html', {'form': op_form, 'out': str(out)})
        else:
            return render(request, 'calculator.html',
                          {'form': op_form, 'error': 'Invalid data. Send list of arguments only'})
    except Exceptions.TwoArgumentNeeded:
        return render(request, 'calculator.html', {'form': op_form, 'error': 'Invalid data. Only Two arguments allowed for this operation'})

    except Exceptions.OneArgumentNeeded:
        return render(request, 'calculator.html', {'form': op_form, 'error': 'Invalid data. Only One arguments allowed for this operation'})

    except Exceptions.IntgerAllowed:
        return render(request, 'calculator.html', {'form': op_form, 'error': 'Invalid data. Only integer is allowed for this function'})

    except Exception as e:
        return render(request, 'calculator.html',{'form': op_form, 'error': e})


def valid_operations(request):
    if request.method == 'GET':
        form = AddOperationForm()
        return render(request, 'add.html', {'methods': form})
    return HttpResponseNotAllowed


def get_function():
    function_list = Methods.objects.all()
    out = []
    for e in function_list:
        out.append(e.name)
    return out


def insert_function(data):
    if data not in wrap_available_operations():
        raise NotValidOperation
    Methods.objects.create(name=data)
    return


def delete_function(data):
    Methods.objects.filter(name=data).delete()
    return



