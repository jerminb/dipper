# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from datetime import datetime

from djongo import models
from enum import Enum
from enumfields import EnumField
from jsonfield import JSONField

from .modelfields import EmbeddedDictField

class JobStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    EXECUTION_FAILED = "FAILED"
    EXECUTION_SUCCESSFUL = "SUCCESSFUL"

class Job(models.Model):
    _id = models.ObjectIdField()
    external_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = EnumField(JobStatus,max_length=17)
    result = EmbeddedDictField(model_container=dict)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.external_id
