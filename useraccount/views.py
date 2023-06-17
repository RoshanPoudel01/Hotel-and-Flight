from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from useraccount.forms import UserSignupForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


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

    return render(
        request,
        "profile.html",
        {"users": user},
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

    return render(request, "profile_edit.html", {"user": userss})
