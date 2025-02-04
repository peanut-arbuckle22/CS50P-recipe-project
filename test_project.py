import project
import pytest # type: ignore

def test_file_search():
    assert project.file_search("key lime") == ["Key Lime Pie"]
    assert project.file_search("hamburgers") == "No Results Found"

def test_file_fetch():
    with open("recipes//cake cornbread.txt") as file:
        assert project.file_fetch("cake cornbread") == file.read()

def test_file_name_fix():
    assert project.file_name_fix("cookie/// cake") == "cookie cake"
    assert project.file_name_fix("apple pie") == "apple pie"