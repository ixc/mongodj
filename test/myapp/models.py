from django.db import models

class Blog(models.Model):
    _id = models.GenericAutoField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "Blog: %s" % self.title
    
class Entry(models.Model):
    _id = models.GenericAutoField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    blog = models.ForeignKey(Blog)
    
    def __unicode__(self):
        return "Entry: %s in the blog '%s'" % (self.title, self.blog)