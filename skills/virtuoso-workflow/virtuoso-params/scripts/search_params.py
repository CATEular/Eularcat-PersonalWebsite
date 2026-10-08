"""Bounded parameter search through an explicit project evaluation adapter."""
import argparse
import importlib.util
import json
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from itertools import product
from pathlib import Path


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


def domain(spec, label):
    if "values" in spec:
        values = [number(v, label) for v in spec["values"]]
        if not values or len(values) != len(set(values)):
            raise ValueError(f"{label}: values must be nonempty and unique")
        return {"values": values}
    low, high = number(spec["min"], label), number(spec["max"], label)
    if low > high:
        raise ValueError(f"{label}: min exceeds max")
    result = {"min": low, "max": high}
    if "step" in spec:
        step = number(spec["step"], label)
        if step <= 0:
            raise ValueError(f"{label}: step must be positive")
        result["step"] = step
        result["count"] = int((Decimal(str(high)) - Decimal(str(low))) // Decimal(str(step))) + 1
    return result


def snap(value, spec):
    if "values" in spec:
        return min(spec["values"], key=lambda v: abs(v - value))
    value = min(spec["max"], max(spec["min"], value))
    if "step" in spec:
        base, step = Decimal(str(spec["min"])), Decimal(str(spec["step"]))
        index = int(((Decimal(str(value)) - base) / step).to_integral_value(rounding=ROUND_HALF_UP))
        index = min(spec["count"] - 1, max(0, index))
        value = float(base + index * step)
    return value


def prepare(config):
    domains = {name: domain(spec, name) for name, spec in config["parameters"].items()}
    if not domains or set(domains) != set(config["baseline"]):
        raise ValueError("baseline must contain exactly the configured parameters")
    baseline = {}
    for name, spec in domains.items():
        value = number(config["baseline"][name], name)
        legal = snap(value, spec)
        if not math.isclose(value, legal, rel_tol=1e-12, abs_tol=1e-15):
            raise ValueError(f"baseline {name} is outside its legal domain")
        baseline[name] = legal
    objective = config["objective"]
    if objective.get("goal") not in ("min", "max") or not objective.get("metric"):
        raise ValueError("objective needs metric and goal=min|max")
    constraints = config.get("constraints", [])
    for item in constraints:
        if not item.get("metric") or not any(key in item for key in ("min", "max")):
            raise ValueError("constraint needs a metric and a bound")
        for key in ("min", "max"):
            if key in item:
                number(item[key], key)
        if "min" in item and "max" in item and item["min"] > item["max"]:
            raise ValueError("constraint min exceeds max")
        if number(item.get("scale", 1), "constraint scale") <= 0:
            raise ValueError("constraint scale must be positive")
    budget = config.get("max_evals", 20)
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 2:
        raise ValueError("max_evals must be an integer at least 2")
    return domains, baseline, budget


def assess(result, config):
    if not isinstance(result, dict) or result.get("ok") is not True:
        raise ValueError("adapter did not return ok=true")
    metrics = result.get("metrics", {})
    objective = config["objective"]
    cost = number(metrics[objective["metric"]], objective["metric"])
    if objective["goal"] == "max":
        cost = -cost
    violations = []
    for item in config.get("constraints", []):
        value = number(metrics[item["metric"]], item["metric"])
        scale = item.get("scale", 1)
        violation = max(0, item.get("min", value) - value, value - item.get("max", value)) / scale
        violations.append(violation)
    total = sum(violations)
    if not math.isfinite(total):
        raise ValueError("non-finite constraint violation")
    feasible = total == 0
    return (0, cost, 0) if feasible else (1, total, cost), feasible


def search(config, evaluate, output):
    domains, baseline, budget = prepare(config)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / "config.json").write_text(json.dumps(config, indent=2, allow_nan=False), encoding="utf-8")
    rng = random.Random(config.get("seed", 0))
    seen, rows = set(), []
    best, best_rank = None, None
    ledger = output / "evaluations.jsonl"

    def run(params, phase):
        row = {"evaluation": len(rows) + 1, "phase": phase, "parameters": dict(params)}
        run_dir = output / f"run_{row['evaluation']:04d}"
        run_dir.mkdir()
        try:
            result = evaluate(dict(params), run_dir)
            row["result"] = result
            json.dumps(result, allow_nan=False)
            rank, feasible = assess(result, config)
            row.update(valid=True, feasible=feasible, rank=list(rank))
        except Exception as exc:
            row.pop("result", None)
            row.update(valid=False, feasible=False, error=f"{type(exc).__name__}: {exc}")
        rows.append(row)
        with ledger.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
        return row

    def consider(params):
        nonlocal best, best_rank
        key = tuple(params[name] for name in domains)
        if key in seen:
            return
        seen.add(key)
        row = run(params, "baseline" if not rows else "search")
        if row["valid"]:
            rank = tuple(row["rank"])
            if best_rank is None or rank < best_rank:
                best, best_rank = row, rank

    consider(baseline)
    discrete = []
    size = 1
    for spec in domains.values():
        count = len(spec["values"]) if "values" in spec else spec.get("count", 1 if spec["min"] == spec["max"] else 0)
        if count == 0:
            size = 0
            break
        size *= count
    if size and size <= min(10000, budget - 1):
        for spec in domains.values():
            values = spec.get("values")
            if values is None:
                values = [snap(spec["min"] + i * spec.get("step", 1), spec) for i in range(spec.get("count", 1))]
            discrete.append(values)
        candidates = list(product(*discrete))
        rng.shuffle(candidates)
        for values in candidates:
            if len(rows) >= budget - 1:
                break
            consider(dict(zip(domains, values)))
    else:
        attempts = 0
        while len(rows) < budget - 1 and attempts < max(100, budget * 50):
            attempts += 1
            candidate = {}
            for name, spec in domains.items():
                if "values" in spec:
                    value = rng.choice(spec["values"])
                elif attempts % 2 == 0 and best:
                    value = rng.gauss(best["parameters"][name], (spec["max"] - spec["min"]) * 0.15)
                else:
                    value = rng.uniform(spec["min"], spec["max"])
                candidate[name] = snap(value, spec)
            consider(candidate)
    validation = None
    if best and best["feasible"]:
        validation = run(best["parameters"], "independent_validation")
        status = "validated" if validation["valid"] and validation["feasible"] else "validation_failed"
    else:
        status = "no_feasible_candidate" if best else "no_valid_evaluation"
    summary = {"status": status, "method": "bounded_random_local_or_small_discrete_grid",
               "global_optimum_proven": False, "evaluations": len(rows), "budget": budget,
               "baseline": rows[0], "best_search_candidate": best,
               "independent_validation": validation}
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return summary


def load_adapter(path):
    path = Path(path).resolve(strict=True)
    spec = importlib.util.spec_from_file_location("project_evaluation_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, "evaluate", None)):
        raise ValueError("adapter must define evaluate(parameters, run_dir)")
    return module.evaluate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    prepare(config)
    summary = search(config, load_adapter(args.adapter), args.output)
    print(json.dumps({key: summary[key] for key in ("status", "evaluations", "budget")}, indent=2))
    return 0 if summary["status"] == "validated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
