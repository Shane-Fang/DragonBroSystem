from django import forms
from .models import Restock
from member.models import Branchs
# class RestockForm(forms.ModelForm):
#     object_id = forms.ModelChoiceField(queryset=Branchs.objects.all(), required=False, label='分店/訂單的ID')

#     class Meta:
#         model = Restock
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(RestockForm, self).__init__(*args, **kwargs)
#         self.fields['object_id'].queryset = Branchs.objects.all()

    # def save(self, commit=True):
    #     print(111)
    #     instance = super(RestockForm, self).save(commit=False)
    #     if self.cleaned_data['object_id']:
    #         instance.object_id = self.cleaned_data['object_id']  # 不使用 .id
    #     else:
    #         instance.object_id = None
    #     if commit:
    #         instance.save()
    #     return instance
class RestockForm(forms.ModelForm):
    object_id = forms.ModelChoiceField(queryset=Branchs.objects.none(), required=False, label='分店/訂單的ID')
    class Meta:
        model = Restock
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(RestockForm, self).__init__(*args, **kwargs)
        # 如果是编辑表单并且Category为'BtoB'，则更新object_id字段的查询集
        if self.instance.pk and self.instance.Category == 1:  # 假设 1 代表 'BtoB'
            self.fields['object_id'].queryset = Branchs.objects.all()
        else:
        # 对于新记录，您可以设置一个默认的查询集
            self.fields['object_id'].queryset = Branchs.objects.all()  # 或者根据需要选择一个不同的查询集
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('Category')
        object_id_field = self.fields['object_id']
    
        # 根据Category动态设置object_id字段的查询集
        if category == 1:  # 假设 1 代表 'BtoB'
            object_id_field.queryset = Branchs.objects.all()
        else:
            object_id_field.queryset = Branchs.objects.none()
    
        # 确保 object_id 是整数
        object_id_instance = cleaned_data.get('object_id')
        if object_id_instance:
            cleaned_data['object_id'] = object_id_instance.id
        return cleaned_data


# member | 店家