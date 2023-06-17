from django.shortcuts import redirect

# class RedirectIfLoggedInMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     # def __call__(self, request):
#     #     if request.user.is_authenticated and request.path == '/register/':
#     #         return redirect('hotel:homepage') # change this to the URL you want to redirect to
#     #     response = self.get_response(request)
#     #     return response
