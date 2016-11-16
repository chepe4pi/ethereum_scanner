from constance import config


class FilterPaginatorViewMixin:
    def get_kwargs_for_filtering(self):
        filtering_kwargs = {}
        for field in self.filter_fields:
            field_value = self.request.query_params.get(field)
            if field_value:
                field_value = field_value.rstrip('/')
                filtering_kwargs[field] = field_value
        return filtering_kwargs

    def get_pagination_kwargs(self):
        request_limit = int(self.request.query_params.get('limit', None) or config.MAX_ROWS_IN_API_RESPONSE)
        offset = int(self.request.query_params.get('offset', 0))
        limit = request_limit if request_limit <= config.MAX_ROWS_IN_API_RESPONSE else config.MAX_ROWS_IN_API_RESPONSE

        return limit, offset

    def get_queryset(self):
        queryset = self.queryset
        filtering_kwargs = self.get_kwargs_for_filtering()
        if filtering_kwargs:
            queryset = queryset.filter(**filtering_kwargs)

        limit, offset = self.get_pagination_kwargs()
        if offset:
            queryset = queryset.skip(offset)
        return queryset.limit(limit)
