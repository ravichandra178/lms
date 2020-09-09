from django.contrib import admin

# Register your models here.
from lms.models import Course,Module,Lesson,CourseStatus,Category,Project,Trainer,FAQ,Question,Answer

import nested_admin


class LessonInline(nested_admin.NestedStackedInline):
    model = Lesson

class ModuleInline(nested_admin.NestedStackedInline):
    model = Module
    inlines = [LessonInline]

class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [ModuleInline]

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Trainer)
admin.site.register(FAQ)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CourseStatus)

admin.site.register(Course, CourseAdmin)
