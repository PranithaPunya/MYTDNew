from rest_framework import serializers
from .models import Project, ProjectDocument, ProjectKPISummary, ProjectFTESummary
from datetime import datetime

class ProjectOverviewSerializer(serializers.Serializer):
    ref = serializers.CharField(source="mydc_ref")
    Project = serializers.CharField(source="project")
    IQP = serializers.CharField(source="business_unit", default="--")
    BU = serializers.CharField(source="otp", default="--")
    Customer = serializers.CharField(source="customer", default="--")
    OTD = serializers.SerializerMethodField()
    RFT = serializers.SerializerMethodField()
    Skill_Compliance = serializers.SerializerMethodField()
    Subskill = serializers.SerializerMethodField()
    ACQP = serializers.CharField(source="bo_acqp_maturity", default="--")
    CSAT = serializers.SerializerMethodField()
    Gross_Margin = serializers.SerializerMethodField()
    BO_PM = serializers.CharField(source="bo_pm", default="--")
    BO_PL2 = serializers.CharField(source="bo_pl2", default="--")
    DC = serializers.SerializerMethodField()
    Business_Manager = serializers.SerializerMethodField()
    DC_Manager = serializers.SerializerMethodField()
    Division_Director = serializers.SerializerMethodField()
    Project_Director = serializers.SerializerMethodField()
    DC_Head = serializers.SerializerMethodField()
    PD = serializers.SerializerMethodField()
    Remark = serializers.CharField(source="remark", default="--")

    excludedFieldsFromTable = serializers.SerializerMethodField()
    infoRightKey = serializers.SerializerMethodField()
    infoLeftKey = serializers.SerializerMethodField()

    def get_OTD(self, obj):
        up = obj.otd or 0
        down = obj.planned_deliverables or 0
        diff = up - down
        sign = "+" if diff >= 0 else "-"
        return f"{up} | {down} | {sign}{abs(diff)}"

    def get_RFT(self, obj):
        return f"{obj.actual_rft_percent:.0f}%" if obj.actual_rft_percent else "--"

    def get_Skill_Compliance(self, obj):
        return f"{obj.skill_compliance:.2f}%" if obj.skill_compliance else "--"

    def get_Subskill(self, obj):
        return "--"

    def get_CSAT(self, obj):
        return str(obj.csat_level) if obj.csat_level else "--"

    def get_Gross_Margin(self, obj):
        return "24%"  # Replace with real logic if needed

    def get_DC(self, obj):
        return "0"

    def get_Business_Manager(self, obj):
        return "Steffen HILLENMEIER"

    def get_DC_Manager(self, obj):
        return "Arjun SUBRAYA"

    def get_Division_Director(self, obj):
        return "--"

    def get_Project_Director(self, obj):
        return obj.bo_pm

    def get_DC_Head(self, obj):
        return "Pradeep PATIL"

    def get_PD(self, obj):
        return "VMA"

    def get_excludedFieldsFromTable(self, obj):
        return [
            "infoRightKey", "DC_Head", "Remark", "Project_Director", "Competency_Head",
            "COC_Manager", "Business_Manager", "excludedFieldsFromTable",
            "infoLeftKey", "PD", "Division_Director", "DC_Manager"
        ]

    def get_infoRightKey(self, obj):
        return [
            "Division_Director", "Project_Director", "DC_Head",
            "DC_Manager", "BO_PM", "BO_PL2", "Business_Manager"
        ]

    def get_infoLeftKey(self, obj):
        return ["ref", "Project", "Customer"]



class GraphDatasetSerializer(serializers.Serializer):
    label = serializers.CharField()
    data = serializers.ListField(child=serializers.FloatField())
    backgroundColor = serializers.CharField()
    type = serializers.CharField(default="bar")
    order = serializers.IntegerField(required=False)
    yAxisID = serializers.CharField(required=False)
    borderColor = serializers.CharField(required=False)
    borderWidth = serializers.IntegerField(required=False)


class GraphDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    order = serializers.IntegerField()
    showlabel = serializers.BooleanField()
    data = serializers.DictField()
    options = serializers.DictField()

class ProjectDocumentInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['document_name', 'document_link']

class ProjectKPISummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectKPISummary
        fields = ['id', 'project', 'metric', 'h1', 'target_h', 'htd']

class ProjectFTESummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFTESummary
        fields = [
            'id',
            'project',
            'fte',
            'iqp1',
            'iqp2',
            'iqp3',
            'iqp4',
            'iqp5',
        ]

