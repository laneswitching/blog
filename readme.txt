start server with 

>> python manage.py runserver

http://127.0.0.1:8000/admin
http://127.0.0.1:8000/

server also remote setup by pythonanywhere

drx.pythonanywhere.com


CLI Django

- from blog.models import Post
- Post.objects.all() <lists all (Posts)>
- Post.objects.create(author=me, title='sample', text='test') <creates a new post> (needs me assigned to a username)
- from django.contrib.auth.models import User 
- User.objects.all()
- me = User.objects.get(username='drx')
- Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

