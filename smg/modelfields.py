from django.db.models import Field, Model
from django import forms
import typing

class EmbeddedDictField(Field):
    def __init__(self,
                 model_container: typing.Type[dict],
                 model_form_class: typing.Type[forms.ModelForm] = None,
                 model_form_kwargs: dict = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_container = model_container
        self.model_form_class = model_form_class
        self.null = True
        self.instance = None

        if model_form_kwargs is None:
            model_form_kwargs = {}
        self.model_form_kwargs = model_form_kwargs

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['model_container'] = self.model_container
        if self.model_form_class is not None:
            kwargs['model_form_class'] = self.model_form_class
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        return self.get_db_prep_value(value, None, False)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if not value:
            return value

        if isinstance(value, dict):
            return value
            
        raise TypeError('Object must be of type dict')

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def db_type(self, connection):
        return 'dict'
