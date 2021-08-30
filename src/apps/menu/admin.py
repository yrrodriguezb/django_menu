from django.contrib import admin, messages
from django.db.models import CharField, Q, Value as V
from django.db.models.functions import Concat
from apps.menu.models import Menu
from utils.admin import filters
from .forms import MenuForm

class ActiveListFilter(filters.ActiveDropdownFilter):
    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(active__iexact=self.value())
        return queryset

class PathEmptyListFilter(filters.EmptyDropdownFilter):
    title = 'path'

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            queryset = queryset.filter(path__isnull=True)
        elif value == '0':
            queryset = queryset.filter(path__isnull=False)
        return queryset


class NameInputFilter(filters.InputFilter):
    parameter_name = 'i'
    title = 'Name'

    def queryset(self, request, queryset):
        term = self.value()

        if term is None:
            return

        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(name__icontains=bit) |
                Q(code__icontains=bit)
            )

        return queryset.filter(any_name)
        
class ParentCodeDropdownFilter(filters.DropdownFilter):
    title = 'parent'
    template = "admin/select_filter.html"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return Menu.objects.all() \
            .filter(Q(parent__isnull=False) | Q(level=1)) \
            .annotate(
                code_name=Concat(V('<'), 'code', V('>: '), 'name', 
                output_field=CharField())
            ) \
            .values_list('code', 'code_name')


    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()
        if value:
            queryset = queryset.filter(code__startswith=value)
        return queryset


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    form = MenuForm
    empty_value_display = ''
    actions = None 
    
    list_display = (
        'code',
        'name',
        'path',
        'level',
        'last_child',
        'parent',
    )

    list_filter = (
        ActiveListFilter,
        ParentCodeDropdownFilter,
        PathEmptyListFilter,
        NameInputFilter
    )

    readonly_fields = (
        'code',
        'level',
    )

    search_fields = (
        'code__startswith',
        'name',
        'path',
    )

    fieldsets = (
        ('Data', {
            'fields': (
                ('code',),
                ('name',), 
                ('path',),
            )
        }),
        ('Advanced options', {
            'fields': ('parent', 'order', 'last_child', 'active'),
        }),
    )

    def save_model(self, request, obj, form, change):
        queryset = Menu.objects.filter(code=obj.code)
  
        if change:
            queryset = queryset.exclude(code=obj.code)

        if not queryset.exists():
            return super().save_model(request, obj, form, change)

        messages.set_level(request, messages.ERROR)
        messages.error(request, f'The menu with code {obj.code} already exists.')
       