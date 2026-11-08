"""Flask web application providing interactive UI and API for target.py functions."""

import json
import os
from flask import Flask, jsonify, render_template, request
import target

app = Flask(__name__)


def get_commit_sha():
    """Resolve current commit SHA from environment (Render or fallback)."""
    return (
        os.environ.get("RENDER_GIT_COMMIT")
        or os.environ.get("COMMIT_SHA")
        or os.environ.get("GITHUB_SHA")
        or "local-dev"
    )


@app.route("/")
def index():
    """Render interactive web frontend."""
    commit_sha = get_commit_sha()
    return render_template("index.html", commit_sha=commit_sha)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint returning deployment status and commit SHA."""
    return jsonify({
        "status": "ok",
        "commit_sha": get_commit_sha()
    }), 200


@app.route("/api/run", methods=["POST"])
def run_function():
    """Execute a function from target.py with arguments."""
    data = request.get_json(silent=True) or {}
    func_name = data.get("func")

    if not func_name:
        return jsonify({
            "success": False,
            "error_type": "ValueError",
            "error": "Missing 'func' parameter"
        }), 400

    available_functions = {
        "is_adult": target.is_adult,
        "celsius_to_fahrenheit": target.celsius_to_fahrenheit,
        "count_vowels": target.count_vowels,
        "invert": target.invert,
        "greet": target.greet,
        "find_max": target.find_max,
        "get_price": target.get_price,
        "swap": target.swap,
        "common_items": target.common_items,
        "is_leap_year": target.is_leap_year,
        "to_int": target.to_int,
        "divide": target.divide,
        "power": target.power,
        "square_root": target.square_root,
        "factorial": target.factorial,
        "average": target.average,
    }

    if func_name not in available_functions:
        return jsonify({
            "success": False,
            "error_type": "ValueError",
            "error": f"Unknown function '{func_name}'"
        }), 404

    target_func = available_functions[func_name]
    raw_args = data.get("args")

    try:
        # Prepare arguments based on function requirements
        if func_name == "is_adult":
            age = raw_args.get("age") if isinstance(raw_args, dict) else raw_args
            result = target_func(age)

        elif func_name == "celsius_to_fahrenheit":
            celsius = raw_args.get("celsius") if isinstance(raw_args, dict) else raw_args
            result = target_func(celsius)

        elif func_name == "count_vowels":
            text = raw_args.get("text") if isinstance(raw_args, dict) else raw_args
            result = target_func(text)

        elif func_name == "invert":
            flag = raw_args.get("flag") if isinstance(raw_args, dict) else raw_args
            result = target_func(flag)

        elif func_name == "greet":
            name = raw_args.get("name") if isinstance(raw_args, dict) else raw_args
            result = target_func() if name is None and not isinstance(raw_args, dict) else target_func(name)

        elif func_name == "find_max":
            numbers = raw_args.get("numbers") if isinstance(raw_args, dict) else raw_args
            if isinstance(numbers, str):
                numbers = [float(x.strip()) if "." in x else int(x.strip()) for x in numbers.split(",") if x.strip()]
            result = target_func(numbers)

        elif func_name == "get_price":
            if isinstance(raw_args, dict) and "prices" in raw_args:
                prices = raw_args["prices"]
                item = raw_args.get("item", "")
            elif isinstance(raw_args, list) and len(raw_args) == 2:
                prices, item = raw_args[0], raw_args[1]
            else:
                prices, item = {}, ""
            if isinstance(prices, str):
                prices = json.loads(prices)
            result = target_func(prices, item)

        elif func_name == "swap":
            pair = raw_args.get("pair") if isinstance(raw_args, dict) else raw_args
            if isinstance(pair, str):
                pair = [x.strip() for x in pair.split(",") if x.strip()]
            result = list(target_func(pair))

        elif func_name == "common_items":
            if isinstance(raw_args, dict):
                set_a = raw_args.get("set_a", [])
                set_b = raw_args.get("set_b", [])
            elif isinstance(raw_args, list) and len(raw_args) == 2:
                set_a, set_b = raw_args[0], raw_args[1]
            else:
                set_a, set_b = [], []
            if isinstance(set_a, str):
                set_a = [x.strip() for x in set_a.split(",") if x.strip()]
            if isinstance(set_b, str):
                set_b = [x.strip() for x in set_b.split(",") if x.strip()]
            result = sorted(list(target_func(set(set_a), set(set_b))))

        elif func_name == "is_leap_year":
            year = raw_args.get("year") if isinstance(raw_args, dict) else raw_args
            if isinstance(year, (int, str)) and str(year).lstrip("-").isdigit():
                year = int(year)
            result = target_func(year)

        elif func_name == "to_int":
            val = raw_args.get("value") if isinstance(raw_args, dict) else raw_args
            result = target_func(val)

        elif func_name == "divide":
            if isinstance(raw_args, dict):
                a = raw_args.get("a")
                b = raw_args.get("b")
            elif isinstance(raw_args, list) and len(raw_args) == 2:
                a, b = raw_args[0], raw_args[1]
            else:
                a, b = 0, 1
            result = target_func(a, b)

        elif func_name == "power":
            if isinstance(raw_args, dict):
                base = raw_args.get("base")
                exp = raw_args.get("exponent")
            elif isinstance(raw_args, list) and len(raw_args) == 2:
                base, exp = raw_args[0], raw_args[1]
            else:
                base, exp = 1, 1
            result = target_func(base, exp)

        elif func_name == "square_root":
            x = raw_args.get("x") if isinstance(raw_args, dict) else raw_args
            result = target_func(x)

        elif func_name == "factorial":
            n = raw_args.get("n") if isinstance(raw_args, dict) else raw_args
            result = target_func(n)

        elif func_name == "average":
            numbers = raw_args.get("numbers") if isinstance(raw_args, dict) else raw_args
            if isinstance(numbers, str):
                numbers = [float(x.strip()) if "." in x else int(x.strip()) for x in numbers.split(",") if x.strip()]
            result = target_func(numbers)

        return jsonify({
            "success": True,
            "func": func_name,
            "result": result
        }), 200

    except Exception as exc:
        return jsonify({
            "success": False,
            "func": func_name,
            "error_type": type(exc).__name__,
            "error": str(exc)
        }), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
