import sys
sys.path.append("DataInteractionClient/")
from unittest.mock import AsyncMock

import pytest
import httpx

from async_data_interaction_client import AsyncDataInteractionClient
from exceptions.data_source_not_active_exception import \
    DataSourceNotActiveException
from models.tag import Tag


@pytest.mark.asyncio
async def test_connect_active_source():
    client = AsyncDataInteractionClient(base_url="http://example.com")
    mock_response = {
        "attributes": {"smtActive": True},
        "tags": [
            {"id": "tag1", "attributes": {"name": "Tag 1"}},
            {"id": "tag2", "attributes": {"name": "Tag 2"}},
        ],
    }
    client._make_request = AsyncMock(return_value=mock_response)

    result = await client.connect(data_source_id="source1")

    assert len(result) == 2
    assert isinstance(result[0], Tag)
    assert result[0].id == "tag1"
    assert result[0].attributes["name"] == "Tag 1"
    assert isinstance(result[1], Tag)
    assert result[1].id == "tag2"
    assert result[1].attributes["name"] == "Tag 2"


@pytest.mark.asyncio
async def test_connect_inactive_source():
    client = AsyncDataInteractionClient(base_url="http://example.com")
    mock_response = {"attributes": {"smtActive": False}, "tags": []}
    client._make_request = AsyncMock(return_value=mock_response)

    with pytest.raises(DataSourceNotActiveException):
        await client.connect(data_source_id="source2")


@pytest.mark.asyncio
async def test_connect_request_error():
    client = AsyncDataInteractionClient(base_url="http://example.com")
    client._make_request = AsyncMock(
        side_effect=httpx.RequestError("Request failed")
    )

    with pytest.raises(httpx.RequestError):
        await client.connect(data_source_id="source3")
