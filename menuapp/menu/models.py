from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.urls.exceptions import NoReverseMatch
from django.urls import reverse
from django.conf import settings
import re


class MyURLValidator(URLValidator):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.regex2 = re.compile(r"^(?:[/?#][^\s]*)?\Z")

  def __call__(self, value) -> None:
    try:
      super().__call__(value)
    except ValidationError:
      if self.regex2.match(value) is None:
        raise ValidationError("MyURLValidator ERROR")
      

url_validator = MyURLValidator()

class MenuModel(models.Model):
  name = models.CharField(
    max_length=20,
    unique=True
  )

  parent = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )

  title = models.CharField(
    max_length=64
  )

  url = models.CharField(
    max_length=200
  )

  @property
  def get_url(self):
    try:
      a = self.url.split('?')[0]
      url_validator(a)
      return self.url
    except ValidationError as err:
      try:
        return reverse(self.url)
      except NoReverseMatch as err:
        return settings.MENU_DEFAULT_REDIRECT

  @classmethod
  def get_menu(cls, name:str):
    q = f"""
    with recursive parents as (
      select m1.*, 0 as root
      from {cls._meta.db_table} m1
      where m1.name = %s
      union
      select m2.* , p1.root + 1 as root
      from {cls._meta.db_table} m2
      join parents p1 on p1.id = m2.parent_id
    )
    select * from parents
    order by root;
    """
    return cls.objects.raw(q, (name,))


  def __repr__(self) -> str:
    return f"{self.__class__.__name__}(id={self.id}, name='{self.name}')"
  
  def __str__(self) -> str:
    return self.__repr__()