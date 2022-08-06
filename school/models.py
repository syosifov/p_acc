# https://github.com/PrettyPrinted/youtube_video_code/tree/master/2020/05/16/Adding%20Extra%20Fields%20On%20Many-To-Many%20Relationships%20in%20Django/many_to_many_extra

from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=30)
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    final_grade = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        unique_together = [['student', 'course']]
