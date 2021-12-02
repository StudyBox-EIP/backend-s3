from sys import stderr
from src.addons.arguments import parse_arguments, treat_arguments
import pytest


def test_parse_empty() -> None:
    with pytest.raises(SystemExit) as exc:
        parse_arguments([])
    assert exc.value.code == 2


def test_parse_flag_type_wrong() -> None:
    with pytest.raises(SystemExit) as exc:
        parse_arguments(["nop"])
    assert exc.value.code == 2


def test_parse_flag_file_empty() -> None:
    with pytest.raises(SystemExit) as exc:
        parse_arguments(["vid", "-f"])
    assert exc.value.code == 2


def test_parse_normal() -> None:
    elm = parse_arguments(["vid", "-f", "assets/videos/rabbit.mp4"])
    assert elm == ("vid", "assets/videos/rabbit.mp4", "https://api.studybox.fr")
    elm = parse_arguments(["img"])
    assert elm == ("img", "assets/videos/rabbit.mp4", "https://api.studybox.fr")
    elm = parse_arguments(["cam"])
    assert elm == ("cam", "assets/videos/rabbit.mp4", "https://api.studybox.fr")


def test_treat_empty() -> None:
    with pytest.raises(SystemExit) as exc:
        treat_arguments([])
    assert exc.value.code == 2


def test_treat_flag_type_wrong() -> None:
    with pytest.raises(SystemExit) as exc:
        treat_arguments(["nop"])
    assert exc.value.code == 2


def test_treat_flag_file_empty() -> None:
    with pytest.raises(SystemExit) as exc:
        treat_arguments(["./Camera", "vid", "-f"])
    assert exc.value.code == 2


def test_treat_flag_file_wrong() -> None:
    with pytest.raises(SystemExit) as exc:
        treat_arguments(["./Camera", "vid", "-f", "nop"])
    assert exc.value.code == 84


def test_treat_flag_file_wrong_type() -> None:
    with pytest.raises(SystemExit) as exc:
        treat_arguments(["./Camera", "vid", "-f", "README.md"])
    assert exc.value.code == 84


def test_treat_normal() -> None:
    elm = treat_arguments(["./Camera", "vid", "-f", "assets/videos/rabbit.mp4"])
    assert elm == ("vid", "assets/videos/rabbit.mp4", "https://api.studybox.fr")
    elm = treat_arguments(["./Camera", "img"])
    assert elm == ("img", "assets/videos/rabbit.mp4", "https://api.studybox.fr")
    elm = treat_arguments(["./Camera", "cam"])
    assert elm == ("cam", "assets/videos/rabbit.mp4", "https://api.studybox.fr")
