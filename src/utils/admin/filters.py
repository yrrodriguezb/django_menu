from django.contrib import admin


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class DropdownFilter(admin.SimpleListFilter):
    template = 'admin/select_filter.html'

    def lookups(self, request, model_admin):
        return ((),)


class ActiveDropdownFilter(DropdownFilter):
    title = 'active'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('0', 'Deactivate'),
            ('1', 'Active'),
        )

class EmptyDropdownFilter(DropdownFilter):
    parameter_name = 'empty'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Empty'),
            ('0', 'Not Empty'),
        )