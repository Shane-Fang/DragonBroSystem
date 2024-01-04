from django import forms
from .models import User,Address
from django.contrib.auth.forms import SetPasswordForm
from django.forms import inlineformset_factory

AddressFormSet = inlineformset_factory(
    User, 
    Address, 
    fields=('address',), 
    extra=1, 
    can_delete=True
)

class UserUpdateForm(forms.ModelForm):
    change_password = forms.BooleanField(required=False, label='更改密碼')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='新密碼', required=False)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(), label='新密碼確認', required=False)
    id = forms.IntegerField(disabled=True, required=False, label='ID')  # 只读 ID 字段
    bonus_points = forms.IntegerField(disabled=True, required=False, label='積分')  # 只读积分字段
    class Meta:
        model = User
        fields = ['user_name', 'phone_number', 'birthday',  'bonus_points', 'id']
        # 可以排除 change_password, new_password 和 new_password_confirm，因为它们不是模型的一部分

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['id'].initial = self.instance.id  # 设置 id 初始值
        self.fields['bonus_points'].initial = self.instance.bonus_points  # 设置 bonus_points 初始值

        # 调整字段的顺序
        order = ['id', 'user_name', 'phone_number', 'birthday', 'bonus_points', 'change_password', 'new_password', 'new_password_confirm']
        self.order_fields(order)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password")
        password2 = cleaned_data.get("new_password_confirm")

        if password1 and password2 and password1 != password2:
            self.add_error('new_password_confirm', "兩次輸入的密碼不一致")

        return cleaned_data

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if self.cleaned_data['change_password']:
            user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user


class RegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='密碼')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='確認密碼')
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='生日')

    class Meta:
        model = User
        fields = ['phone_number', 'user_name', 'phone_number', 'birthday']
        # 根据需要调整字段的标签和其他属性

    def __init__(self, *args, **kwargs):
        super(RegisterModelForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = '密碼'
        self.fields['password2'].label = '確認密碼'
        # 如果需要其他字段的特殊处理，在这里添加
        self.order_fields(['phone_number', 'password1', 'password2', 'user_name',  'birthday' ])

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
    
class RegisterAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']