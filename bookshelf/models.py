from django.db import models

class book(models.Model):
	title=models.CharField(max_length=50)
	author=models.CharField(max_length=100)
	bookKey=models.CharField(max_length=40,unique=True)
	def __unicode__(self):
		return self.title

class comment(models.Model):
	book=models.ForeignKey(book)
	comment=models.CharField(max_length=500)
