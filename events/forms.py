from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), 
                              label="Leave a Comment",
                              required=True)
    event = forms.DecimalField()

class ImageForm(forms.Form):
    image = forms.ImageField()
    event = forms.DecimalField()
