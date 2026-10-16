import pytest
from app.utils.anonymous_id import (
    generate_anonymous_id,
    validate_anonymous_id,
    normalize_anonymous_id,
    SAFE_ALPHANUMERIC,
    ANONYMOUS_ID_LENGTH,
)


class TestAnonymousId:
    def test_generate_anonymous_id_format(self):
        anon_id = generate_anonymous_id()
        assert isinstance(anon_id, str)
        assert len(anon_id) == ANONYMOUS_ID_LENGTH
        assert validate_anonymous_id(anon_id) is True

    def test_generate_unique_ids(self):
        ids = {generate_anonymous_id() for _ in range(50)}
        assert len(ids) == 50

    def test_no_confusing_characters(self):
        for _ in range(100):
            anon_id = generate_anonymous_id()
            for char in ["0", "O", "1", "I", "L", "l", "o"]:
                assert char not in anon_id

    def test_validate_valid_ids(self):
        assert validate_anonymous_id("AX7K29P4") is True
        assert validate_anonymous_id("ax7k29p4") is True  # normalizes to uppercase
        assert validate_anonymous_id("  CZ9M42W8  ") is True

    def test_validate_invalid_ids(self):
        assert validate_anonymous_id("") is False
        assert validate_anonymous_id(None) is False
        assert validate_anonymous_id("SHORT") is False
        assert validate_anonymous_id("TOOLONGID123") is False
        assert validate_anonymous_id("AX7K29P!") is False  # special character
        assert validate_anonymous_id("AX7K29P0") is False  # contains '0' which is excluded

    def test_normalize_anonymous_id(self):
        assert normalize_anonymous_id("  ax7k29p4  ") == "AX7K29P4"
        assert normalize_anonymous_id("") == ""
        assert normalize_anonymous_id(None) == ""
