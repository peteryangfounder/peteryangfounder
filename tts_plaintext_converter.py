#!/usr/bin/env python3
"""Convert LaTeX-heavy text into pronounceable plain English."""

from __future__ import annotations

import re
import sys
from typing import Tuple

# ------------------------ Utilities: numbers to words ------------------------

_UNDER_20 = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
_TENS = [
    "",
    "ten",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]
_SCALES = [(10**9, "billion"), (10**6, "million"), (1000, "thousand"), (100, "hundred")]


def int_to_words(n: int) -> str:
    if n < 0:
        return "minus " + int_to_words(-n)
    if n < 20:
        return _UNDER_20[n]
    if n < 100:
        if n % 10 == 0:
            return _TENS[n // 10]
        return _TENS[n // 10] + " " + _UNDER_20[n % 10]
    for scale, name in _SCALES:
        if n >= scale:
            head = n // scale
            tail = n % scale
            if tail == 0:
                return int_to_words(head) + " " + name
            return int_to_words(head) + " " + name + " " + int_to_words(tail)
    return str(n)


_DIGIT_WORD = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}


def digits_to_words(text: str) -> str:
    text = re.sub(
        r"(?<![A-Za-z0-9])\d+(?![A-Za-z0-9])",
        lambda m: int_to_words(int(m.group())),
        text,
    )

    def replace_alnum(match: re.Match[str]) -> str:
        prefix = match.group(1)
        digits = match.group(2)
        suffix = match.group(3)
        phrase = int_to_words(int(digits))
        result = []
        if prefix:
            result.append(prefix)
            if prefix[-1].isalpha():
                result.append(" ")
        result.append(phrase)
        if suffix:
            result.append(" ")
            result.append(suffix)
        return "".join(result)

    text = re.sub(r"([A-Za-z])?(\d+)([A-Za-z])", replace_alnum, text)

    def replace_digit(match: re.Match[str]) -> str:
        return " " + _DIGIT_WORD[match.group()] + " "

    text = re.sub(r"\d", replace_digit, text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------------------- Symbol dictionaries ---------------------------

GREEK = {
    "alpha": "alpha",
    "beta": "beta",
    "gamma": "gamma",
    "delta": "delta",
    "epsilon": "epsilon",
    "zeta": "zeta",
    "eta": "eta",
    "theta": "theta",
    "iota": "iota",
    "kappa": "kappa",
    "lambda": "lambda",
    "mu": "mu",
    "nu": "nu",
    "xi": "xi",
    "omicron": "omicron",
    "pi": "pi",
    "rho": "rho",
    "sigma": "sigma",
    "tau": "tau",
    "upsilon": "upsilon",
    "phi": "phi",
    "chi": "chi",
    "psi": "psi",
    "omega": "omega",
    "varepsilon": "epsilon",
    "vartheta": "theta",
    "varpi": "pi",
    "varrho": "rho",
    "varsigma": "sigma",
    "varphi": "phi",
}


UPPER_GREEK = {
    "Alpha": "alpha",
    "Beta": "beta",
    "Gamma": "gamma",
    "Delta": "delta",
    "Epsilon": "epsilon",
    "Zeta": "zeta",
    "Eta": "eta",
    "Theta": "theta",
    "Iota": "iota",
    "Kappa": "kappa",
    "Lambda": "lambda",
    "Mu": "mu",
    "Nu": "nu",
    "Xi": "xi",
    "Omicron": "omicron",
    "Pi": "pi",
    "Rho": "rho",
    "Sigma": "sigma",
    "Tau": "tau",
    "Upsilon": "upsilon",
    "Phi": "phi",
    "Chi": "chi",
    "Psi": "psi",
    "Omega": "omega",
}


UNICODE_SYMBOLS = {
    "≤": " less than or equal to ",
    "≥": " greater than or equal to ",
    "≠": " not equal to ",
    "≈": " approximately equal to ",
    "∈": " is an element of ",
    "∉": " is not an element of ",
    "⊂": " proper subset of ",
    "⊆": " subset or equal to ",
    "⊃": " proper superset of ",
    "⊇": " superset or equal to ",
    "∪": " union ",
    "∩": " intersection ",
    "→": " to ",
    "↦": " maps to ",
    "⇒": " implies ",
    "⇔": " if and only if ",
    "∀": " for all ",
    "∃": " there exists ",
    "∑": " sum ",
    "∏": " product ",
    "√": " square root of ",
    "∞": " infinity ",
    "±": " plus or minus ",
    "∂": " partial ",
    "·": " times ",
    "×": " times ",
    "÷": " divided by ",
    "|": " absolute value bars ",
    "‖": " norm ",
}


TEX_SIMPLE = {
    r"\langle": " angle ",
    r"\rangle": " angle ",
    r"\le": " less than or equal to ",
    r"\ge": " greater than or equal to ",
    r"\neq": " not equal to ",
    r"\approx": " approximately equal to ",
    r"\in": " is an element of ",
    r"\notin": " is not an element of ",
    r"\subset": " proper subset of ",
    r"\subseteq": " subset or equal to ",
    r"\supset": " proper superset of ",
    r"\supseteq": " superset or equal to ",
    r"\cup": " union ",
    r"\cap": " intersection ",
    r"\to": " to ",
    r"\rightarrow": " to ",
    r"\mapsto": " maps to ",
    r"\implies": " implies ",
    r"\iff": " if and only if ",
    r"\forall": " for all ",
    r"\exists": " there exists ",
    r"\cdot": " times ",
    r"\times": " times ",
    r"\pm": " plus or minus ",
    r"\mp": " minus or plus ",
    r"\ldots": " dot dot dot ",
    r"\cdots": " dot dot dot ",
    r"\infty": " infinity ",
    r"\partial": " partial ",
    r"\nabla": " nabla ",
    r"\propto": " proportional to ",
    r"\angle": " angle ",
    r"\triangle": " triangle ",
    r"\Vert": " norm ",
    r"\|": " norm ",
}


FUNCTIONS = {
    "sin": "sine of ",
    "cos": "cosine of ",
    "tan": "tangent of ",
    "csc": "cosecant of ",
    "sec": "secant of ",
    "cot": "cotangent of ",
    "arcsin": "arc sine of ",
    "arccos": "arc cosine of ",
    "arctan": "arc tangent of ",
    "sinh": "hyperbolic sine of ",
    "cosh": "hyperbolic cosine of ",
    "tanh": "hyperbolic tangent of ",
    "log": "logarithm of ",
    "ln": "natural logarithm of ",
    "exp": "exponential of ",
    "max": "maximum of ",
    "min": "minimum of ",
    "det": "determinant of ",
    "dim": "dimension of ",
    "rank": "rank of ",
}


BLACKBOARD = {
    r"\mathbb{R}": " R ",
    r"\mathbb{N}": "natural numbers",
    r"\mathbb{Z}": "integers",
    r"\mathbb{Q}": "rational numbers",
    r"\mathbb{C}": "complex numbers",
}


# -------------------------- Group extraction helpers ------------------------


def _skip_spaces(s: str, i: int) -> int:
    while i < len(s) and s[i].isspace():
        i += 1
    return i


def _read_group(s: str, i: int) -> Tuple[str, int]:
    i = _skip_spaces(s, i)
    if i >= len(s):
        return "", i
    ch = s[i]
    if ch == "{":
        depth = 0
        j = i
        while j < len(s):
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    return s[i + 1 : j], j + 1
            j += 1
        return s[i + 1 :], len(s)
    if ch == "\\":
        j = i + 1
        while j < len(s) and s[j].isalpha():
            j += 1
        cmd = s[i:j]
        k = j
        if k < len(s) and s[k] == "{":
            group, k = _read_group(s, k)
            return cmd + "{" + group + "}", k
        return cmd, j
    return s[i], i + 1


# --------------------------- Core TeX processors ----------------------------


def _process_frac(s: str, i: int) -> Tuple[str, int]:
    num, k = _read_group(s, i)
    den, j = _read_group(s, k)
    return f"{tex_to_words(num)} over {tex_to_words(den)}", j


def _process_sqrt(s: str, i: int) -> Tuple[str, int]:
    idx = ""
    if i < len(s) and s[i] == "[":
        j = i + 1
        depth = 1
        while j < len(s) and depth > 0:
            if s[j] == "[":
                depth += 1
            elif s[j] == "]":
                depth -= 1
                if depth == 0:
                    idx = s[i + 1 : j]
                    i = j + 1
                    break
            j += 1
    rad, j = _read_group(s, i)
    if idx:
        return f"{tex_to_words(idx)} th root of {tex_to_words(rad)}", j
    return f"square root of {tex_to_words(rad)}", j


def _process_sum_or_prod(name: str, s: str, i: int) -> Tuple[str, int]:
    lower = upper = ""
    i = _skip_spaces(s, i)
    if i < len(s) and s[i] == "_":
        lower, i = _read_group(s, i + 1)
    i = _skip_spaces(s, i)
    if i < len(s) and s[i] == "^":
        upper, i = _read_group(s, i + 1)
    word = "sum" if name == "sum" else "product"
    out = word
    if lower or upper:
        lo = tex_to_words(lower) if lower else ""
        up = tex_to_words(upper) if upper else ""
        if lower and upper:
            out += f" from {lo} to {up}"
        elif lower:
            out += f" with lower limit {lo}"
        elif upper:
            out += f" with upper limit {up}"
    return out, i


def _process_integral(s: str, i: int) -> Tuple[str, int]:
    lower = upper = ""
    i = _skip_spaces(s, i)
    if i < len(s) and s[i] == "_":
        lower, i = _read_group(s, i + 1)
    i = _skip_spaces(s, i)
    if i < len(s) and s[i] == "^":
        upper, i = _read_group(s, i + 1)
    prefix = "integral"
    if lower or upper:
        lo = tex_to_words(lower) if lower else ""
        up = tex_to_words(upper) if upper else ""
        if lower and upper:
            prefix = f"integral from {lo} to {up}"
        elif lower:
            prefix = f"integral with lower limit {lo}"
        elif upper:
            prefix = f"integral with upper limit {up}"
    return prefix, i


def _process_binom(s: str, i: int) -> Tuple[str, int]:
    a, k = _read_group(s, i)
    b, j = _read_group(s, k)
    return f"binomial of {tex_to_words(a)} and {tex_to_words(b)}", j


def _process_lim(s: str, i: int) -> Tuple[str, int]:
    sub = ""
    i = _skip_spaces(s, i)
    if i < len(s) and s[i] == "_":
        sub, i = _read_group(s, i + 1)
    if sub:
        return f"limit as {tex_to_words(sub)} of", i
    return "limit of", i


def _process_matrix(env: str, body: str) -> str:
    body = body.strip()
    rows = []
    if body:
        raw_rows = [r for r in re.split(r"\\", body) if r.strip()]
        for raw in raw_rows:
            cols = [c.strip() for c in raw.split("&") if c.strip()]
            rows.append(cols)
    m = len(rows)
    n = max((len(r) for r in rows), default=0)
    row_word = int_to_words(m)
    col_word = int_to_words(n)
    row_label = "row" if m == 1 else "rows"
    col_label = "column" if n == 1 else "columns"
    parts = [f"matrix with {row_word} {row_label} and {col_word} {col_label}"]
    for idx, r in enumerate(rows, start=1):
        entries = [tex_to_words(c) for c in r]
        row_phrase = f"row {int_to_words(idx)} entries are " + ", ".join(entries)
        parts.append(row_phrase)
    return ". ".join(parts)


def _process_projection(name: str, s: str, i: int) -> Tuple[str, int]:
    target = ""
    i = _skip_spaces(s, i)
    if i < len(s) and s[i] == "_":
        target, i = _read_group(s, i + 1)
    i = _skip_spaces(s, i)
    arg, i = _read_group(s, i)
    subject = tex_to_words(arg) if arg else ""
    onto = tex_to_words(target) if target else ""
    if name == "proj":
        if onto:
            return f"projection of {subject} onto {onto}", i
        return f"projection of {subject}", i
    if onto and subject:
        return f"perpendicular of {onto} onto {subject}", i
    if onto:
        return f"perpendicular of {onto}", i
    return f"perpendicular of {subject}", i


# ------------------------------ Main TeX walker -----------------------------


def tex_to_words(s: str) -> str:
    s = re.sub(r"([A-Za-z]+)\s*\*\s*(\{)", r"\1_\2", s)
    s = re.sub(r"([A-Za-z\}])\s*\*\s*([0-9A-Za-z])", r"\1_{\{\2\}}", s)
    s = re.sub(r"([A-Za-z]+)\s*\*\s*(\{)", r"\1_\2", s)
    s = re.sub(r"(min|max)\*\s*\{", r"\1_{", s)

    s = s.replace(r"\|", " norm ")
    for sym, word in UNICODE_SYMBOLS.items():
        s = s.replace(sym, word)

    s = s.replace(r"\,", " ").replace(r"\;", " ").replace(r"\:", " ").replace(r"\!", " ")

    for k, v in BLACKBOARD.items():
        s = s.replace(k, v)

    def text_repl(match: re.Match[str]) -> str:
        content = match.group(1)
        lowered = content.strip().lower()
        if lowered in {"proj", "perp"}:
            return "\\" + lowered
        return content

    def operator_repl(match: re.Match[str]) -> str:
        content = match.group(1)
        lowered = content.strip().lower()
        if lowered in {"proj", "perp"}:
            return "\\" + lowered
        return content

    s = re.sub(r"\\text\s*\{([^{}]*)\}", text_repl, s)
    s = re.sub(r"\\operatorname\s*\{([^{}]*)\}", operator_repl, s)

    s = re.sub(r"([A-Za-z]+)\s*\*\s*(\{)", r"\1_\2", s)
    s = re.sub(r"([A-Za-z\}])\s*\*\s*([0-9A-Za-z])", r"\1_{\{\2\}}", s)
    s = re.sub(r"([A-Za-z]+)\s*\*\s*(\{)", r"\1_\2", s)

    s = re.sub(r"\bdiag\s*\(([^()]*)\)", lambda m: "diagonal of " + m.group(1), s)
    s = re.sub(r"\bcol\s*\(([^()]*)\)", lambda m: "column space of " + m.group(1), s)
    s = re.sub(r"\b[Ss]pan\s*\{([^{}]*)\}", lambda m: "span of " + m.group(1), s)

    s = re.sub(r"\b([A-Za-z])\s*\(\s*([A-Za-z])\s*\)", r"\1 of \2", s)

    s = re.sub(r"\bI\s*_\s*\{?\s*([A-Za-z0-9]+)\s*\}?", r"identity_{\{\1\}}", s)

    s = re.sub(r"(?<!\\)\bproj\b", r"\\proj", s)
    s = re.sub(r"(?<!\\)\bperp\b", r"\\perp", s)

    def env_repl(m: re.Match[str]) -> str:
        env = m.group(1)
        body = m.group(2)
        if "matrix" in env:
            return _process_matrix(env, body)
        if "cases" in env:
            items = [seg.strip() for seg in re.split(r"\\", body) if seg.strip()]
            items_words = [tex_to_words(seg.replace("&", " when ")) for seg in items]
            return "cases " + ". ".join(items_words)
        return tex_to_words(body)

    s = re.sub(r"\\begin\{([a-zA-Z*]+)\}(.+?)\\end\{\1\}", env_repl, s, flags=re.DOTALL)

    for k, v in TEX_SIMPLE.items():
        name = k[1:] if k.startswith("\\") else k
        s = re.sub(r"\\" + re.escape(name) + r"(?![A-Za-z])", v, s)

    for g in sorted(GREEK.keys(), key=len, reverse=True):
        s = re.sub(r"\\" + re.escape(g) + r"(?![A-Za-z])", " " + GREEK[g] + " ", s)
    for g in sorted(UPPER_GREEK.keys(), key=len, reverse=True):
        s = re.sub(r"\\" + re.escape(g) + r"(?![A-Za-z])", " " + UPPER_GREEK[g] + " ", s)

    s = s.replace(r"\left", " ").replace(r"\right", " ")

    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\":
            j = i + 1
            while j < len(s) and s[j].isalpha():
                j += 1
            cmd = s[i + 1 : j]
            i = j
            if cmd == "frac":
                phrase, i = _process_frac(s, i)
                out.append(phrase)
                continue
            if cmd == "sqrt":
                phrase, i = _process_sqrt(s, i)
                out.append(phrase)
                continue
            if cmd in ("sum", "prod"):
                phrase, i = _process_sum_or_prod(cmd, s, i)
                out.append(phrase + " ")
                continue
            if cmd == "int":
                phrase, i = _process_integral(s, i)
                out.append(phrase + " ")
                continue
            if cmd == "binom":
                phrase, i = _process_binom(s, i)
                out.append(phrase)
                continue
            if cmd == "lim":
                phrase, i = _process_lim(s, i)
                out.append(phrase + " ")
                continue
            if cmd in ("mathbf", "boldsymbol", "bm", "vec"):
                arg, i = _read_group(s, i)
                out.append("vector " + tex_to_words(arg))
                continue
            if cmd in ("overline", "bar"):
                arg, i = _read_group(s, i)
                out.append("conjugate of " + tex_to_words(arg))
                continue
            if cmd in ("hat", "widehat"):
                arg, i = _read_group(s, i)
                out.append("hat " + tex_to_words(arg))
                continue
            if cmd == "proj":
                phrase, i = _process_projection("proj", s, i)
                out.append(phrase)
                continue
            if cmd == "perp":
                lookahead = _skip_spaces(s, i)
                if lookahead < len(s) and s[lookahead] == "_":
                    phrase, i = _process_projection("perp", s, i)
                    out.append(phrase)
                else:
                    out.append(" perpendicular to ")
                continue
            if cmd in ("dot", "ddot"):
                arg, i = _read_group(s, i)
                descriptor = "time derivative of " if cmd == "dot" else "second time derivative of "
                out.append(descriptor + tex_to_words(arg))
                continue
            continue
        if ch == "^":
            content, i = _read_group(s, i + 1)
            raw = content.strip()
            words = tex_to_words(content).strip()
            if raw in ("\\top", "top", "T"):
                out.append(" transposed")
            elif raw in ("2", "two"):
                out.append(" squared")
            elif raw in ("3", "three"):
                out.append(" cubed")
            elif words.strip() == "minus one":
                out.append(" inverse")
            else:
                out.append(" to the power " + words)
            continue
        if ch == "_":
            content, i = _read_group(s, i + 1)
            words = tex_to_words(content)
            out.append(" sub " + words)
            continue
        if ch in "()[]{}":
            out.append(" ")
            i += 1
            continue
        if ch == "+":
            out.append(" plus ")
            i += 1
            continue
        if ch == "-":
            out.append(" minus ")
            i += 1
            continue
        if ch == "*":
            out.append(" times ")
            i += 1
            continue
        if ch == "/":
            out.append(" divided by ")
            i += 1
            continue
        if ch == "=":
            out.append(" equals ")
            i += 1
            continue
        if ch == "<":
            out.append(" less than ")
            i += 1
            continue
        if ch == ">":
            out.append(" greater than ")
            i += 1
            continue
        if ch == ",":
            out.append(", ")
            i += 1
            continue
        if ch == ".":
            out.append(".")
            i += 1
            continue
        out.append(ch)
        i += 1

    text = "".join(out)

    text = re.sub(r"\bd\s*([A-Za-z])\b", lambda m: "with respect to " + m.group(1), text)
    text = re.sub(
        r"\bpartial\s*([A-Za-z])\b",
        lambda m: "partial with respect to " + m.group(1),
        text,
    )

    text = text.replace(" to the power minus one", " inverse")
    text = re.sub(r"angle\s+(.+?)\s*,\s*(.+?)\s+angle", r"inner product of \1 and \2", text)
    text = re.sub(r"\bvec\b", "vector", text, flags=re.IGNORECASE)
    text = re.sub(r"\bnorm\s+([^\.,]+?)\s+norm\b", r"norm of \1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ----------------------------- Expression pass ------------------------------


def convert_math_and_text(source: str) -> str:
    s = source
    s = re.sub(r"\\operatorname\s*\{([^{}]*)\}", lambda m: "\\" + m.group(1), s)
    s = re.sub(r"([A-Za-z]+)\s*\*\s*(\{)", r"\1_\2", s)
    s = re.sub(r"([A-Za-z\}])\s*\*\s*([0-9A-Za-z])", r"\1_{\{\2\}}", s)
    s = re.sub(r"([A-Za-z]+)\s*\*\s*(\{)", r"\1_\2", s)
    s = re.sub(r"(min|max)\*\s*\{", r"\1_{", s)
    s = re.sub(r"(\d)\s*!\s*:\s*!\s*([A-Za-z0-9])", r"\1 to \2", s)

    def dollar_repl(m: re.Match[str]) -> str:
        return " " + tex_to_words(m.group(1)) + " "

    s = re.sub(r"\$\$(.+?)\$\$", dollar_repl, s, flags=re.DOTALL)
    s = re.sub(r"\$(.+?)\$", dollar_repl, s, flags=re.DOTALL)
    s = re.sub(r"\\\((.+?)\\\)", dollar_repl, s, flags=re.DOTALL)
    s = re.sub(r"\\\[(.+?)\\\]", dollar_repl, s, flags=re.DOTALL)

    text = tex_to_words(s)
    text = digits_to_words(text)

    tokens = text.split(" ")
    allowed_letters = {"a", "i", "j"}.union(GREEK.values())
    special_letters = {"R"}
    for idx, tok in enumerate(tokens):
        if re.fullmatch(r"[A-Za-z]", tok):
            if tok in special_letters:
                continue
            if tok.lower() in allowed_letters:
                continue
            tokens[idx] = '"' + tok.lower() + '"'
        else:
            tokens[idx] = tok
    text = " ".join(tokens)

    text = re.sub(r"[^A-Za-z\.\,\"\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ------------------------------ Command-line I/O ----------------------------


def main() -> None:
    if len(sys.argv) > 1:
        source = " ".join(sys.argv[1:])
    else:
        source = sys.stdin.read()
    output = convert_math_and_text(source)
    sys.stdout.write(output + ("\n" if not output.endswith("\n") else ""))


if __name__ == "__main__":
    main()

