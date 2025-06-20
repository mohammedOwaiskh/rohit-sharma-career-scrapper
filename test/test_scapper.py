import pytest
from scrapper.utils import get_output_filepath


@pytest.mark.parametrize(
    "input,expected_extension,should_raise",
    [
        ("output.txt", None, True),
        ("output.csv", "csv", False),
        ("output.", None, True),
        ("output", None, True),
        ("output.parquet", "parquet", False),
    ],
)
def test_get_filepath_extension(input, expected_extension, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            _, extension = get_output_filepath(input)
    else:
        _, extension = get_output_filepath(input)
        assert extension == expected_extension
