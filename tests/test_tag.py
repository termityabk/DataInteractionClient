import sys
sys.path.append("DataInteractionClient/")

import pytest

from models.tag import Tag


def test_init_with_dict_id():
    tag_id = {"tagName": "tag1", "parentObjectId": "obj1"}
    attributes = {"attr1": "value1", "attr2": "value2"}
    tag = Tag(id=tag_id, attributes=attributes)
    assert tag.id["tagName"] == "tag1"
    assert tag.id["parentObjectId"] == "obj1"
    assert tag.attributes == attributes
    assert tag.data is None


def test_init_with_str_id():
    tag_id = "tag2"
    attributes = {"attr1": "value1", "attr2": "value2"}
    tag = Tag(id=tag_id, attributes=attributes)
    assert tag.id == tag_id
    assert tag.attributes == attributes
    assert tag.data is None


def test_add_data():
    tag_id = "tag4"
    attributes = {"attr1": "value1", "attr2": "value2"}
    tag = Tag(id=tag_id, attributes=attributes)
    tag.add_data(x="563", y=1, q=0)
    assert tag.data[-1] == {"x": "563", "y": 1, "q": 0}


def test_init_with_dict_id_missing_keys():
    tag_id = {"tagName": "tag3"}
    attributes = {"attr1": "value1", "attr2": "value2"}
    with pytest.raises(ValueError):
        Tag(id=tag_id, attributes=attributes)


def test_clear_data():
    tag_id = "tag6"
    attributes = {"attr1": "value1", "attr2": "value2"}
    tag = Tag(id=tag_id, attributes=attributes)
    tag.add_data(x="563", y=1, q=0)
    tag.clear_data()
    assert tag.data is None
