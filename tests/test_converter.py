import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tts_plaintext_converter.py"


def run_converter(text: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), text],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_membership_phrase() -> None:
    output = run_converter(
        "For \\mathbf{u}, \\mathbf{v} \\in \\mathbb{R}^n with \\mathbf{v} \\neq \\mathbf{0}."
    )
    assert "vector \"v\" is an element of R to the power \"n\"" in output
    assert "vector \"v\" not equal to vector zero" in output


def test_alpha_membership() -> None:
    output = run_converter(
        "This is the unique vector on the line \\alpha \\mathbf{v}. \\alpha \\in \\mathbb{R}."
    )
    assert "alpha is an element of R" in output


def test_projection_phrase() -> None:
    output = run_converter("\\operatorname{proj}_{\\mathbf{v}} \\mathbf{u}")
    assert "projection of vector \"u\" onto vector" in output
    assert " proj" not in output
    assert "proj_" not in output


def test_projection_without_subscript() -> None:
    output = run_converter("\\operatorname{proj} \\mathbf{u}")
    assert output == "projection of vector \"u\""


def test_projection_parentheses() -> None:
    output = run_converter("\\operatorname{proj}_{\\mathbf{v}}(\\mathbf{u})")
    assert "projection of vector \"u\" onto vector \"v\"" in output


def test_perpendicular_phrase() -> None:
    output = run_converter("\\operatorname{perp}_{\\mathbf{v}} \\mathbf{u}")
    assert "perpendicular of vector \"u\" onto vector \"v\"" in output


def test_perpendicular_without_subscript() -> None:
    output = run_converter("\\perp \\mathbf{u}")
    assert output == "perpendicular to vector \"u\""


def test_norm_word() -> None:
    output = run_converter("The length is \\|x\\|.")
    assert "norm of \"x\"" in output
    assert "absolute value" not in output


def test_norm_literal_bars() -> None:
    output = run_converter("||v||^2")
    assert "norm of \"v\" squared" in output


def test_matrix_dimensions() -> None:
    output = run_converter("\\begin{bmatrix}1 & 2 \\ 3 & 4\\end{bmatrix}")
    assert "matrix with two rows and two columns" in output


def test_matrix_entries() -> None:
    output = run_converter("\\begin{bmatrix}1 & 2\\end{bmatrix}")
    assert "row one entries are one, two" in output


def test_imaginary_spacing() -> None:
    output = run_converter("z = 2i + 5i.")
    assert "two i" in output
    assert "five i" in output
    assert "twoi" not in output


def test_digits_with_adjacent_letters() -> None:
    output = run_converter("5x + 10y")
    assert "five \"x\" plus ten \"y\"" in output


def test_vec_command_replaced() -> None:
    output = run_converter("\\vec{i} + \\mathbf{j}")
    assert "vector i" in output
    assert "vec" not in output.lower().split()


def test_mathbb_r_power() -> None:
    output = run_converter("\\mathbb{R}^3")
    assert output == "R cubed"


def test_notin_phrase() -> None:
    output = run_converter("x \\notin A")
    assert output == "\"x\" is not an element of A"


def test_cases_environment() -> None:
    output = run_converter("\\begin{cases}x & a \\ y & b\\end{cases}")
    assert "cases \"x\" when a." in output
    assert "\"y\" when \"b\"" in output


def test_sum_limits() -> None:
    output = run_converter("\\sum_{i=0}^{n} a_i")
    assert "sum from i equals zero to \"n\"" in output


def test_integral_limits() -> None:
    output = run_converter("\\int_{0}^{1} f(x) dx")
    assert "integral from zero to one" in output
    assert "with respect to \"x\"" in output


def test_binomial_phrase() -> None:
    output = run_converter("\\binom{n}{k}")
    assert output == "binomial of \"n\" and \"k\""


def test_dot_operator_translation() -> None:
    output = run_converter("\\dot{x}")
    assert output == "time derivative of \"x\""


def test_plain_variable_is_quoted() -> None:
    output = run_converter("x")
    assert output == "\"x\""


def test_cdot_spacing() -> None:
    output = run_converter("C \\cdot D")
    assert output == "\"c\" times \"d\""
    assert "cdot" not in output
