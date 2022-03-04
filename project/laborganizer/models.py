"""Models relating to Lab Organizers."""
from django.db import models
from datetime import datetime, date
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
        return self.semester_time + str(self.year)

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

    year = models.IntegerField('Calendar year', choices=YEARS)
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

    def set_days(self, days_list):
        """Convert a list of days into a string delimited by ' ' character."""
        self.days = ' '.join(days_list)
        self.save()

    def get_start_time(self):
        """Convert the stored start time fo a lab."""
        return str(self.start_time)

    def get_end_time(self):
        """Convert the stored end time fo a lab."""
        return str(self.end_time)

    #TODO This must switch via the template schedule, instead of directly switching via the database
    def confirm_switch(self, other_lab, TA1, TA2):
        self.assigned_ta = None
        other_lab.assigned_ta = None
        self.save()
        other_lab.save()
        self.assigned_ta = TA2
        other_lab.assigned_ta = TA1
        self.save()
        other_lab.save()

    class_name = models.CharField("Class name", default="N/A", max_length=50)
    subject = models.CharField("Subject", max_length=10)
    catalog_id = models.CharField("Catalog ID", max_length=10)
    course_id = models.CharField("Course ID", max_length=10, blank=True, unique=True)
    section = models.CharField("Section", max_length=10, blank=True)
    days = models.CharField("Days", max_length=10)
    facility_id = models.CharField("Facility ID", max_length=20, blank=True)
    facility_building = models.CharField("Facility Building", max_length=50,
                                         blank=True)
    instructor = models.CharField("Instructor", max_length=50, blank=True)
    start_time = models.TimeField("Start Time", auto_now=False,
                                  auto_now_add=False, blank=True, null=True)
    end_time = models.TimeField("End Time", auto_now=False,
                                auto_now_add=False, blank=True, null=True)
    staffed = models.BooleanField(default=False)

    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        verbose_name='Semester',
        null=True,
        blank=True
    )


class AllowTAEdit(models.Model):
    """
    Boolean flag for TA information edits.

    Acts as a variable that is checked every time a TA tries to edit their
    own information.
    """

    class Meta:
        """Meta information for TA edit object."""

        verbose_name = 'Allow TA Edit'
        verbose_name_plural = 'Allow TA Edits'

    def __str__(self):
        """Human readable object name."""
        return 'Allowance'

    def is_allowed(self):
        """Check if the current time is after the currently saved time."""
        # get current datetime information
        day_and_time = datetime.now()

        # format current datetime information
        day = day_and_time.strftime('%m/%d/%Y')
        time = day_and_time.strftime('%H:%M')

        # format saved datetime information
        saved_day = self.date.strftime('%m/%d/%Y')
        saved_time = self.time.strftime('%H:%M')

        # if the current time is before the saved time, allow
        # TA's to edit their information
        if day < saved_day or time < saved_time:
            self.allowed = True
            return True
        else:
            # if the saved time is after the current time, do not
            # allow TA's to edit their information
            self.allowed = False
            return False

    allowed = models.BooleanField('Allow TA\'s to edit', default=False)
    date = models.DateField(auto_now=False, auto_now_add=False,
                            blank=True, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False,
                            blank=True, null=True)


class History(models.Model):
    ta_1 = models.ManyToManyField(TA, blank=True, related_name='ta_1')
    ta_2 = models.ManyToManyField(TA, blank=True, related_name='ta_2')
    lab_1 = models.ManyToManyField(Lab, blank=True, related_name='lab_1')
    lab_2 = models.ManyToManyField(Lab, blank=True, related_name='lab_2')

    def undo_bilateral_switch(self):
        self.lab_1.first().confirm_switch(self.lab_2.first(), self.ta_1.first(), self.ta_2.first())
