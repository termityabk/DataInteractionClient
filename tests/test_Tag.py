import sys
sys.path.append("DataInteractionClient")

import unittest

from DataInteractionClient.models.tag import Tag


class TestTag(unittest.TestCase):
    def test_init_with_dict_id(self):
        tag_id = {"tagName": "tag1", "parentObjectId": "obj1"}
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(tag_id, attributes)
        self.assertEqual(tag.id, "tag1")
        self.assertEqual(tag.parent_object_id, "obj1")
        self.assertEqual(tag.attributes, attributes)
        self.assertIsNone(tag.data)

    def test_init_with_str_id(self):
        tag_id = "tag2"
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(tag_id, attributes)
        self.assertEqual(tag.id, tag_id)
        self.assertEqual(tag.parent_object_id, "")
        self.assertEqual(tag.attributes, attributes)
        self.assertIsNone(tag.data)

    def test_init_with_dict_id_missing_keys(self):
        tag_id = {"tagName": "tag3"}
        attributes = {"attr1": "value1", "attr2": "value2"}
        with self.assertRaises(KeyError):
            Tag(tag_id, attributes)

    def test_update_data(self):
        tag_id = "tag4"
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(tag_id, attributes, data=[1, 2, 3])
        new_data = [4, 5, 6]
        tag.update(new_data)
        self.assertEqual(tag.data, new_data)

    def test_update_data_empty_list(self):
        tag_id = "tag5"
        attributes = {"attr1": "value1", "attr2": "value2"}
        tag = Tag(tag_id, attributes, data=[1, 2, 3])
        new_data = []
        tag.update(new_data)
        self.assertEqual(tag.data, new_data)


if __name__ == "__main__":
    unittest.main()
