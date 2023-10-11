from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from useraccount.forms import UserSignupForm, UserEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages 

import stripe
stripe.api_key = "sk_test_51N2DKlBDe5c2rfDAZlaYAUJWD6ORem7RLEZFoDAZcKyPx55mSltZ2L2KrgeHboSO7hr7pSzcO1OpvGVhdosoeEDW00VrQx4XTO"


# Create your views here.

User = get_user_model()


class UserLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("hotel:homepage")


class SignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = "register.html"
    success_url = reverse_lazy("hotel:homepage")
    # def get(self,request):
    #     if request.user.is_authenticated:
    #         print(request.user)
    #         return HttpResponseRedirect( reverse(
    #             "hotel:homepage")
    #         )
        # else:
        #     return render(request,"register.html")
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)
   
           


@login_required
def user_profile(request, user, id):
    user = get_object_or_404(User, username=user, id=id)
    userss = UserEditForm(request.POST or None, request.FILES or None, instance=user)

    return render(
        request,
        "profile.html",
        {"users": user, "userprofile": userss,},
    )


@login_required
def user_profile_edit(request, id):
    user = get_object_or_404(User, id=id, username=request.user)
    userss = UserEditForm(request.POST or None, request.FILES or None, instance=user)
    if userss.is_valid():
        userss.save()

        return HttpResponseRedirect(
            reverse(
                "user:userprofile",
                args=(
                    user.username,
                    user.id,
                ),
            )
        )

    return render(request, "profile_edit.html", {"userprofile": userss})
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            # return redirect('user:userprofile')
            return HttpResponseRedirect(
            reverse(
                "user:userprofile",
                args=(
                    user.username,
                    user.id,
                ),
            )
        )
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })
# @login_required
# def password_change(request,id):
#     user=get_object_or_404(User,id=id,username=request.user)
#     userform=PasswordChangeForm(request.POST or None,request.FILES or None)
#     if userform.is_valid():
#         userform.save()
#         return HttpResponseRedirect(
#             reverse(
#                 "user:userprofile",
#                 args=(
#                     user.username,
#                     user.id,
#                 ),
#             )
#         )

#     return render(request, "changepassword.html", {"userprofile": userform})



def makeclientpage(request):
    return render(request, "become_client.html")

@login_required
def make_client(request):
    user=User.objects.get(id=request.user.id)
    if user.stripe_customer_id is None:
        acount=stripe.Account.create(type="express")
        user.stripe_customer_id=acount.id
        user.is_client=True
        user.save()
    else:
        acount = stripe.Account.retrieve(user.stripe_customer_id)

    account_link=stripe.AccountLink.create(
        account=acount.id,
        refresh_url="https://www.google.com/",
        return_url=settings.REDIRECT_DOMAIN,
        type="account_onboarding",
        )
    return render(request, "become_client.html", {"account_link_url": account_link.url, "user": user})