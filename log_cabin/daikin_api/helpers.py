from typing import Dict, Any, Optional

def parse_string_response(s: str) -> Dict[str, str]:
    d = dict([pair.split("=") for pair in s.split(",")])
    if d.pop("ret", None) == "OK":
        return d
    print(f"Invalid response: {s}")
    return dict()

def pretty_dict(d: Dict[Any, Any], keys: bool = True, vals: bool = True) -> str:
    return "\n".join(f"{k + ': ' if keys else ''}{v if vals else ''}" for k, v in d.items())

def as_float(s: str) -> Optional[float]:
    try:
        return float(s)
    except(ValueError, TypeError):
        return None