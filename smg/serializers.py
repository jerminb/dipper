from rest_framework import serializers
from .models import Job, JobStatus
from . import fields

class JobSerializer(serializers.HyperlinkedModelSerializer):
    _id = fields.ObjectIdField(read_only=True)
    status = fields.EnumField(enum=JobStatus)
    result = serializers.DictField()
    class Meta:
        model = Job
        fields = '__all__'
