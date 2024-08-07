from typing import Any, Optional

from dbt_copilot_python.database import database_url_from_env
from dbt_copilot_python.utility import is_copilot
from opensearchpy import RequestsHttpConnection
from pydantic import BaseModel, ConfigDict, computed_field
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

from conf.helpers import get_env_files, is_circleci, is_local


class BaseSettings(PydanticBaseSettings):
    """Base class holding all environment variables for Great."""

    model_config = SettingsConfigDict(
        extra="ignore",
        validate_default=False,
    )

    # Start of Environment Variables
    debug: bool = False
    app_environment: str = 'dev'
    static_host: str = ""
    staticfiles_storage: str = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    secret_key: str
    signature_secret: str
    feature_openapi_enabled: bool = False
    health_check_token: str
    sentry_dsn: str = ""
    sentry_environment: str = ""
    sentry_enable_tracing: bool = False
    sentry_traces_sample_rate: float = 1.0
    session_cookie_domain: str = ""
    session_cookie_secure: bool = True
    csrf_cookie_secure: bool = True
    gecko_api_key: str = ""
    gecko_api_pass: str = "X"
    opensearch_company_index_alias: str = "ch-companies"
    opensearch_chunk_size: int = 10000
    opensearch_timeout_seconds: int = 30
    opensearch_thread_count: int = 4
    opensearch_use_parallel_bulk: bool = False
    companies_house_api_key: str


class CIEnvironment(BaseSettings):

    @computed_field(return_type=dict)
    @property
    def opensearch_config(self):
        return {
            "alias": "default",
            "hosts": ["localhost:9200"],
            "use_ssl": False,
            "verify_certs": False,
            "connection_class": RequestsHttpConnection,
        }

    database_url: str
    redis_url: str


class DBTPlatformEnvironment(BaseSettings):
    """Class holding all listed environment variables on DBT Platform.

    Instance attributes are matched to environment variables by name (ignoring case).
    e.g. DBTPlatformEnvironment.app_environment loads and validates the APP_ENVIRONMENT environment variable.
    """

    build_step: bool = False
    celery_broker_url: str = ""
    opensearch_url: str

    @computed_field(return_type=str)
    @property
    def database_url(self):
        return database_url_from_env("DATABASE_CREDENTIALS")

    @computed_field(return_type=str)
    @property
    def redis_url(self):
        return self.celery_broker_url

    @computed_field(return_type=dict)
    @property
    def opensearch_config(self):
        return {
            "alias": "default",
            "hosts": [self.opensearch_url],
            "connection_class": RequestsHttpConnection,
            "http_compress": True,
        }


class GovPaasEnvironment(BaseSettings):
    """Class holding all listed environment variables on Gov PaaS.

    Instance attributes are matched to environment variables by name (ignoring case).
    e.g. GovPaasSettings.app_environment loads and validates the APP_ENVIRONMENT environment variable.
    """

    class VCAPServices(BaseModel):
        """Config of services bound to the Gov PaaS application"""

        model_config = ConfigDict(extra="ignore")

        postgres: list[dict[str, Any]]
        redis: list[dict[str, Any]]
        opensearch: list[dict[str, Any]]

    class VCAPApplication(BaseModel):
        """Config of the Gov PaaS application"""

        model_config = ConfigDict(extra="ignore")

        application_id: str
        application_name: str
        application_uris: list[str]
        cf_api: str
        limits: dict[str, Any]
        name: str
        organization_id: str
        organization_name: str
        space_id: str
        uris: list[str]

    model_config = ConfigDict(extra="ignore")

    vcap_services: Optional[VCAPServices] = None
    vcap_application: Optional[VCAPApplication] = None

    @computed_field(return_type=str)
    @property
    def database_url(self):
        if self.vcap_services:
            return self.vcap_services.postgres[0]["credentials"]["uri"]

        return "postgres://"

    @computed_field(return_type=str)
    @property
    def redis_url(self):
        if self.vcap_services:
            return self.vcap_services.redis[0]["credentials"]["uri"]

        return "rediss://"

    @computed_field(return_type=str)
    @property
    def opensearch_url(self):
        if self.vcap_services:
            return self.vcap_services.opensearch[0]["credentials"]["uri"]
        return "https://"

    @computed_field(return_type=dict)
    @property
    def opensearch_config(self):
        return {
            "alias": "default",
            "hosts": [self.opensearch_url],
            "connection_class": RequestsHttpConnection,
            "http_compress": True,
        }


if is_local() or is_circleci():
    # Load environment files in a local or CI environment
    env = CIEnvironment(_env_file=get_env_files(), _env_file_encoding="utf-8")
elif is_copilot():
    # When deployed read values from DBT Platform environment
    env = DBTPlatformEnvironment()
else:
    # When deployed read values from Gov PaaS environment
    env = GovPaasEnvironment()
