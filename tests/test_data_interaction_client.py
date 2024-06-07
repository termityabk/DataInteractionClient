import sys
sys.path.append("DataInteractionClient/")
from unittest.mock import patch

import pytest
import httpx

from data_interaction_client import DataInteractionClient
from exceptions.data_source_not_active_exception import \
    DataSourceNotActiveException


def test_connect_valid_id():
    client = DataInteractionClient(base_url="https://example.com")
    mock_response = {
        "error": {"id": 0},
        "attributes": {
            "smtActive": True,
            "smtJsonConfigString": "some json string with connect parameters",
        },
        "tags": [
            {
                "id": "tagId",
                "attributes": {
                    "smtTagValueTypeCode": 1,
                    "smtTagValueScale": 1,
                    "smtTagMaxDev": 1,
                    "smtTagSource": "json config string",
                },
            }
        ],
    }
    with patch("httpx.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        tags = client.connect(data_source_id="valid_id")
        assert len(tags) == 1
        assert tags[0].id == "tagId"
        assert tags[0].attributes["smtTagValueTypeCode"] == 1


def test_connect_invalid_id():
    client = DataInteractionClient(base_url="https://example.com")
    mock_response = {
        "error": {"id": 0},
        "attributes": {
            "smtActive": False,
            "smtJsonConfigString": "some json string with connect parameters",
        },
    }
    with patch("httpx.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        with pytest.raises(DataSourceNotActiveException):
            client.connect(data_source_id="45345434")


#... and so on for the rest of the test cases