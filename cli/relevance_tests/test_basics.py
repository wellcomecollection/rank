import pytest
from . import get_rank_elastic_client

client = get_rank_elastic_client()


def test_basics():
    assert client.ping() == True
