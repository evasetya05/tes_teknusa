from django.db import models
from django.urls import reverse

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
    ('archived', 'Archived'),
]

class Idea(TimestampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assumptions = models.TextField(blank=True, help_text='Key assumptions to validate')
    priority = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lean:idea_detail', args=[self.pk])

class Build(TimestampedModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='builds')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return f"Build: {self.title}"

class Product(TimestampedModel):
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Measure(TimestampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='measures')
    metric = models.CharField(max_length=200)
    target = models.FloatField(null=True, blank=True)
    current = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.metric} — {self.product.name}"

class DataPoint(TimestampedModel):
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE, related_name='datapoints')
    value = models.FloatField()
    measured_at = models.DateTimeField()
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-measured_at']

    def __str__(self):
        return f"{self.value} @ {self.measured_at.date()}"

class Learning(TimestampedModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='learnings', null=True, blank=True)
    summary = models.TextField()
    action = models.TextField(blank=True, help_text='Next steps or experiments')

    def __str__(self):
        return (self.summary[:60] + '...') if len(self.summary) > 60 else self.summary