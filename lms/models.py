from django.db import models
from authentication.models import MyUser
from lms.ytd import ytapi,minsec
import itertools,random
from django.utils.text import slugify
from quiz.models import Quiz

# Create your models here.

class TimeStamp(models.Model):
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(MyUser,on_delete = models.CASCADE,null = True)

	class Meta:
		abstract = True

class Category(models.Model):
	category = models.CharField(max_length = 200)
	img380x256 = models.ImageField(upload_to = '',default = 'market.jpg')

	def __str__(self):
		return self.category

	def trending_courses(self):
		objects = [i for i in Course.objects.all()]
		random.shuffle(objects)
		return objects[:8]

class Project(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField()

	def __str__(self):
		return self.title

class Trainer(models.Model):
	name = models.CharField(max_length = 100)
	image = models.ImageField(upload_to = '',default = 'market.jpg')
	about = models.CharField(max_length = 200)
	description = models.TextField()
	linkedin = models.URLField()
	quora = models.URLField()

	def __str__(self):
		return self.name

class FAQ(models.Model):
	question = models.CharField(max_length = 300)
	answer = models.TextField()

	def __str__(self):
		return self.question


class Course(models.Model):
	title = models.CharField(max_length = 100)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	short_description = models.TextField()
	description = models.TextField()
	video_id = models.CharField(max_length = 20,default = 'bY6m6_IIN94',verbose_name = "Introduction Video ID")
	img1240x600 = models.ImageField(upload_to = '')
	img293x274 = models.ImageField(upload_to = '')
	duration = models.CharField(max_length = 10)
	credits = models.IntegerField()
	reviews = models.FloatField(verbose_name = 'rating')
	enrolled = models.IntegerField()
	slug = models.SlugField()
	offer_price = models.IntegerField()
	original_price = models.IntegerField()
	tags = models.TextField(verbose_name = 'Key Skills')
	trainer = models.ForeignKey(Trainer, on_delete = models.CASCADE)
	project = models.ManyToManyField(Project)
	faq = models.ManyToManyField(FAQ)


	def __str__(self):
		return self.title

	def get_tags(self):
		return self.tags.split(",")

	def lesson_count(self):
		lesson_list = [i.lesson_set.all().count() for i in Course.objects.get(id = self.id).module_set.all()]
		return list(itertools.accumulate(lesson_list))[-1]



class Module(models.Model):
	course = models.ForeignKey(Course,on_delete = models.CASCADE)
	module = models.CharField(max_length = 1000)
	pdf = models.FileField(upload_to = '',default = 'mozilla.pdf',blank = True,null = True)
	quiz = models.ForeignKey(Quiz,on_delete = models.CASCADE,blank = True,null = True)
	
	def __str__(self):
		return self.module

	def duration(self):
		obj = Module.objects.get(id = self.id)
		videos = [ytapi(i.video_id) for i in obj.lesson_set.all()]
		return minsec(list(itertools.accumulate(videos))[-1])


class Lesson(models.Model):
	module = models.ForeignKey(Module,on_delete = models.CASCADE)
	lesson = models.CharField(max_length = 1000)
	pdf = models.FileField(upload_to = '',default = 'mozilla.pdf',blank = True,null = True)
	video_id = models.CharField(max_length = 11)
	preview = models.BooleanField(default = False,verbose_name = "Show Preview")

	def __str__(self):
		return self.lesson

	def duration(self):
		return minsec(ytapi(self.video_id))

	def get_slug(self):
		return slugify(self.lesson,allow_unicode = True)

	def all_lessons(self):
		return Lesson.objects.all().count()


class CourseStatus(models.Model):
	course = models.ForeignKey(Course,on_delete = models.CASCADE)
	user = models.ForeignKey(MyUser,on_delete = models.CASCADE)
	completed_lessons = models.ManyToManyField(Lesson,related_name = 'completed_lessons',blank = True)
	current_lesson = models.ForeignKey(Lesson,on_delete = models.CASCADE, related_name = 'current_lesson',blank = True,null = True)

	class Meta:
		verbose_name_plural = "Course Status"


class Question(TimeStamp):
	question = models.TextField()
	course = models.ForeignKey(Course,on_delete = models.CASCADE)

	def __str__(self):
		return self.question

class Answer(TimeStamp):
	question = models.ForeignKey(Question,on_delete = models.CASCADE,related_name = "answers")
	answer = models.TextField()

	def __str__(self):
		return self.answer






