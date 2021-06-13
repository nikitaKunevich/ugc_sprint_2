import sentry_sdk
from config import settings

sentry_sdk.init(dsn=settings.sentry_dsn)

sentry_sdk.init(
    dsn=settings.sentry_dsn, max_breadcrumbs=150, environment=settings.environment
)
