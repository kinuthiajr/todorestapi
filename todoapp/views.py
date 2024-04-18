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

"""" Detail View """
class TodoDetailViewApi(APIView):
     # permissions to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,todo_id,user_id):
        """"
        Helper method that gets an object given todo id and user id
        """
        try:
            return Todo.objects.get(id=todo_id,user=user_id)
        except Todo.DoesNotExist:
            return None
    
    # 3. Retrieve
    def get(self, request,todo_id,*args,**kwargs):
        """"
        Retrieves all todos with a given todo_id
        """
        todo_instance = self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response({'res':"Object with the todo id does not exist"},status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # 4. Update
    def put(self,request,todo_id,*args,**kwargs):
        """"
        Edits item todo with given todo_id if exists
        """
        todo_instance = self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response({'res':"Object with the todo id does not exist"},status=status.HTTP_400_BAD_REQUEST)
        data = {
            'task':request.data.get('task'),
            'completed':request.data.get('completed'),
            'user':request.user.id
        }
        serializer = TodoSerializer(instance=todo_instance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self,request,todo_id,*args,**kwargs):
        """
        Destroy a todo item if exists given its todo id
        """
        todo_instance = self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response({'res':"Object with the todo id does not exist"},status=status.HTTP_400_BAD_REQUEST)
        todo_instance.delete()
        return Response({'res':"Object deleted!"},status=status.HTTP_200_OK)