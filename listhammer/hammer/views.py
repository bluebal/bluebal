from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView, View, FormView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.edit import FormView
from django.conf import settings

from .models import Hammer, HammerItem, HammerShare, HammerCheckin, UserPreference, HammerDataDefault, HammerData
from .forms import HammerForm, HammerItemForm, HammerShareForm, UserPreferenceForm, HammerDataForm, HammerDataDefaultForm


import urlparse
import datetime
import string
import random
import json
import os

def date_format( datestring, toPython=False ):
	''' take a python date format and return the javasript $.datepicker equivalent, set toPython to True to do the reverse'''
	pairs=[
		( '%d', 'd' ), # day of month
		( '%Y', 'yy' ), # 4 digit year
		( '%B', 'MM' ), # month name long
	]
	ds='%s' % datestring
	for pair in pairs:
		fr=pair[( 1 if toPython else 0 )]
		to=pair[( 0 if toPython else 1 )]
		ds=ds.replace( fr, to )
	return ds
	
def hammer_record( hammer, items=True, shares=True ):
    ret={
        'id': hammer.pk,
        'name': hammer.name,
        'creator': hammer.creator.username,
        'created': datetime.date.strftime( hammer.created, '%B %d, %Y' ),
		'can_add': True,
		'can_remove': True,
		'can_change': True,
		'theme': hammer.theme,
		'shared': False,
        'items':[] if not items else [ item_record( item ) for item in hammer.items.all() ],
        'shares': [] if not shares else [ share_record( share ) for share in hammer.shares.all() ],
    }
    return ret
    
def shared_hammer_record( share ):
	ret=hammer_record( share.hammer, shares=False )
	ret.update({
		'can_add': share.can_add,
		'can_remove': share.can_remove,
		'can_change': share.can_change,
		'theme': share.theme,
		'shared': True,
	})
	return ret
	
def item_record( item ):
    ret={
        'id': item.pk,
        'title': item.title,
        'status': item.status,
        'index': item.index,
    }
    return ret

def user_record( user ):
	ret={
		'name': user.username,
		'id': user.pk,
	}
	return ret
	
def current_user_record( user ):
	pref=UserPreference.objects.get_or_create( user=user )[0]
	ret=user_record( user )
	ret.update({
		'date_format': date_format( pref.date_format ),
		'military': pref.military,
	})
	return ret
	
def share_record( share ):
	ret={
		'id': share.pk,
		'sharee': share.sharee.username,
		'can_add': share.can_add,
		'can_change': share.can_change,
		'can_remove': share.can_remove,
		'can_share': share.can_share,
	}
	return ret

class LoginOrRegisterView( TemplateView ):
    template_name="login.html"
    success_url='/'
    def get_context_data( self, **kwargs ):
    	print 'get-ctx'
        ctx=super( LoginOrRegisterView, self ).get_context_data( **kwargs )
        ctx.update({
            'loginform': AuthenticationForm(),
            'registerform': UserCreationForm(),
        })
        return ctx
        
