import pytest
from unittest.mock import patch, MagicMock
import barky

# Testing clear_screen function
def test_clear_screen():
    with patch("os.system") as clear_test:
        barky.clear_screen()
        clear_test.assert_called()

# Testing the print_options function
def test_print_options(capsys):
    options = {'A': barky.Option('Add a bookmark', None)}
    barky.print_options(options)
    captured = capsys.readouterr()
    assert "(A) Add a bookmark\n\n" in captured.out

# Testing option_choice_is_valid function
@pytest.mark.parametrize("choice, options, expected", [
    ('c', {'C': None}, True),
    ('B', {'A': None}, False),
])
def test_option_choice_is_valid(choice, options, expected):
    assert barky.option_choice_is_valid(choice, options) == expected

# Mocking input data for function get_option_choice and testing get_option_choice function
@patch('builtins.input', side_effect=['A'])
def test_get_option_choice(mock_input):
    options = {'A': barky.Option('Add a bookmark', MagicMock())}
    chosen_option = barky.get_option_choice(options)
    assert chosen_option.name == 'Add a bookmark'

# Mock input data for the function get_user_input and testing get_ne_bookmark_data function
@patch('builtins.input', side_effect=['Test Title', 'Test URL', 'Test Notes'])
def test_get_new_bookmark_data(input):
    expected = {
        "title": "Test Title",
        "url": "Test URL",
        "notes": "Test Notes",
    }
    assert barky.get_new_bookmark_data() == expected


# Testing get_new_bookmark_data()
@patch('barky.get_user_input', side_effect=['Test Title', 'Test URL', 'Test Notes'])
def test_get_new_bookmark_data(user_input):
    expected = {
        "title": "Test Title",
        "url": "Test URL",
        "notes": "Test Notes",
    }
    assert barky.get_new_bookmark_data() == expected
    assert user_input.call_count == 3


# Testing get_bookmark_id_for_deletion()
@patch('barky.get_user_input', return_value='123')
def test_get_bookmark_id_for_deletion(user_input):
    assert barky.get_bookmark_id_for_deletion() == '123'


# Testing get_github_import_options()
@patch('barky.get_user_input', side_effect=['octocat', 'Y'])
def test_get_github_import_options(user_input):
    expected = {
        "github_username": "octocat",
        "preserve_timestamps": True,
    }
    assert barky.get_github_import_options() == expected
    assert user_input.call_count == 2


# Testing get_new_bookmark_info()
@patch('barky.get_user_input', side_effect=['123', 'title', 'New Title'])
def test_get_new_bookmark_info(input):
    expected = {
        "id": "123",
        "update": {"title": "New Title"},
    }
    assert barky.get_new_bookmark_info() == expected
    assert input.call_count == 3
