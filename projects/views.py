from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Max
from django.shortcuts import get_object_or_404
from .models import Project, ProjectDocument, ProjectKPISummary, ProjectFTESummary
from .serializers import (
    ProjectOverviewSerializer,
    ProjectDetailSerializer,
    ProjectDocumentSerializer,
    ProjectKPISummarySerializer,
    ProjectFTESummarySerializer,
)

class ProjectOverviewAPI(APIView):
    permission_classes = [AllowAny]


    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectOverviewSerializer(projects, many=True)
        return Response({"data": serializer.data})


class ProjectDetailAPI(APIView):
    permission_classes = [AllowAny]

    
    def get(self, request, project_id):
        try:
            latest_month = Project.objects.filter(mydc_ref=project_id).aggregate(
                Max("month")
            )["month__max"]

            if not latest_month:
                return Response(
                    {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            project = Project.objects.get(mydc_ref=project_id, month=latest_month)
            serializer = ProjectDetailSerializer(project)
            return Response({"data": [serializer.data]})

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
class ProjectDocumentCreateView(generics.CreateAPIView):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer

class ProjectKPISummaryView(APIView):

    def post(self, request):
        serializer = ProjectKPISummarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "KPI created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        kpi = get_object_or_404(ProjectKPISummary, pk=pk)
        serializer = ProjectKPISummarySerializer(kpi, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "KPI updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        kpi = get_object_or_404(ProjectKPISummary, pk=pk)
        kpi.delete()
        return Response({"message": "KPI deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class ProjectFTESummaryView(APIView):

    def post(self, request):
        serializer = ProjectFTESummarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "FTE Summary created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        fte = get_object_or_404(ProjectFTESummary, pk=pk)
        serializer = ProjectFTESummarySerializer(fte, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "FTE Summary updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        fte = get_object_or_404(ProjectFTESummary, pk=pk)
        fte.delete()
        return Response({"message": "FTE Summary deleted"}, status=status.HTTP_204_NO_CONTENT)