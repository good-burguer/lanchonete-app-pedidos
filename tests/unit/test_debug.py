"""Tests for app.adapters.utils.debug module"""

import sys
import os
from pathlib import Path
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from app.adapters.utils.debug import var_dump_die
from fastapi import HTTPException


def test_var_dump_die_with_dict():
    """Test var_dump_die raises HTTPException with dict data"""
    test_data = {"key": "value", "number": 42}
    
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(test_data)
    
    exception = exc_info.value
    assert exception.status_code == 400
    assert isinstance(exception.detail, dict)
    assert exception.detail["debug"] is True
    assert "location" in exception.detail
    assert "data" in exception.detail
    assert exception.detail["data"]["key"] == "value"


def test_var_dump_die_with_list():
    """Test var_dump_die with list data"""
    test_data = [1, 2, 3, "test"]
    
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(test_data)
    
    exception = exc_info.value
    assert exception.status_code == 400
    assert exception.detail["debug"] is True


def test_var_dump_die_with_string():
    """Test var_dump_die with string data"""
    test_data = "test string"
    
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(test_data)
    
    exception = exc_info.value
    assert exception.status_code == 400
    assert exception.detail["debug"] is True


def test_var_dump_die_includes_location_info():
    """Test that var_dump_die includes location information"""
    test_data = {"test": True}
    
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(test_data)
    
    exception = exc_info.value
    location = exception.detail["location"]
    assert "file" in location
    assert "line" in location
    assert "function" in location
    assert location["file"] == "test_debug.py"


def test_var_dump_die_with_complex_object():
    """Test var_dump_die with complex nested objects"""
    test_data = {
        "nested": {
            "deep": {
                "value": 123
            }
        },
        "list": [1, 2, 3],
        "string": "test"
    }
    
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(test_data)
    
    exception = exc_info.value
    assert exception.status_code == 400
    assert exception.detail["debug"] is True


def test_var_dump_die_with_none():
    """Test var_dump_die with None value"""
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(None)
    
    exception = exc_info.value
    assert exception.status_code == 400
    assert exception.detail["debug"] is True


def test_var_dump_die_with_number():
    """Test var_dump_die with numeric value"""
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(42)
    
    exception = exc_info.value
    assert exception.status_code == 400


def test_var_dump_die_with_boolean():
    """Test var_dump_die with boolean value"""
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die(False)
    
    exception = exc_info.value
    assert exception.status_code == 400
