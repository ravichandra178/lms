from django import template
from lms.models import CourseStatus,Module
register = template.Library()

@register.simple_tag
def user_enrolled(user,course):
	return CourseStatus.objects.filter(user = user).filter(course = course).exists()

@register.simple_tag
def lessons_completed(user,module_id):
	status = CourseStatus.objects.get(user = user)
	module = Module.objects.get(id = module_id)
	return len([i for i in status.completed_lessons.all() if i in module.lesson_set.all()])

@register.simple_tag
def viewed(user,module_id):
	status = CourseStatus.objects.get(user = user)
	module = Module.objects.get(id = module_id)
	return [i.lesson for i in status.completed_lessons.all() if i in module.lesson_set.all()]