class LoginView(FormView):
	"""
	This is a class based version of django.contrib.auth.views.login.

	Usage:
		in urls.py:
			url(r'^login/$',
				LoginView.as_view(
					form_class=MyCustomAuthFormClass,
					success_url='/my/custom/success/url/),
				name="login"),

	"""
	form_class = AuthenticationForm
	redirect_field_name = REDIRECT_FIELD_NAME
	template_name = 'login.html'
	success_url='/'

	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, *args, **kwargs):
		return super(LoginView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		"""
		The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
		can log him in.
		"""
		login(self.request, form.get_user())
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		if self.success_url:
			redirect_to = self.success_url
		else:
			redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

		netloc = urlparse.urlparse(redirect_to)[1]
		if not redirect_to:
			redirect_to = settings.LOGIN_REDIRECT_URL
		# Security check -- don't allow redirection to a different host.
		elif netloc and netloc != self.request.get_host():
			redirect_to = settings.LOGIN_REDIRECT_URL
		return redirect_to

	def set_test_cookie(self):
		self.request.session.set_test_cookie()

	def check_and_delete_test_cookie(self):
		if self.request.session.test_cookie_worked():
			self.request.session.delete_test_cookie()
			return True
		return False

	def get(self, request, *args, **kwargs):
		"""
		Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
		"""
		self.set_test_cookie()
		return super(LoginView, self).get(request, *args, **kwargs)

	def get_context_data( self, **kwargs ):
		ctx=super( LoginView, self ).get_context_data( **kwargs )
		print "getcontextdasta"
		ctx.update({
			'registerform': UserCreationForm(),
		})
		print 'get ctx from login'
		return ctx
		
	def post(self, request, *args, **kwargs):
		"""
		Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
		"""
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			self.check_and_delete_test_cookie()
			return self.form_valid(form)
		else:
			self.set_test_cookie()
			return self.form_invalid(form)


class RegisterView( CreateView ):
	template_name="register.html"
	form_class=UserCreationForm
	success_url='/'
	
	def form_valid( self, form ):
		form.save()
		d=form.cleaned_data
		user=authenticate( username=d.get( 'username' ), password=d.get( 'password2' ) )
		login( self.request, user )
		return http.HttpResponseRedirect( '/' )

	
class AjaxMixin( object ):
    model=None
    ajax_only=False
    @method_decorator( csrf_exempt )
    def dispatch( self, request, *args, **kwargs ):
        if request.is_ajax():
            self.request, self.args, self.kwargs=request, args, kwargs
            self.user=request.user
            self.data=self.get_data()
            self.object=self.get_object()
            attrib= 'ajax_%s' % request.method.lower() 
            if hasattr( self, attrib ):
                return getattr( self, attrib )( request, *args, **kwargs )
            return dump( {"error": "Attribute on AjaxView not found - ( %s )" % attrib } )
        elif self.ajax_only:
        	return http.HttpResponseForbidden( "This url does not support landing" )
        return super( AjaxMixin, self ).dispatch( request, *args, **kwargs )
    
    def get_data( self ):
        if self.request.method.lower() in ( 'put', 'post', ):
            try:
                return json.loads( self.request.body )
            except:
                pass
        return self.request.REQUEST
    
    def get_object( self ):
        try:
            return self.model.objects.get( pk=self.kwargs.get( 'id', self.kwargs.get( 'pk') ) )
        except Exception, e:
            return None
		
class AjaxView( AjaxMixin, View ):
	pass
	

class HammerView( AjaxMixin, TemplateView ):
	template_name="hammer/2hammer.html"
	model=Hammer
	def get_context_data( self, **kwargs ):
		ctx=super( HammerView, self ).get_context_data( **kwargs )
		user=self.request.user
		js={}
		if user.is_authenticated():
			owned_hammers=Hammer.objects.filter( creator=user )
			shared=HammerShare.objects.filter( sharee=user )
			js={
				'user': current_user_record( user ),
				'hammers': [ hammer_record( hammer ) for hammer in owned_hammers ],
				'shared': [ shared_hammer_record( share ) for share in shared ],
			}
		ctx['json']=json.dumps(js)
		return ctx

	def ajax_delete( self, request, *args, **kwargs ):
		if self.object:
			if self.object.creator==self.user:
				hammer.delete() #deactivate instead of actually deleting??
				return dumpOK()
			return dumpError( "Not authorized to delete this hammer" )
		return dumpError( "Hammer not found  - DELETE" )
			
	def ajax_get( self, request, *args, **kwargs ):
		'''read a hammer'''
		if self.object:
			if self.object.creator==self.user: 
				return dump( hammer_record( self.object ) )
			elif self.user.shares.filter( hammer=self.object ).count():
				return dump( shared_hammer_record( self.object ) )
			return dumpError( 'Not Autorized' )

		return dumpError( "Hammer not found -- GET" )

	def ajax_put( self, request, *args, **kwargs ):
		'''save an existing hammer '''
		if self.object:
			if self.object.creator==self.user:
				form=HammerForm( data=self.data, instance=self.object )
				if form.is_valid():
					form.save()
					return dumpOK()
				return dumpFormErrors( form )
			return dumpError( "Not Autorized" )
		elif type( self.data ) is list:
			'''order change of items - data is a list of pks of items'''
			hammer=None
			for index, pk in enumerate( self.data ):
				item=HammerItem.objects.get( pk=pk )
				if hammer is None:
					hammer=item.hammer
					if( hammer.creator != self.user ) and ( not self.user.shares.filter( hammer=hammer, can_change=True ).count() ):
						return dumpError( "Not authorized to change this item" )
				item.index=index
				item.save()
			return dumpOK()
		return dumpError( "Hammer not found -- PUT" )
		
	def ajax_post( self, request, *args, **kwargs ):
		''' create a new hammer '''
		hammer=Hammer( creator=self.user )
		form=HammerForm( instance=hammer, data=self.data )
		if form.is_valid():
			form.save()
			hammer.data.create( user=self.user )
			return dumpOK( hammer_record( hammer ))
		return dumpFormErrors( form )

    
class HammerItemView( AjaxMixin, View ):
	model=HammerItem
	def ajax_get( self, request, *args, **kwargs ):
		'''read an item'''
		if self.object:
			if ( self.object.creator == self.user ) or ( self.user.shares.filter( hammer=self.object.hammer ).count() ):
				return dump( item_record( self.object ) )
			return dumpError( 'Not Authorized' )
		return dumpError( 'Item not found -- GET' )
	
	def ajax_delete( self, request, *args, **kwargs ):
		'''remove an item'''
		if self.object:
			hammer=self.object.hammer
			if ( hammer.creator==self.user ) or ( self.user.shares.filter( hammer=hammer, can_remove=True ).count() ):
				self.object.delete()
				return dumpOK()
			return dumpError( "Not authorized to remove items" )
		return dumpError( "Item not found --  DELETE" )
		
	def ajax_put( self, request, *args, **kwargs ):
		'''update an existing item'''
		item=self.object
		if item.hammer.creator != self.user:
			shares=HammerShare.objects.filter( hammer=item.hammer, sharee=self.user )
			if not ( shares.count() and shares[0].can_change ):
				return dumpError( "not authorized to update this item" )
		form=HammerItemForm( instance=item, data=self.data )
		if form.is_valid():
			form.save()
			return dump( item_record( item ) )
		return dumpFormErrors( form )
		
	def ajax_post( self, request, *args, **kwargs ):
		''' create a new item '''
		hpk=self.data.get( 'hammer' )
		if hpk:
			hammer=Hammer.objects.get( pk=hpk )
			if hammer.creator==self.user or self.user.shares.filter( hammer=hammer, can_add=True ).count():
				item=HammerItem( creator=self.user, hammer=hammer )
				form=HammerItemForm( data=self.data, instance=item )
				if form.is_valid():
					form.save()
					return dump( item_record( item ) )
				return dumpFormErrors( form )
			return dumpError( 'Not authorized to add items to this hammer' )
		return dumpError( 'No hammer found to add item to' )
		
		
		data, user=self.data, self.user
		hpk, pk, action=data.get('hammer'), data.get('id'), data.get('action')
		hammer, item, share=None, None, None
		
		if hpk:
			hammer=Hammer.objects.get( pk=hpk )
		elif pk:
			item=HammerItem.objects.get( pk=pk )
			hammer=item.hammer
		else:
			return dump({ 'error': 'No hammer or item found' })
			
		owner=hammer.creator==user
		if not owner:
			try:
				share=hammer.shares.get( sharee=user )
			except Exception, e:
				return dump({ 'error': 'Not authorized -  %s' % e })
		if action=='delete':
			if owner or share.can_remove:
				item.delete()
				return dumpOK()
			return dump({ 'error': 'Not authorized' })
		
		if not item:#CREATE
			if owner or share.can_add:
				item=HammerItem( hammer=hammer, creator=user )
			else:
				return dumpError('Not authorized to ADD items to a hammer')
		
		form=HammerItemForm( data=data, instance=item )
		if form.is_valid():
			form.save()
			return dump( item_record( item ) )
		return dumpFormErrors( form )
		
		if 'id' in data:
			try:
				hammer=Hammer.objects.get( pk=hpk )
			except:
				return dump({ 'error': 'Hammer not found id: %s' % hpk })
			
			owner=hammer.creator==user
			if not owner: #get the user share if it exists
				try:
					share=HammerShare.objects.get( hammer=hammer, sharee=user )
				except:
					return dump({ 'error': 'Not authorized to access this hammer' })
			add=owner or ( share and share.can_add )
			rem=owner or ( share and share.can_remove )
			chg=owner or ( share and share.can_change )
			if data['id']:# existing item
				item=hammer.items.get( pk=data['id'] )
				if action=='delete':
					if rem:
						item.delete()
						return dump({ 'success': True })
					return dump({ 'error': 'Not authorized to remove items' })
				if chg:
					form=HammerItemForm( instance=item, data=data )
				return dump({ 'error': 'Not authorized to change items' })
			elif add:
				item=HammerItem( hammer=hammer, creator=user )
				form=HammerItemForm( instance=item, data=data )
			if form.is_valid():
				form.save()
				return dump({ 'success': True })
			return dump({ 'error': '%s' % form.errors })
		return dump({ 'error': 'An id property is required to update stuff' })

class ShareView( AjaxMixin, View ):
	def ajax_post( self, request, *args, **kwargs ):
		''' all ajax share operations come through this view '''
		data=self.data
		hpk=data.get( 'hammer' )
		action=data.get( 'action' )
		share=None
		try:
			hammer=Hammer.objects.get( pk=hpk )
		except:
			return dump({ 'error': 'Hammer not found id: %s' % hpk })
		
		owner=hammer.creator==self.user
		if not owner:
			return dump({ 'error': 'Not authorized' })
			
		if 'id' in data:
			if not data[ 'id' ]:
				'''create a new default share if the user can be found'''
				username=data.get( 'sharee' )
				try:
					user=User.objects.get( username=username )
				except:
					try:
						user=User.objects.get( email=username )
					except:
						return dump({ 'error': 'Not found %s' % username })
				
				if HammerShare.objects.filter( sharee=user, hammer=hammer ).count():
					return dump({ 'error': 'exists' })
				share=HammerShare.objects.create( hammer=hammer, sharee=user )
				return dump( share_record( share ) )
			try:
				existing_share=hammer.shares.get( pk=data['id'])
			except:
				return dump({'error': 'share not found' })
				
			if action=='delete':
				existing_share.delete()
				return dump({'success': True })
			form=HammerShareForm( instance=existing_share, data=data )
			if form.is_valid():
				form.save()
				return dump({'success': True})
			return dump({'error': 'WTF ARE YOU DOING?' })
		return dump({ 'error': 'An id property is required when dealing with HammerShares'})

class HammerDataView( AjaxMixin, View ):
	''' deal with updating hammer data '''
	model=Hammer # we user Hammer as the model because data is attached to the hammer record as properties
	ajax_only=True
	def ajax_put( self, request, *args, **kwargs ):
		hammer=self.object



class CheckinView( AjaxMixin, View ):
	ajax_only=True
	
	def ajax_get( self, request, *args, **kwargs ):
		checkins=self.user.checkins.all()
		checkin=checkins[0] if checkins.count() else self.user.checkins.create()
		shared=self.user.shares.filter( hammer__revised__gte=checkin.checkin )
		ret=[]
		if shared.count():
			ret=[ shared_hammer_record( s ) for s in shared ]
		checkin.checkin=datetime.datetime.now()
		checkin.save()
		return dump( ret )
		


class UserPreferenceView( AjaxMixin, View ):
	ajax_only=True
	
	def ajax_post( self, request, *args, **kwargs ):
		''' update a users global settings '''
		pref=UserPreference.objects.get_or_create( user=self.user )[0]
		form=UserPreferenceForm( instance=pref, data=self.data )
		if form.is_valid():
			form.save()
			return dumpOK()
		return dumpFormErrors( form )
		
def dump( resp, status=200, content_type='application/json', dumps=True ):
	if dumps:
		resp=json.dumps( resp )
	return http.HttpResponse( resp, content_type=content_type, status=status )
	
def dumpOK( obj=None, success=True, status=200, content_type='application/json' ):
	d={ 'success': success }
	if obj is not None and type( obj ) == dict:
		d.update( obj )
	return dump( d, status=status, content_type=content_type )
	
def dumpError( obj, status=400, content_type='application/json' ):
	if type( obj ) != dict:
		obj={ 'error': obj }
	return dumpOK( obj, success=False, status=status, content_type=content_type )
	
def dumpFormErrors( form, obj=None, content_type='application/json',status=400 ):
	d=dict( form.errors )
	if obj is not None:
		d.update( obj )
	return dumpError( d, status=status, content_type=content_type )