class ProjectDetailSerializer(serializers.Serializer):
    ref_id = serializers.CharField(source="mydc_ref")
    Customer = serializers.CharField(source="customer")
    Project = serializers.CharField(source="project")
    ProjectData = serializers.SerializerMethodField()
    Remark = serializers.SerializerMethodField()
    GraphData = serializers.SerializerMethodField()
    Documents = serializers.SerializerMethodField()
    KPIData = serializers.SerializerMethodField()
    FTESummary = serializers.SerializerMethodField()

    def get_ProjectData(self, obj):
        return [
            {
                "title": "Project: ",
                "subTitle": obj.project,
                "infoText": "",
                "bgVariant": "yellow",
                "showIconOnSubTitle": False,
                "showBottomText": False,
            },
            {
                "title": "Customer:",
                "subTitle": obj.customer or "-",
                "infoText": "",
                "bgVariant": "red",
                "showIconOnSubTitle": False,
                "showBottomText": False,
            },
            {
                "title": "DC Entity:",
                "subTitle": "- Alten IN",
                "infoText": "",
                "bgVariant": "orange",
                "showIconOnSubTitle": True,
                "showBottomText": False,
            },
            {
                "title": "People staffed/ordered today",
                "subTitle": f"{int(obj.fte_count)}/7",
                "infoText": "",
                "bgVariant": "blue",
                "showIconOnSubTitle": False,
                "showBottomText": True,
            },
        ]

    def get_Remark(self, obj):
        return [
            {
                "id": 1,
                "author": "NA",
                "content": obj.remark or "No remarks",
                "date": obj.csat_date.strftime("%B %d") if obj.csat_date else "N/A",
            }
        ]

    def get_GraphData(self, obj):
        # Fetch last 3 months of data for the project
        recent_entries = (
            Project.objects.filter(mydc_ref=obj.mydc_ref)
            .order_by("-month")[:3]
            .values(
                "month",
                "actual_otd_percent",
                "actual_rft_percent",
                "skill_compliance",
                "fte_count",
            )
        )
        recent_entries = list(
            reversed(recent_entries)
        )  # So it’s in chronological order

        # Extract data
        labels = [
            datetime.strptime(entry["month"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")
            for entry in recent_entries
        ]
        otd_data = [entry["actual_otd_percent"] for entry in recent_entries]
        rft_data = [entry["actual_rft_percent"] for entry in recent_entries]
        skill_data = [entry["skill_compliance"] for entry in recent_entries]
        fte_data = [entry["fte_count"] for entry in recent_entries]

        return [
            {
                "name": "On Time Delivery (OTD)",
                "type": "bar",
                "order": 1,
                "showlabel": True,
                "data": {
                    "labels": labels,
                    "datasets": [
                        {
                            "label": "OTD",
                            "data": otd_data,
                            "backgroundColor": "#00ff62",
                        }
                    ],
                },
                "options": self._get_chart_options(),
            },
            {
                "name": "Right First Time (RFT)",
                "type": "bar",
                "order": 2,
                "showlabel": True,
                "data": {
                    "labels": labels,
                    "datasets": [
                        {
                            "label": "RFT",
                            "data": rft_data,
                            "backgroundColor": "#0073ff",
                        }
                    ],
                },
                "options": self._get_chart_options(),
            },
            {
                "name": "Skill Compliance",
                "type": "bar",
                "order": 3,
                "showlabel": True,
                "data": {
                    "labels": labels,
                    "datasets": [
                        {
                            "label": "Skill",
                            "data": skill_data,
                            "backgroundColor": "#ffb700",
                            "order": 2,
                            "yAxisID": "y",
                        },
                        {
                            "label": "No of FTE",
                            "data": fte_data,
                            "backgroundColor": "red",
                            "type": "line",
                            "borderColor": "red",
                            "borderWidth": 2,
                            "order": 1,
                            "yAxisID": "y-right",
                        },
                    ],
                },
                "options": self._get_chart_options(extra_y_right=True),
            },
        ]
    
    def get_Documents(self, obj):
        documents = obj.documents.all()
        return ProjectDocumentInlineSerializer(documents, many=True).data
    
    def get_KPIData(self, obj):
        kpis = ProjectKPISummary.objects.filter(project=obj)
        return [
            {
                "id": kpi.id,
                "metric": kpi.metric,
                "h1": kpi.h1,
                "target_h": kpi.target_h,
                "htd": kpi.htd,
            }
            for kpi in kpis
        ]
    def get_FTESummary(self, obj):
        return ProjectFTESummarySerializer(obj.fte_summaries.all(), many=True).data

    def _get_chart_options(self, extra_y_right=False):
        options = {
            "plugins": {
                "datalabels": {
                    "display": True,
                    "color": "black",
                    "font": {"size": 20},
                },
                "legend": {"labels": {"font": {"size": 18, "weight": 600}}},
            },
            "scales": {
                "x": {"ticks": {"font": {"size": 20, "weight": "500"}}},
                "y": {"ticks": {"font": {"size": 20, "weight": "500"}}},
            },
        }
        if extra_y_right:
            options["scales"]["y-right"] = {
                "beginAtZero": True,
                "position": "right",
                "grid": {"drawOnChartArea": False},
                "ticks": {"font": {"size": 20, "weight": "500"}},
            }
        return options

class ProjectDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['id', 'project', 'document_name', 'document_link']