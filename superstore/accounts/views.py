from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, get_user_model, login
from django.views import generic as views

from superstore.accounts.forms import UserCreateForm
# Create your views here.
UserModel = get_user_model()


class SignUpView(views.CreateView):
    model = UserModel
    template_name = 'accounts/register-page.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    #login directly after register
    #def post(self, request, *args, **kwargs):
        #response = super().post(request, *args, **kwargs)
        #login(request, self.object)
        #print(self.object)
        #return response


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        toys = self.object.toy_set.prefetch_related('like_set')

        context['is_owner'] = self.request.user == self.object
        context['toys_count'] = self.object.toy_set.count()
        context['likes_count'] = sum(x.like_set.count() for x in toys)
        context['toys'] = self.object.toy_set.all()
        context['userModel'] = UserModel

        return context


class UserEditView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'gender', 'email', 'profile_picture')

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={
            'pk': self.request.user.pk,
        })


class UserDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('index')

