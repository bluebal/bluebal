from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime, os

def u_slug(instance,name, slug_field, max_length=50):
	slug = slugify(name)[:(max_length - 5)]
	curSlug=None
	try:
		curSlug=getattr(instance, slug_field)
	except:
		pass
	qs=instance.__class__.objects.exclude(slug=curSlug)
	all = [obj.values()[0] for obj in qs.values(slug_field)]
	if slug in all:
		import re
		counterFinder = re.compile(r'-\d+$')
		counter = 2
		slug = "%s-%i" % (slug, counter)
		while slug in all:
			slug = re.sub(counterFinder,"-%i" % counter, slug)
			counter += 1
	return slug

class DateClass(models.Model):
	created=models.DateTimeField( default=datetime.datetime.now, editable=False )
	revised=models.DateTimeField( editable=False )
	
	class Meta:
		abstract=True
		
	def save(self, *args, **kwargs):
		self.revised=datetime.datetime.now()
		super(DateClass, self).save(*args, **kwargs)

class Hammer(models.Model):
    ''' A list object. It contains items...that's all'''
    creator=models.ForeignKey( User, related_name="hammers", null=True )
    created=models.DateTimeField()
    revised=models.DateTimeField( default=datetime.datetime.now )
    cxr=models.CharField( max_length=50, null=True ) # hammer constructor - a registered name which adds functionality to a hammer
    theme=models.CharField( max_length=25, default="default" )
    name=models.CharField(max_length=100)
    slug=models.SlugField( blank=True, editable=False )
    
    def save(self, *args, **kwargs):
        try:
            reslug=kwargs.pop('reslug')
        except:
            reslug=False
        if not self.slug or reslug:
            self.slug=u_slug(self, self.name, 'slug')
        if not self.created:
            self.created=datetime.datetime.now()
        self.revised=datetime.datetime.now()
        return super(Hammer, self).save(*args, **kwargs)
    
    class Meta:
        ordering=('name',)
    
    def __unicode__(self):
        return self.name

    
    
class HammerItem( models.Model ):
    ''' An item on a list '''
    creator=models.ForeignKey( User, related_name="items" )
    hammer=models.ForeignKey( Hammer, related_name="items" )
    title=models.CharField( max_length=100, default="ITEM" )
    raw=models.TextField( null=True, blank=True )
    index=models.IntegerField( default=0 )
    status=models.CharField( max_length=100, default="idle" )
    
    class Meta:
        ordering=( 'index', )


class HammerShare( models.Model ):
    ''' a connection between a list and a user with which it is shared '''
    sharee=models.ForeignKey( User, related_name="shares" )
    hammer=models.ForeignKey( Hammer, related_name="shares" )
    theme=models.CharField( max_length=25, default="default" ) # user override of the theme
    can_add=models.BooleanField( default=True, blank=True ) # add an item
    can_remove=models.BooleanField( default=True, blank=True ) # remove an item
    can_change=models.BooleanField( default=True, blank=True ) # change an item
    can_share=models.BooleanField( default=True, blank=True ) # re share the hammer

class HammerCheckin( models.Model ):
    ''' a record of when a user has last checked in for changes to hammers shared with them'''
    user=models.ForeignKey( User, related_name="checkins" )
    checkin=models.DateTimeField( default=datetime.datetime.now )
    
class AbstractHammerData( models.Model ):
    theme=models.CharField( max_length=50, default="default" )
    numbered=models.BooleanField( default=True ) #show line numbers?
    class Meta:
        abstract=True
    
class HammerData( AbstractHammerData ):
    '''a connection between a hammer and a user which defines settings '''
    hammer=models.ForeignKey( Hammer, related_name="data" )
    user=models.ForeignKey( User, related_name="data" )
    
class HammerDataDefault( AbstractHammerData ):
    ''' user defaults for new hammers '''
    user=models.ForeignKey( User, related_name="default_data" )
    
class UserPreference( models.Model ):
    ''' global settings for a user '''
    user=models.OneToOneField( User, unique=True )
    date_format=models.CharField( max_length=40, default="%B %d, %Y" )
    military=models.BooleanField( default=False )