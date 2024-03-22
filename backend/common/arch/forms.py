from typing import Self, Optional, Annotated

from django.http import HttpRequest

from pydantic import BaseModel, constr, Field


class Form(BaseModel):

    @classmethod
    def from_GET(cls, request: HttpRequest) -> Self:
        # noinspection PyArgumentList
        return cls(**request.GET.dict())

    @classmethod
    def from_POST(cls, request: HttpRequest) -> Self:
        return cls.parse_raw(request.body)


PositiveInt = Annotated[int, Field(gt=0)]


class WriteToDBForm(Form):
    path_to_tasks: constr(min_length=1)
    path_to_templates: constr(min_length=1)
    path_to_roles: constr(min_length=1)
    path_to_roles_list_wb: constr(min_length=1)


class PaginationForm(Form):
    page: PositiveInt | None = None
    per_page: PositiveInt | None = None

    @property
    def fr(self) -> int | None:
        if self.page and self.per_page:
            return (self.page - 1) * self.per_page
        else:
            return None

    @property
    def to(self) -> int | None:
        if self.page and self.per_page:
            return self.fr + self.per_page
        else:
            return None


class SearchForm(Form):
    search_text: constr(max_length=100) | None = None


class OrderForm(Form):
    order_by: constr(max_length=100) | None = None
    order_dir: constr(max_length=1) | None = None

    def get_ext_ordering_str(self, ext_field: str) -> str:
        if self.order_by:
            if self.order_dir == '-':
                return f'{self.order_dir}{ext_field}{self.order_by}'
            else:
                return f'{ext_field}{self.order_by}'
        else:
            return ''

    @property
    def ordering_str(self) -> str:
        if self.order_by:
            if self.order_dir == '-':
                return f'{self.order_dir}{self.order_by}'
            else:
                return f'{self.order_by}'
        else:
            return ''

    @property
    def order_sql_arg(self) -> str:
        if self.order_dir == '-':
            return 'DESC'
        else:
            return 'ASC'
