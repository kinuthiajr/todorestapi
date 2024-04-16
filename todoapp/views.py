from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

class TodoListApiView(APIView):
    # add permissions to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1 list all
    def get(self,request,*args,**kwargs):
        """
        list all tasks by a user
        """
        todos = Todo.objects.filter(user=request.user.id)
        serializer = TodoSerializer(todos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # 2 Create a Todo by a user
    def post(self,request,*args,**kwargs):
        """"
        Create a todo with a given data by a user
        """
        data = {
            'task':request.data.get('task'),
            'completed':request.data.get('completed'),
            'user':request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    