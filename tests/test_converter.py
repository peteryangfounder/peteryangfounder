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


def test_membership_phrase():
    output = run_converter("For \\mathbf{u}, \\mathbf{v} \\in \\mathbb{R}^n with \\mathbf{v} \\neq \\mathbf{0}.")
    assert "vector \"v\" is an element of R to the power \"n\"" in output
    assert "vector \"v\" not equal to vector zero" in output


def test_alpha_membership():
    output = run_converter("This is the unique vector on the line \\alpha \\mathbf{v}. \\alpha \\in \\mathbb{R}.")
    assert "alpha is an element of R" in output


def test_projection_phrase():
    output = run_converter("The projection is \\operatorname{proj}_{\\mathbf{v}} \\mathbf{u}.")
    assert "projection of vector \"u\" onto vector v" in output


def test_norm_word():
    output = run_converter("The length is \\|x\\|.")
    assert "norm of \"x\"" in output
    assert "absolute value" not in output


def test_matrix_dimensions():
    output = run_converter("\\begin{bmatrix}1 & 2 \\ 3 & 4\\end{bmatrix}")
    assert "two rows" in output
    assert "two columns" in output


def test_imaginary_spacing():
    output = run_converter("z = 2i + 5i.")
    assert "two i" in output
    assert "five i" in output
    assert "twoi" not in output


def test_perpendicular_phrase():
    output = run_converter("\\operatorname{perp}_{\\mathbf{u}} \\mathbf{v}")
    assert "perpendicular of vector \"u\" onto vector \"v\"" in output

