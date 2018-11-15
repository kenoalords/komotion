from django import forms
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from academy.models import Category, Software, Rank, Course, Author, CourseFile, RankDescription

class CourseForm(forms.ModelForm):

    title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'Enter course title...', 'required': True }))
    description = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'textarea', 'placeholder': 'Enter a brief description about this course...', 'rows': 5, 'required': True }))
    image = forms.ImageField()
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    software = forms.ModelMultipleChoiceField(queryset=Software.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    rank = forms.ModelMultipleChoiceField(queryset=Rank.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)

    class Meta:
        model = Course
        fields = ('title', 'description', 'image', 'authors', 'category', 'software', 'rank',)

class CourseFileForm(forms.ModelForm):
    title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'Enter course file title...', }))
    track_no = forms.CharField(max_length=64, widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'e.g 01', }))
    description = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'textarea', 'placeholder': 'Enter a brief description...', 'rows': 2, }))
    image = forms.ImageField(required=False)
    file = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'textarea', 'placeholder': 'Copy and paste vimeo embed code', 'rows': 2, }))
    duration = forms.CharField(max_length=24, widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'e.g 05:45', }))
    class Meta:
        model = CourseFile
        fields = ('track_no', 'title', 'description', 'image', 'file', 'duration',)

CourseFileFormset = inlineformset_factory(parent_model=Course, model=CourseFile, form=CourseFileForm, extra=1)


class RankForm(forms.ModelForm):
    title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'Title', }))
    cost = forms.CharField(max_length=128, widget=forms.NumberInput(attrs={ 'class': 'input', 'placeholder': 'Cost', }))
    description = forms.CharField(max_length=256, widget=forms.Textarea(attrs={ 'class': 'textarea', 'placeholder': 'Description', 'rows': 2 }), required=False)
    class Meta:
        model = Rank
        fields = ('title', 'description', 'image', 'cost',)

class RankDescriptionForm(forms.ModelForm):
    class Meta:
        model = RankDescription
        fields = ('title', 'description',)

class SubscriptionForm(forms.Form):
    DURATION_CHOICES = (
        (1, 'Monthly'),
        (6, 'Bi-anually'),
        (12, 'Yearly'),
    )
    rank = forms.ModelChoiceField(queryset=Rank.objects.all())
    duration = forms.CharField( widget=forms.Select(choices=DURATION_CHOICES) )
