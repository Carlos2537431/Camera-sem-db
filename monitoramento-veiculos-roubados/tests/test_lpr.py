import pytest
from src.services.lpr.processor import process_image
from src.services.lpr.validators import validate_plate

def test_process_image_valid_plate():
    image_path = "tests/images/valid_plate.jpg"  # Path to a test image with a valid plate
    result = process_image(image_path)
    assert result is not None
    assert validate_plate(result) is True

def test_process_image_invalid_plate():
    image_path = "tests/images/invalid_plate.jpg"  # Path to a test image with an invalid plate
    result = process_image(image_path)
    assert result is None

def test_validate_plate_valid():
    valid_plate = "ABC1D23"
    assert validate_plate(valid_plate) is True

def test_validate_plate_invalid():
    invalid_plate = "AB1234"
    assert validate_plate(invalid_plate) is False

def test_process_image_no_plate():
    image_path = "tests/images/no_plate.jpg"  # Path to a test image with no plate
    result = process_image(image_path)
    assert result is None