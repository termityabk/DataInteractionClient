import sys
import unittest
from unittest.mock import Mock, patch

import requests

sys.path.append("DataInteractionClient")
sys.path.append("/models/")
sys.path.append("/exceptions/")
from exceptions.DataSourceNotActiveException import \
    DataSourceNotActiveException
from models.RequestData import RequestData
from models.Tag import Tag

from DataInteractionClient import DataInteractionClient


class TestClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com"
        self.client = DataInteractionClient.DataInteractionClient(self.base_url)
        self.mock_response = Mock()
        self.mock_response.json.return_value = {"attributes": {"smtActive": True}}

    def test_connect(self):
        self.client._make_request = Mock(return_value=self.mock_response)
        data_source_id = "123"
        result = self.client.connect(data_source_id)
        self.assertEqual(result, {"attributes": {"smtActive": True}})
        self.client._make_request.assert_called_once_with(
            f"{self.base_url}/smt/dataSources/connect", {"id": data_source_id}
        )

    def test_connect_invalid_data_source_id(self):
        with self.assertRaises(ValueError):
            self.client.connect(123)

    def test_connect_data_source_not_active(self):
        self.mock_response.json.return_value = {"attributes": {"smtActive": False}}
        self.client._make_request = Mock(return_value=self.mock_response)
        with self.assertRaises(DataSourceNotActiveException):
            self.client.connect("123")

    def test_make_request_success(self):
        client = DataInteractionClient("https://example.com")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Request successful"}
        with patch("requests.post", return_value=mock_response) as mock_post:
            response = client._make_request(
                "https://example.com/api", {"param1": "value1"}
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Request successful"}
            mock_post.assert_called_once_with(
                "https://example.com/api", params={"param1": "value1"}, timeout=5
            )

    def test_set_data(self):
        self.base_url = "https://example.com"
        self.client = DataInteractionClient.DataInteractionClient(self.base_url)
        self.mock_response = Mock()
        self.client._make_request = Mock(return_value=self.mock_response)
        tag1 = Tag(tag_id="tag1", attributes=[], data={"value": 10})
        tag2 = Tag(tag_id="tag2", attributes=[], data={"value": 20})
        tags = [tag1, tag2]

        expected_response = {"status": "success"}
        self.mock_response.json.return_value = expected_response

        result = self.client.set_data(tags)

        self.assertEqual(result, expected_response)
        self.client._make_request.assert_called_once_with(
            f"{self.base_url}/smt/data/set",
            {
                "data": [
                    {"tagId": "tag1", "data": {"value": 10}},
                    {"tagId": "tag2", "data": {"value": 20}},
                ]
            },
        )

    def test_create_tags_with_valid_data(self):
        self.client = DataInteractionClient.DataInteractionClient("https://example.com")
        tags_data = [
            {
                "id": "tag1",
                "attributes": {"name": "Tag 1", "description": "Description 1"},
            },
            {
                "id": "tag2",
                "attributes": {"name": "Tag 2", "description": "Description 2"},
            },
        ]
        expected_tags = [
            Tag("tag1", {"name": "Tag 1", "description": "Description 1"}),
            Tag("tag2", {"name": "Tag 2", "description": "Description 2"}),
        ]
        result = self.client.create_tags(tags_data)
        self.assertEqual([tag.id for tag in result], [tag.id for tag in expected_tags])

    def test_create_tags_with_empty_list(self):
        tags_data = []
        expected_tags = []
        result = self.client.create_tags(tags_data)
        self.assertEqual(result, expected_tags)

    def test_create_tags_with_missing_id(self):
        tags_data = [{"attributes": {"name": "Tag 1", "description": "Description 1"}}]
        with self.assertRaises(KeyError):
            self.client.create_tags(tags_data)

    def test_create_tags_with_missing_attributes(self):
        tags_data = [{"id": "tag1"}]
        with self.assertRaises(KeyError):
            self.client.create_tags(tags_data)

    def test_create_tags_with_invalid_data_type(self):
        tags_data = "invalid data"
        with self.assertRaises(TypeError):
            self.client.create_tags(tags_data)

    def test_create_request_data_all_params(self):
        client = DataInteractionClient.DataInteractionClient("https://example.com")
        tag_id = ["tag1", "tag2"]
        from_time = "2022-01-01T00:00:00Z"
        to_time = "2022-01-02T00:00:00Z"
        max_count = 100
        time_step = 60000
        value = [int, float]
        format_param = True
        actual = False

        expected_request_data = {
            "tagId": tag_id,
            "from": from_time,
            "to": to_time,
            "maxCount": max_count,
            "timeStep": time_step,
            "value": value,
            "format": format_param,
            "actual": actual,
        }

        assert client.create_request_data(
            tag_id,
            from_time,
            to_time,
            max_count,
            time_step,
            value,
            format_param,
            actual,
        )

    def test_create_request_data_required_param(self):
        client = DataInteractionClient.DataInteractionClient("https://example.com")
        tag_id = "tag1"

        expected_request_data = {
            "tagId": tag_id,
            "from": None,
            "to": None,
            "maxCount": None,
            "timeStep": None,
            "value": None,
            "format": None,
            "actual": None,
        }

        assert client.create_request_data(tag_id)

    def test_create_request_data_optional_none(self):
        client = DataInteractionClient.DataInteractionClient("https://example.com")
        tag_id = "tag1"

        expected_request_data = {
            "tagId": tag_id,
            "from": None,
            "to": None,
            "maxCount": None,
            "timeStep": None,
            "value": None,
            "format": None,
            "actual": None,
        }

        assert client.create_request_data(
            tag_id, None, None, None, None, None, None, None
        )

    def test_create_request_data_list_tag_ids(self):
        client = DataInteractionClient.DataInteractionClient("https://example.com")
        tag_id = ["tag1", "tag2"]

        expected_request_data = {"tagId": tag_id, "from": 100, "to": 100000}

        assert client.create_request_data(tag_id)

    def test_create_request_data_single_tag_id(self):
        client = DataInteractionClient.DataInteractionClient("https://example.com")
        tag_id = "tag1"

        expected_request_data = {
            "tagId": tag_id,
            "from": None,
            "to": None,
            "maxCount": None,
            "timeStep": None,
            "value": None,
            "format": None,
            "actual": None,
        }

        assert client.create_request_data(tag_id)

    @patch("requests.post")
    def test_make_request_success(self, mock_post):
        self.client = DataInteractionClient.DataInteractionClient("https://example.com")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.client._make_request(
            "https://example.com/api", {"param": "value"}
        )

        mock_post.assert_called_once_with(
            "https://example.com/api", params={"param": "value"}, timeout=5
        )
        self.assertEqual(response, mock_response)

    @patch("requests.post")
    def test_make_request_timeout(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        with self.assertRaises(requests.exceptions.RequestException) as cm:
            self.client._make_request("https://example.com/api", {"param": "value"})

        self.assertEqual(str(cm.exception), "Ошибка запроса: Request timed out")

    @patch("requests.post")
    def test_make_request_generic_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException(
            "Generic request error"
        )

        with self.assertRaises(requests.exceptions.RequestException) as cm:
            self.client._make_request("https://example.com/api", {"param": "value"})

        self.assertEqual(str(cm.exception), "Ошибка запроса: Generic request error")


if __name__ == "__main__":
    unittest.main()
