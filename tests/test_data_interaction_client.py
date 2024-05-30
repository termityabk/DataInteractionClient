import sys

sys.path.append("DataInteractionClient/")

import unittest
from unittest.mock import patch

import requests
from data_interaction_client import DataInteractionClient
from exceptions.data_source_not_active_exception import \
    DataSourceNotActiveException
from exceptions.no_data_to_send_exception import NoDataToSendException
from exceptions.server_response_error_exception import \
    ServerResponseErrorException
from models.tag import Tag
from pydantic_core._pydantic_core import ValidationError


class TestDataInteractionClient(unittest.TestCase):
    def test_connect_valid_id(self):
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
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            tags = client.connect(data_source_id="valid_id")
            assert len(tags) == 1
            assert tags[0].id == "tagId"
            assert tags[0].attributes["smtTagValueTypeCode"] == 1

    def test_connect_invalid_id(self):
        client = DataInteractionClient(base_url="https://example.com")
        mock_response = {
            "error": {"id": 0},
            "attributes": {
                "smtActive": False,
                "smtJsonConfigString": "some json string with connect parameters",
            },
        }
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            with self.assertRaises(DataSourceNotActiveException):
                client.connect(data_source_id="45345434")

    def test_set_data_valid_tags(self):
        client = DataInteractionClient(base_url="https://example.com")
        mock_response = {"error": {"id": 0}}
        tags = [
            Tag(
                id="tag1",
                attributes={"smtTagMaxDev": 1, "smtTagSource": "json config string"},
            )
        ]
        tags[0].add_data(x="2018-06-26 17:16:00", q=140, y=13)
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            client.set_data(tags=tags)
            assert mock_post.called
            assert mock_post.call_args[1]["params"]["data"] == [
                {
                    "tagId": "tag1",
                    "data": [{"x": "2018-06-26 17:16:00", "q": 140, "y": 13}],
                }
            ]
            assert all(tag.data is None for tag in tags)

    def test_set_data_no_data(self):
        client = DataInteractionClient(base_url="https://example.com")
        tags = [
            Tag(
                id="tag1",
                attributes={"smtTagMaxDev": 1, "smtTagSource": "json config string"},
            )
        ]
        with patch("requests.post") as mock_post:
            with self.assertRaises(NoDataToSendException):
                client.set_data(tags=tags)
            assert not mock_post.called

    def test_get_data_valid_params(self):
        client = DataInteractionClient(base_url="https://example.com")
        mock_response = {
            "error": {"id": 0},
            "data": [
                {
                    "tagId": "tag id",
                    "excess": False,
                    "data": [{"x": 100000, "y": 1, "q": 0}],
                }
            ],
        }
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            data = client.get_data(
                tag_id="tag1", from_time=1, to_time=3, max_count=10, time_step=1
            )
            assert mock_post.called
            assert mock_post.call_args[1]["params"]["params"] == {
                "from": 1,
                "to": 3,
                "tagId": "tag1",
                "maxCount": 10,
                "timeStep": 1,
            }
            assert data == [
                {
                    "tagId": "tag id",
                    "excess": False,
                    "data": [{"x": 100000, "y": 1, "q": 0}],
                }
            ]

    def test_connect_request_exception(self):
        client = DataInteractionClient(base_url="https://example.com")
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.RequestException()
            with self.assertRaises(requests.exceptions.RequestException):
                client.connect(data_source_id="valid_id")

    def test_connect_server_error_exceptions(self):
        client = DataInteractionClient(base_url="https://example.com")
        mock_response = {"error": {"id": 0, "message": "error"}}
        with patch("requests.post") as mock_post:
            mock_post.side_effect = ServerResponseErrorException(
                message="Сервер вернул внутреннюю ошибку: error"
            )
            with self.assertRaises(ServerResponseErrorException):
                client.connect(data_source_id="valid_id")


if __name__ == "__main__":
    unittest.main()
