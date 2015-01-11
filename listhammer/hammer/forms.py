from django import forms

from .models import Hammer, HammerItem, HammerShare, HammerCheckin, UserPreference, HammerDataDefault, HammerData

class HammerForm( forms.ModelForm ):
    class Meta:
        model=Hammer
        fields=( 'name', )
        

class HammerItemForm( forms.ModelForm ):
    class Meta:
        model=HammerItem
        fields=('title', 'index','status' )
        
class HammerShareForm( forms.ModelForm ):
    class Meta:
        model=HammerShare
        fields=( 'can_add', 'can_remove', 'can_change',)
        
class UserPreferenceForm( forms.ModelForm ):
    class Meta:
        model=UserPreference
        fields=('date_format', 'military', )
        

class HammerDataForm( forms.ModelForm ):
    class Meta:
        model=HammerData
        exclude=( 'hammer', 'user', )
        
class HammerDataDefaultForm( forms.ModelForm ):
    class Meta:
        model=HammerDataDefault
        exclude=( 'hammer', 'user', )
                