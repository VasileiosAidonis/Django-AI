from django import forms
from .models import Images


GROUP_AGE = (
    ('10-19','Under 19'),
    ('20-29', '20-29'),
    ('30-39','30-39'),
    ('40-49','40-49'),
    ('50-59','50-59'),
    ('60-69','60-69'),
    ('70','Over 70')
)

ANATOMIC_SITE = (
    ('lower_extremity', 'lower extremity'),
    ('upper_extremity', 'upper extremity'),
    ('head_neck', 'head / neck'),
    ('anterior_torso', 'anterior torso'),
    ('posterior_torso', 'posterior torso'),
    ('lateral_torso', 'lateral torso'),
    ('palms_soles', 'palms / soles'),
    ('oral_genital', 'oral / genital'),
    ('other', 'Other')
)

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
)

class ImageForm(forms.Form):
    image = forms.ImageField()
    gender = forms.CharField(widget=forms.Select(
        choices=GENDER))
    anatomic_site = forms.CharField(widget=forms.Select(
        choices=ANATOMIC_SITE))
    group_age = forms.CharField(widget=forms.Select(
        choices=GROUP_AGE))
