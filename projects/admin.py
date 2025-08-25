from django.contrib import admin
from .models import Project, ProjectDocument, ProjectKPISummary, ProjectFTESummary

admin.site.register(Project)
admin.site.register(ProjectKPISummary)
admin.site.register(ProjectFTESummary)

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ('project', 'document_name', 'document_link')