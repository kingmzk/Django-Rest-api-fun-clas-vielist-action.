'''
from .models import Todo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TodoSerializer


@api_view(['GET', 'POST', 'PATCH'])
def home(request):
    if request.method == 'GET':
        return Response({
            "Status": 200,
            'Yes': 'Django - API Working!',
            'Method': 'GET'
        })

    elif request.method == 'POST':
        return Response({
            "Status": 200,
            'Yes': 'Django - API Working!',
            'Method': 'POST'
        })

    elif request.method == 'PATCH':
        return Response({
            "Status": 200,
            'Yes': 'Django - API Working!',
            'Method': 'PATCH'
        })

    else:
        return Response({
            "Status": 400,
            'Yes': 'Django - API Working!',
            'Method': 'Invalid Method'
        })


@api_view(['POST'])
def post_todo(request):
    try:
        data = request.data
        serializer = TodoSerializer(data=data)

        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({
                "status": True,
                'Message': 'Success data',
                'data': serializer.data
            })

        return Response({
            "status": False,
            'Message': 'Invalid data',
            'errors': serializer.errors
        })

    except Exception as e:
        print(e)
        return Response({
            "status": False,
            'Message': 'Something Went Wrong!'
        })


@api_view(['GET'])
def get_todo(request):
    todo_objs = Todo.objects.all()
    Serializer = TodoSerializer(todo_objs, many=True)

    return Response({
        'status': True,
        'message': "Todo Got SuccessFully",
        'data': Serializer.data
    })


@api_view(['PATCH'])
def patch_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
                "status": False,
                'Message': 'uid is Required'
            })

        obj = Todo.objects.get(uid=data.get('uid'))
        serializer = TodoSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({
                "status": True,
                'Message': 'Success data',
                'data': serializer.data
            })

        return Response({
            "status": False,
            'Message': 'Invalid data',
            'errors': serializer.errors
            })

    except Exception as e:
        print(e)
        return Response({
            "status": False,
            'Message': 'invalid uid!'
        })

@api_view(['DELETE'])
def delete_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
                "status": False,
                'Message': 'uid is Required'
            })

        obj = Todo.objects.get(uid=data.get('uid'))
        obj.delete()
        return Response({
            "status": True,
            'Message': 'Todo deleted successfully'
        })

    except Exception as e:
        print(e)
        return Response({
            "status": False,
            'Message': 'Invalid uid!'
        })
        
        
        
        
        
@api_view(['PUT'])
def put_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
                "status": False,
                'Message': 'uid is Required'
            })

        obj = Todo.objects.get(uid=data.get('uid'))
        serializer = TodoSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                'Message': 'Success data',
                'data': serializer.data
            })

        return Response({
            "status": False,
            'Message': 'Invalid data',
            'errors': serializer.errors
        })

    except Exception as e:
        print(e)
        return Response({
            "status": False,
            'Message': 'Invalid uid!'
        })
   
        
   '''


# Class - Based


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import TodoSerializer
from .models import Todo
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from .helpers import paginate
from rest_framework.exceptions import ValidationError


'''
class TodoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # print(request.user)
 
        # todo_objs = Todo.objects.all()
        todo_objs = Todo.objects.filter(user = request.user)
        
        page = request.GET.get('page',1)
        page_obj = Paginator(todo_objs,page)
        # print(page_obj)
        results = paginate(todo_objs, page_obj, page)
        # print(results)
        
        # serializer = TodoSerializer(todo_objs, many=True)
        serializer = TodoSerializer(results['results'], many=True)
        return Response({
            'status': True,
            'message': "Todo Retrieved Successfully",
            'data': {'data':serializer.data, 'paginator':results['pagination']}
        })
'''

class TodoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        todo_objs = Todo.objects.filter(user=request.user)
        
        page = request.GET.get('page', 1)
        page_size = 3  # Set the desired page size to 2
        page_obj = Paginator(todo_objs, page_size)
        
        try:
            results = paginate(todo_objs, page_obj, page, page_size)
        except ValidationError as e:
            return Response({
                'status': False,
                'message': str(e.detail),
                'data': None
            }, status=e.status_code)
        
        serializer = TodoSerializer(results['results'], many=True)
        return Response({
            'status': True,
            'message': "Todo Retrieved Successfully",
            'data': {'data': serializer.data, 'paginator': results['pagination']}
        })



    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer  = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                'message': 'Todo Created Successfully',
                'data': serializer.data
            })
        return Response({
            "status": False,
            'message': 'Invalid data',
            'errors': serializer.errors
        })

    def put(self, request):
        data = request.data
        uid = data.get('uid')
        if not uid:
            return Response({
                "status": False,
                'message': 'uid is Required'
            })

        try:
            todo_obj = Todo.objects.get(uid=uid)
        except Todo.DoesNotExist:
            return Response({
                "status": False,
                'message': 'Todo not found',
            })

        serializer = TodoSerializer(todo_obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                'message': 'Todo Updated Successfully',
                'data': serializer.data
            })
        return Response({
            "status": False,
            'message': 'Invalid data',
            'errors': serializer.errors
        })

    def patch(self, request):
        data = request.data
        uid = data.get('uid')
        if not uid:
            return Response({
                "status": False,
                'message': 'uid is Required'
            })

        try:
            todo_obj = Todo.objects.get(uid=uid)
        except Todo.DoesNotExist:
            return Response({
                "status": False,
                'message': 'Todo not found',
            })

        serializer = TodoSerializer(todo_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                'message': 'Todo Patched Successfully',
                'data': serializer.data
            })
        return Response({
            "status": False,
            'message': 'Invalid data',
            'errors': serializer.errors
        })

    def delete(self, request):
        data = request.data
        uid = data.get('uid')
        if not uid:
            return Response({
                "status": False,
                'message': 'uid is Required'
            })

        try:
            todo_obj = Todo.objects.get(uid=uid)
        except Todo.DoesNotExist:
            return Response({
                "status": False,
                'message': 'Todo not found',
            })

        todo_obj.delete()
        return Response({
            "status": True,
            'message': 'Todo deleted successfully'
        })
            

# VIEWSETS



'''from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import TimingTodo
from .models import Todo
from .serializer import TimingTodoSerializer, TodoSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, permissions

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    # allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    
    
    
    @action(detail=False, methods=['GET'])
    def get_timing_todo(self, request):
        objs = TimingTodo.objects.all()
        serializer = TimingTodoSerializer(objs, many=True)
        return Response({
            'status':True,
            'message': 'Timing Todo Fetched',
            'data': serializer.data
        })
        
    
    

    @action(detail=False, methods=['post'])
    def add_data_to_todo(self, request):
        try:
            data = request.data
            serializer = TimingTodoSerializer(data = data)
            if serializer.is_valid():
                print(serializer.validated_data)
                serializer.save()
                return Response({
                    "status": True,
                    'Message': 'Success data',
                    'data': serializer.data
                })

            return Response({
                "status": False,
                'Message': 'Invalid data',
                'errors': serializer.errors
            })

        except Exception as e:
            print(e)
            return Response({
                "status": False,
                'Message': 'Something Went Wrong!'
            })
'''
