from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from utils.models import BaseModel


LEVELS = [ (x, x) for x in range(1, 15) ]

class Menu(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    path = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=30)
    level = models.PositiveSmallIntegerField(choices=LEVELS)
    order = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    active = models.BooleanField(default=True)
    last_child = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ('code',)
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return f'<{self.code}>: {self.name}'

    @property
    def code_name(self):
        return f'<{self.code}>: {self.name}'

    def clean(self):
        if self.parent:
            self.level = self.parent.level + 1
            self.code = f'{self.parent.code}'
        else:
            self.level = 1

        if self.order:
            if self.level > 1:
                self.code += f'00{self.order}' if self.order > 0 and self.order < 10 else f'0{self.order}'
            else:
                self.code = f'00{self.order}' if self.order > 0 and self.order < 10 else f'0{self.order}'
            
        if self.last_child:
            self.parent = None

        if self.level == 1 or self.parent:
            self.path = None