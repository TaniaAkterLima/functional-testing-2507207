"""Unit tests for Flask application app.py verifying routes, execution, and health."""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Target Function Runner" in response.data
    assert b"Live Deployed Commit SHA" in response.data


def test_health_route(client, monkeypatch):
    monkeypatch.setenv("RENDER_GIT_COMMIT", "test-sha-12345")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["commit_sha"] == "test-sha-12345"


def test_api_run_missing_func(client):
    response = client.post("/api/run", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Missing 'func' parameter" in data["error"]


def test_api_run_unknown_func(client):
    response = client.post("/api/run", json={"func": "non_existent_func"})
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert "Unknown function" in data["error"]


@pytest.mark.parametrize(
    "func_name,args,expected_result",
    [
        ("is_adult", {"age": 20}, True),
        ("is_adult", 17, False),
        ("celsius_to_fahrenheit", {"celsius": 100}, 212.0),
        ("celsius_to_fahrenheit", 0, 32.0),
        ("count_vowels", {"text": "hello"}, 2),
        ("count_vowels", "world", 1),
        ("invert", {"flag": True}, False),
        ("invert", False, True),
        ("greet", {"name": "Alice"}, "Hello, Alice!"),
        ("greet", None, "Hello, Guest!"),
        ("find_max", {"numbers": [1, 5, 2]}, 5),
        ("find_max", "10, 20, 5", 20),
        ("get_price", {"prices": {"apple": 1.5}, "item": "apple"}, 1.5),
        ("get_price", [{"banana": 0.8}, "banana"], 0.8),
        ("get_price", {"prices": '{"orange": 2.0}', "item": "orange"}, 2.0),
        ("swap", {"pair": [1, 2]}, [2, 1]),
        ("swap", "a, b", ["b", "a"]),
        ("common_items", {"set_a": [1, 2, 3], "set_b": [2, 3, 4]}, [2, 3]),
        ("common_items", [[1, 2], [2, 3]], [2]),
        ("common_items", {"set_a": "1, 2", "set_b": "2, 3"}, ["2"]),
        ("is_leap_year", {"year": 2024}, True),
        ("is_leap_year", 2023, False),
        ("to_int", {"value": "42"}, 42),
        ("to_int", 3.14, 3),
        ("divide", {"a": 10, "b": 2}, 5.0),
        ("divide", [20, 4], 5.0),
        ("power", {"base": 2, "exponent": 3}, 8),
        ("power", [3, 2], 9),
        ("square_root", {"x": 16}, 4.0),
        ("square_root", 25, 5.0),
        ("factorial", {"n": 5}, 120),
        ("factorial", 0, 1),
        ("average", {"numbers": [10, 20, 30]}, 20.0),
        ("average", "5, 15", 10.0),
    ],
)
def test_api_run_success(client, func_name, args, expected_result):
    response = client.post("/api/run", json={"func": func_name, "args": args})
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["result"] == expected_result


@pytest.mark.parametrize(
    "func_name,args,expected_err_type",
    [
        ("is_adult", {"age": -5}, "ValueError"),
        ("divide", {"a": 10, "b": 0}, "ZeroDivisionError"),
        ("square_root", {"x": -4}, "ValueError"),
        ("factorial", {"n": -1}, "ValueError"),
        ("get_price", {"prices": {}, "item": "missing"}, "KeyError"),
        ("swap", {"pair": [1, 2, 3]}, "ValueError"),
        ("find_max", {"numbers": []}, "ValueError"),
        ("average", {"numbers": []}, "ValueError"),
    ],
)
def test_api_run_errors(client, func_name, args, expected_err_type):
    response = client.post("/api/run", json={"func": func_name, "args": args})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error_type"] == expected_err_type
