from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        print('user.phone_number1:')
        user = super().save_user(request, sociallogin, form)
        
        extra_data = sociallogin.account.extra_data
        user_name = extra_data.get('name')
        email = extra_data.get('email')
        line_token = extra_data.get('sub')
        print('user_name:', user_name)
        print('email:', email)
        print('line_token:', line_token)

        if user_name:
            user.user_name = user_name

        if line_token:
            user.line_token = line_token
            
        user.save()
            
        if not user.phone_number:
            request.session['socialaccount_sociallogin'] = sociallogin.serialize()
            return redirect('enter_phone_number')

        return user