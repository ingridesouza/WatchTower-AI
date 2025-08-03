import django_filters as df

from .models import DetectionEvent


class EventFilter(df.FilterSet):
    from_dt = df.IsoDateTimeFilter(field_name="timestamp_utc", lookup_expr="gte")
    to_dt = df.IsoDateTimeFilter(field_name="timestamp_utc", lookup_expr="lte")
    violation = df.BooleanFilter(field_name="has_violation")

    class Meta:
        model = DetectionEvent
        fields = ["site", "area", "camera", "violation"]
