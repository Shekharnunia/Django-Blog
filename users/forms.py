from django import forms

from .models import User

STATUS = [
    ('is_teacher', 'teacher'),
    ('is_student', 'student'),
]


class SignupForm(forms.Form):
    status = forms.CharField(label='What is your status?', widget=forms.Select(choices=STATUS))

    def signup(self, request, user):
        if self.cleaned_data['status'] == 'is_teacher':
            user.is_teacher = True
        if self.cleaned_data['status'] == 'is_student':
            user.is_student = True
        user.save()


class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'required': True}),
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'picture', ]
