from django.shortcuts import render
from .models import Book,Comment
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from django.http import Http404
from rest_framework.decorators import api_view,permission_classes
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  
from  BookPublication.serializers import RegistrationSerializer
import ast

# Create your views here.



@api_view(['POST', ])
def registration_view(request):

	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			user= serializer.save(request.user)
			data['response'] = 'successfully registered new user.'
			data['username'] = user.username
			
		else:
			data = serializer.errors
		return Response(data) 


@api_view(["POST",])
@permission_classes((IsAuthenticated,))
def login(request):
    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'message':'Sucessfully Logged In'},
                        status=HTTP_200_OK)



@api_view(['GET','POST'])
def get_comment(request):  
    if request.method=='GET':
        data=[]
        try:
            obj=Comment.objects.all()
            for x in obj:
                com={
                    "comment_by":x.comment_by,
                    "bookName":x.bookId,
                    "comment":x.comment,
                    "post_on":x.post_on,
              
                }
                data.append({"field":com})
        
          
            json_data= json.dumps(data,indent=4, sort_keys=True, default=str)
            status_code = status.HTTP_200_OK
            res= ast.literal_eval(json_data)
            return Response(res, status = status_code) 
           
        except ObjectDoesNotExist:
            return Response({"error " : "Comment obj doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
        
       
    if request.method == 'POST':
        
        
        try:
            user = request.GET.get('user')
            bookName = request.GET.get('bookName')
            comment = request.GET.get('comment')
            bookId = Book.objects.get(book=bookName)
            comment_by = User.objects.get(username=user)
            
            div = Comment(comment_by=comment_by,
                          bookId=bookId,
                comment=comment,
                )
            
            div.save()
            res = {
                    
                  
                    "comment_by": div.comment_by,
                    "bookName" : div.bookId,
                    "post_on":div.post_on,
                    "comment":div.comment,
                  
            }
            json_data= json.dumps(res,indent=4, sort_keys=True, default=str)
            status_code = status.HTTP_200_OK
            result= ast.literal_eval(json_data)
            return Response(result, status = status_code)

        except ObjectDoesNotExist:
            res = {"error": "you are unauthorized to perform this action."}
        status_code = status.HTTP_400_BAD_REQUEST
        
@api_view(['DELETE',])
def delete_comment(request,id):          
    if request.method == 'DELETE':
        try:
            div_obj = Comment.objects.get(id=id).delete()
            return Response({"success" : "Comment is deleted."}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error " : "Comment obj doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET','POST'])
def bookauthor(request):  
    if request.method=='GET':
        data=[]
        try:
            obj=Book.objects.all()
            for x in obj:
                com={
                    
                    "bookName":x.book,
                    "author":x.author,
                    "publish_on":x.publish_on,
                    "votes":str(x.total_votes())
              
                }
                data.append({"field":com})
        
          
            json_data= json.dumps(data,indent=4, sort_keys=True, default=str)
            status_code = status.HTTP_200_OK
            res= ast.literal_eval(json_data)
            return Response(res, status = status_code) 
           
        except ObjectDoesNotExist:
            return Response({"error " : "Comment obj doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
        
       
    if request.method == 'POST':
        
        
        try:
            user = request.GET.get('user')
            bookName = request.GET.get('bookName')
            comment = request.GET.get('comment')
            author = User.objects.get(username=user)
            
            div = Book(author=author,
                        book=bookName,
                       
                )
            
            div.save()
            res = {
                    
                "author":div.author,
                "bookName" : div.book,
                "publish_on":div.publish_on,
                
                  
            }
            json_data= json.dumps(res,indent=4, sort_keys=True, default=str)
            status_code = status.HTTP_200_OK
            result= ast.literal_eval(json_data)
            return Response(result, status = status_code)

        except ObjectDoesNotExist:
            res = {"error": "you are unauthorized to perform this action."}
        status_code = status.HTTP_400_BAD_REQUEST