class FilterViewMixin:
    def get_kwargs_for_filtering(self):
        filtering_kwargs = {}
        for field in self.filter_fields:
            field_value = self.request.query_params.get(field)
            if field_value:
                field_value = field_value.rstrip('/')
                filtering_kwargs[field] = field_value
        return filtering_kwargs

    def get_queryset(self):
        queryset = self.queryset
        filtering_kwargs = self.get_kwargs_for_filtering()
        if filtering_kwargs:
            queryset = queryset.filter(**filtering_kwargs)
        return queryset
