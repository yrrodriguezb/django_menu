from django import forms
from django.db.models import Q
from .models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = (
            'code',
            'name',
            'path',
            'level',
            'order',
            'parent',
            'last_child',
            'active',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].queryset = \
            Menu.objects \
                .filter(active=True) \
                .filter(Q(parent__isnull=False) | Q(level=1)) \
                .order_by('code')    

        self.fields['parent'].empty_label = 'None'

    def clean(self):
        data = self.cleaned_data

        if data.get('parent', None):
            parent = data.get('parent')
            parent_level = parent.level
            data['level'] = parent_level + 1
        else:
            data['level'] = 1

        if data.get('parent', None):
            data['code'] = data['parent'].code

        order = data.get('order', None)
        if order:
            level = data.get('level', 1)
            if level > 1:
                data['code'] += f'00{order}' if order > 0 and order < 10 else f'0{order}'
            else:
                data['code'] = f'00{order}' if order > 0 and order < 10 else f'0{order}'

        if data.get('last_child', False):
            if data.get('path', None) is None:
                self.add_error('path', 'The path is required because it\'s last child.')
            data['parent'] = None

        level = data.get('level', None)
        parent = data.get('parent', None)

        if level == 1 or parent:
            if level == 1 and parent:
                self.add_error('level', 'The menu with a level (1) cannot have an associated relative level')
            data['path'] = None

        code = data.get('code', None)
        if code:
            qs_code = Menu.objects.filter(code=code)

            if self.instance.pk:
                qs_code = qs_code.exclude(code=self.instance.code)
            if qs_code.exists():
                raise forms.ValidationError(f'The menu with code {code} already exists.')   

        return data