import os
from logging import INFO, Logger, getLogger
from typing import Any, Optional

import boto3
from botocore.config import Config

logger: Logger = getLogger()
logger.setLevel(INFO)


class Api(object):
    _clients: dict = {}
    _resources: dict = {}

    @classmethod
    def get_client(
        cls,
        service: str,
        endpoint_url: Optional[str] = None,
        config: Optional[Config] = None,
        **kwargs
    ) -> Any:
        if service not in cls._clients:
            cls._clients[service] = boto3.client(
                service,
                endpoint_url=os.environ.get("AWS_ENDPOINT_URL", None)
                if endpoint_url is None
                else endpoint_url,
                config=config,
                **kwargs
            )

        logger.debug("service: {}, endpoint_url: {}".format(service, endpoint_url))
        return cls._clients[service]

    @classmethod
    def get_resource(
        cls,
        service: str,
        endpoint_url: Optional[str] = None,
        config: Optional[Config] = None,
        **kwargs
    ) -> Any:
        if service not in cls._resources:
            cls._resources[service] = boto3.resource(
                service,
                endpoint_url=os.environ.get("AWS_ENDPOINT_URL", None)
                if endpoint_url is None
                else endpoint_url,
                config=config,
                **kwargs
            )

        logger.debug("service: {}, endpoint_url: {}".format(service, endpoint_url))
        return cls._resources[service]
