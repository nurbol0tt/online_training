import sqlalchemy as sa
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:

    created_at = sa.Column(
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.FetchedValue(),
    )
    updated_at = sa.Column(
        sa.DateTime,
        onupdate=sa.func.now(),
        server_default=sa.FetchedValue(),
        server_onupdate=sa.FetchedValue(),
    )