"""Tests for c3_invoke.output — JSON parsing from CLI output."""

import pytest

from c3_invoke.output import parse_json_output


class TestParseJsonOutput:
    def test_plain_json_array(self):
        result = parse_json_output('["Python", "TypeScript"]')
        assert result == ["Python", "TypeScript"]

    def test_plain_json_object(self):
        result = parse_json_output('{"score": 85}')
        assert result == {"score": 85}

    def test_json_in_markdown_fence(self):
        text = '```json\n["React", "Node.js"]\n```'
        assert parse_json_output(text) == ["React", "Node.js"]

    def test_json_in_generic_fence(self):
        text = '```\n{"key": "value"}\n```'
        assert parse_json_output(text) == {"key": "value"}

    def test_embedded_json_after_preamble(self):
        text = 'Here are the skills:\n["Python", "Docker"]'
        assert parse_json_output(text) == ["Python", "Docker"]

    def test_embedded_object_after_preamble(self):
        text = "Based on my analysis:\n{\"score\": 42, \"decision\": \"Apply\"}"
        result = parse_json_output(text)
        assert result["score"] == 42
        assert result["decision"] == "Apply"

    def test_empty_input_raises(self):
        with pytest.raises(ValueError, match="empty"):
            parse_json_output("")

    def test_none_input_raises(self):
        with pytest.raises(ValueError, match="empty"):
            parse_json_output(None)

    def test_no_json_raises(self):
        with pytest.raises(ValueError, match="valid JSON"):
            parse_json_output("This is just plain text with no JSON.")

    def test_whitespace_around_json(self):
        result = parse_json_output("  \n  [1, 2, 3]  \n  ")
        assert result == [1, 2, 3]

    def test_nested_json(self):
        text = '{"items": [{"name": "Python"}, {"name": "Go"}]}'
        result = parse_json_output(text)
        assert len(result["items"]) == 2
