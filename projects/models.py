from django.db import models

class Project(models.Model):
    month = models.CharField(max_length=20)
    mydc_ref = models.IntegerField(null=False, blank=False)
    otp = models.CharField(max_length=50)
    project = models.CharField(max_length=100)
    customer = models.CharField(max_length=100, blank=True, null=True)
    business_unit = models.CharField(max_length=100, blank=True, null=True)
    global_iqp = models.CharField(max_length=100, blank=True, null=True)
    bo_pm = models.CharField(max_length=100)
    bo_pl2 = models.CharField(max_length=100)
    bo_acqp_maturity = models.CharField(max_length=100)
    bo_acqp_assessment_date = models.DateField(null=True, blank=True)

    planned_deliverables = models.IntegerField()
    otd = models.IntegerField()
    otd_target = models.FloatField()
    actual_otd_percent = models.FloatField()

    right_first_time = models.IntegerField()
    rft_target = models.FloatField()
    actual_rft_percent = models.FloatField()

    skill_compliance = models.FloatField()

    csat_level = models.IntegerField()
    csat_date = models.DateField(null=True, blank=True)

    csat_service_mgmt = models.IntegerField()
    csat_quality = models.IntegerField()
    csat_autonomy = models.IntegerField()
    csat_communication = models.IntegerField()
    csat_flexibility = models.IntegerField()
    csat_proactivity = models.IntegerField()

    fte_count = models.FloatField()
    attrition = models.IntegerField()
    replaced_fte = models.IntegerField()

    real_capacity_hours = models.FloatField()
    time_sold_hours = models.FloatField()
    turnover_engaged = models.FloatField()
    cumulative_turnover_engaged = models.FloatField()

    po_received = models.FloatField()
    cumulative_po_received = models.FloatField()

    current_dan = models.FloatField()
    cumulative_dan = models.FloatField()

    std_target_margin = models.FloatField()
    std_forecasted_margin = models.FloatField()

    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.month} - {self.project}"
    

class ProjectDocument(models.Model):
    DOCUMENT_CHOICES = [
        ('PMP', 'PMP'),
        ('Skill Matrix', 'Skill Matrix'),
        ('SLA', 'SLA'),
        ('Turtle Chart', 'Turtle Chart'),
        ('Other', 'Other'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=50, choices=DOCUMENT_CHOICES)
    document_link = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.project.project} - {self.document_name}"

class ProjectKPISummary(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='kpi_summaries')
    metric = models.CharField(max_length=100)
    h1 = models.FloatField()
    target_h = models.FloatField()
    htd = models.FloatField()

    def __str__(self):
        return f"{self.metric} - {self.project.project}"
    
class ProjectFTESummary(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="fte_summaries")
    fte = models.IntegerField()
    iqp1 = models.IntegerField()
    iqp2 = models.IntegerField()
    iqp3 = models.IntegerField()
    iqp4 = models.IntegerField()
    iqp5 = models.IntegerField()

    def __str__(self):
        return f"FTE Summary for {self.project.project} (FTE: {self.fte})"