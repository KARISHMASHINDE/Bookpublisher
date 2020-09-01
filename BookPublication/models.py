from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum



# Create your models here.
class Book(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE, null = True, blank = True)  
    book = models.TextField() #no limitation of line use
    publish_on = models.DateTimeField(auto_now_add=True, null = True, blank = True)
    votes = models.BooleanField(null = True, blank = True,default= False)

    def __str__(self):
        return '{} ' .format(self.book)
    
    def total_votes(self):
        return Book.objects.filter(votes=True).count()
    		
		
class Comment(models.Model):
    comment_by = models.ForeignKey(User,on_delete = models.CASCADE, null = True, blank = True)  
    bookId = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField()
    post_on = models.DateTimeField(auto_now_add=True, null = True, blank = True)
    
    def __str__(self):
        return  str(self.comment)

