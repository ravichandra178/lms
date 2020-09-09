from django.shortcuts import render,reverse
from lms.models import Course,Module,Lesson,CourseStatus,Category,Question,Answer
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect,JsonResponse
from django.views.generic.edit import FormMixin
from lms.forms import QuestionForm,AnswerForm
import time
from codetiming import Timer

# Create your views here.

def index(request):
	category = Category.objects.all()
	return render(request,'index.html',{'category':category})

def about(request):
	return render(request,'about-us.html')

def qna(request,slug):
	course = Course.objects.get(slug = slug)
	course_id = course.id
	course_title = course.title
	course_slug = course.slug
	questions = Question.objects.filter(course_id = course_id)
	return render(request,'qna.html',{'questions':questions,'course':course_slug,'course_title':course_title,'aform':AnswerForm()})

class CourseDetail(DetailView):
	model = Course
	template_name = 'course.html'

def blog(request):
	return render(request,'blog.html')

def contact(request):
	return render(request,'contact.html')

def event(request):
	return render(request,'event.html')

def allcourses(request):

	return render(request,'all-courses.html')

def mycourses(request):
	mycourses = CourseStatus.objects.filter(user = request.user)
	return render(request,'mycourses.html',{'mycourses':mycourses})

def cart(request):
	return render(request,'cart.html')

def checkout(request,slug):
    return render(request,'checkout.html')

def answer(request,slug,pk):
	if request.method == 'POST':
		answer = request.POST.get('answer')
		obj = Answer(question_id = pk,answer = answer,user = request.user)
		obj.save()
	return HttpResponseRedirect(reverse('lms:qna', kwargs = {'slug':slug}))


class detail(FormMixin, DetailView):
	model = Course
	template_name = 'purchased-course.html'
	form_class = QuestionForm

	def get_success_url(self):
		return reverse('lms:detail', kwargs={'slug': self.object.slug})

	def get_context_data(self, **kwargs):
		context = super(detail, self).get_context_data(**kwargs)
		is_enrolled = self.request.user.is_authenticated and CourseStatus.objects.filter(user = self.request.user).filter(course = kwargs['object']).exists()
		if is_enrolled:
			user_course_it = CourseStatus.objects.filter(user = self.request.user).filter(course = kwargs['object'])
			user_course = CourseStatus.objects.get(id = [i.id for i in user_course_it][0])
			context['form'] = QuestionForm()
			context['aform'] = AnswerForm()
			context['questions'] = Question.objects.filter(course = kwargs['object'])

		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		course = Course.objects.get(slug = kwargs['slug'])
		form = self.get_form()
		question = request.POST.get('question')
		if form.is_valid():
			form.instance.user = self.request.user
			form.instance.course = course
			form.instance.question = question
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		form.save()
		return super(detail, self).form_valid(form)

def onended(request):
	if request.is_ajax():
		iframe_id = request.GET.get('iframe_id')
		status = CourseStatus.objects.get(user = request.user)
		current_lesson = Lesson.objects.get(video_id = iframe_id)
		status.current_lesson = current_lesson
		status.completed_lessons.add(current_lesson)
		count = len([i for i in status.completed_lessons.all() if i in current_lesson.module.lesson_set.all()])
		data = {'count':count,'module':current_lesson.module.id,'lesson':current_lesson.id}
	return JsonResponse(data)

def enrol(request):
	if request.is_ajax():
		username = request.GET.get('username')[0]
		data = request.GET.get('status')
		#print(data)
		r = data.split(':')
		slug = r[0]
		payment_id = r[1]
		enrol,created = CourseStatus.objects.get_or_create(user_id = request.user.id,course_id = Course.objects.get(slug = slug).id)
		data = {'slug':slug,'created':created}
		return JsonResponse(data)

def navbar(request):
   return {'category':Category.objects.all()}

def timer(request):
	if request.is_ajax():
		hour = request.GET.get('hour')
		minute = request.GET.get('minute')
		seconds = request.GET.get('seconds')
		total_seconds = ((hour*60)+minute)*60 + seconds
		t = Timer(name = request.user)
		t.start()
		time.sleep(1)
		t.stop()
		elapsed_time = t.stop()
		return


