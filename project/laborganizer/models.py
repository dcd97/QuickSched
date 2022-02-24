"""Models relating to Lab Organizers."""
from django.db import models
from datetime import date
from teachingassistant.models import TA


class Semester(models.Model):
    """
    Semester Object. Primary key is predefined as an integer by Django.

    One Semester contains many labs.
    """

    class Meta:
        """Metadata regarding a Semester."""

        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def __str__(self):
        """Human readable class name, for admin site."""
        return self.semester_time + self.year

    TIMES = (
        ('SPR', 'Spring'),
        ('SUM', 'Summer'),
        ('FAL', 'Fall'),
        ('WNT', 'Winter')
    )

    def get_10_years():
        """
        Generate a list of tuples of 10 years.

        Beginning with the current year, assign keys and values.
        Note that keys/values are the same, allowing the list to
        remain dynamic.
        """
        year = date.today().year
        years = [(year, year)]
        for index in range(10):
            year += 1
            years.append((year, year))
        return years

    YEARS = get_10_years()

    year = models.CharField('Calendar year', max_length=5, choices=YEARS)
    semester_time = models.CharField('Time held', max_length=3, choices=TIMES)


class Lab(models.Model):
    """Lab Object related to a single semester."""

    class Meta:
        """Metadata regarding a Lab Object."""

        verbose_name = 'Lab'
        verbose_name_plural = 'Labs'

    def __str__(self):
        """Human readable class name, for admin site."""
        return self.subject + self.catalog_id + ' : ' + self.class_name

    def get_days(self):
        """Convert 'days' field into a readable list."""
        split_days = self.days.split(' ')
        return ', '.join(split_days)

    class_name = models.CharField("Class name", default="N/A", max_length=50)
    subject = models.CharField("Subject", max_length=10)
    catalog_id = models.CharField("Catalog ID", max_length=10)
    course_id = models.CharField("Course ID", max_length=10, blank=True)
    section = models.CharField("Section", max_length=10, blank=True)
    days = models.CharField("Days", max_length=10)
    facility_id = models.CharField("Facility ID", max_length=20, blank=True)
    facility_building = models.CharField("Facility Building", max_length=50,
                                         blank=True)
    instructor = models.CharField("Instructor", max_length=50, blank=True)
    start_time = models.CharField("Start time", max_length=50, blank=True)
    end_time = models.CharField("End time", max_length=50, blank=True)
    staffed = models.BooleanField(default=False)

    # assigned_ta = models.OneToOneField(TA, on_delete=models.DO_NOTHING,
    #                                   null=True, blank=True)

    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        verbose_name='Semester',
        null=True,
        blank=True
    )
