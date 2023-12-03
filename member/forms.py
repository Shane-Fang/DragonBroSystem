from django import forms
from .models import User



class RegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='密碼')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='確認密碼')
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='生日')

    class Meta:
        model = User
        fields = ['email', 'user_name', 'phone_number', 'birthday', 'address' ]
        # 根据需要调整字段的标签和其他属性

    def __init__(self, *args, **kwargs):
        super(RegisterModelForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = '密碼'
        self.fields['password2'].label = '確認密碼'
        # 如果需要其他字段的特殊处理，在这里添加
        self.order_fields(['email', 'password1', 'password2', 'user_name', 'phone_number', 'birthday', 'address' ])

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "兩次輸入的密碼不一致")

        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user