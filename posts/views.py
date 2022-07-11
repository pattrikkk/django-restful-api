from django.http import JsonResponse
from requests import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from .utils import check_if_userid_exists
from .utils import check_if_post_exists
import requests

@api_view(['GET', 'POST'])
def post_list(request):
    #Získa všetky príspevky
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    #Vytvorí nový príspevok
    if request.method == 'POST':
        #Kontrola či userid existuje
        if not check_if_userid_exists(request):
            return JsonResponse({'error': 'Userid does not exist'}, status=400)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PATCH', 'DELETE'])
def post_detail(request, postid):
    #Kontrola či príspevok existuje
    try:
        post = Post.objects.get(postid=postid)
    except Post.DoesNotExist:
        #Ak neexistuje, tak skontroluje externú API
        responsePosts = check_if_post_exists(postid)
        #Ak sa nenašiel príspevok, tak vráti chybu
        if not responsePosts or request.method != 'GET':
            return JsonResponse({'error': 'Post with this id does not exist'}, status=404)
        #Príspevok sa našiel, tak ho uloží
        post = Post.objects.create(postid=postid, title=responsePosts['title'], body=responsePosts['body'], userid=responsePosts['userId'])

    #Získa príspevok
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, status=200)

    #Upraví príspevok
    if request.method == 'PATCH':
        #Kontrola či používateľ nemení userid a postid
        if 'postid' in request.data or 'userid' in request.data:
            return JsonResponse({'error': 'Cannot modify userid or postid'}, status=400)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)

    #Zmazanie príspevku
    if request.method == 'DELETE':
        post.delete()
        return JsonResponse({'deleted': 'Post successfully deleted'}, status=204)
