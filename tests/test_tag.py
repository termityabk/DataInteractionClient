import sys

sys.path.append("DataInteractionClient/models/")

import unittest

from pydantic_core._pydantic_core import ValidationError
from tag import Tag


class TestTag(unittest.TestCase):
    def test_init_with_dict_id(self):
        tag_id = {"tagName": "tag1", "parentObjectId": "obj1"}
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(id=tag_id, attributes=attributes)
        self.assertEqual(tag.id["tagName"], "tag1")
        self.assertEqual(tag.id["parentObjectId"], "obj1")
        self.assertEqual(tag.attributes, attributes)
        self.assertIsNone(tag.data)

    def test_init_with_str_id(self):
        tag_id = "tag2"
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(id=tag_id, attributes=attributes)
        self.assertEqual(tag.id, tag_id)
        self.assertEqual(tag.attributes, attributes)
        self.assertIsNone(tag.data)

    def test_add_data(self):
        tag_id = "tag4"
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(id=tag_id, attributes=attributes)
        tag.add_data(x="563", y=1, q=0)
        self.assertEqual(tag.data[-1], {"x": "563", "y": 1, "q": 0})

    def test_init_with_dict_id_missing_keys(self):
        tag_id = {"tagName": "tag3"}
        attributes = {"attr1": "value1", "attr2": "value2"}
        with self.assertRaises(ValueError):
            Tag(id=tag_id, attributes=attributes)

    def test_add_data_empty_list(self):
        tag_id = "tag5"
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(id=tag_id, attributes=attributes)

        with self.assertRaises(ValidationError):
            tag.add_data()

    def test_clear_data(self):
        tag_id = "tag6"
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(id=tag_id, attributes=attributes)
        tag.add_data(x="563", y=1, q=0)
        tag.clear_data()
        self.assertEqual(tag.data, None)


if __name__ == "__main__":
    unittest.main()
