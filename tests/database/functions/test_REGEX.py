from codebase.database.functions.REGEX import regex_pattern_match


def test_regex_pattern_match():
    assert regex_pattern_match(r'\d+', 123) is False
    assert regex_pattern_match(r'\d+', '123') is True
    assert regex_pattern_match(r'\d{3}', 'arun') is False
