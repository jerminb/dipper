# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import viewsets

from .serializers import JobSerializer
from .models import Job

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('created_at')
    serializer_class = JobSerializer
