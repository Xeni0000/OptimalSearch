from typing import Self

from django.http import HttpRequest

from pydantic import BaseModel, constr


class Form(BaseModel):

    @classmethod
    def from_GET(cls, request: HttpRequest) -> Self:
        # noinspection PyArgumentList
        return cls(**request.GET.dict())

    @classmethod
    def from_POST(cls, request: HttpRequest) -> Self:
        return cls.parse_raw(request.body)


class WriteToDBForm(Form):
    path_to_tasks: constr(min_length=1)
    path_to_templates: constr(min_length=1)
    path_to_roles: constr(min_length=1)
    path_to_roles_list_wb: constr(min_length=1)
