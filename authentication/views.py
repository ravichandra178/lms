from django.shortcuts import render,reverse
from authentication.models import MyUser
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def profile(request):
	return render(request,'profile.html')

class ProfileUpdate(UserPassesTestMixin, UpdateView):
	model = MyUser
	fields = ['first_name','last_name','college','branch','display_pic']
	template_name = 'updateprofile.html'
	success_url = '/accounts/profile/'

	def test_func(self):
		return self.request.user.slug == self.kwargs['slug']