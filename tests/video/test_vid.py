from src.video.vid import video


def test_path_empty() -> None:
    assert video("", False) == 84


def test_path_wrong_1() -> None:
    # `asset` instead of `assets`
    assert video("asset/videos/rabbit.mp4", False) == 84


def test_path_wrong_2() -> None:
    # `mp4` instead of `mp3`
    assert video("assets/videos/rabbit.mp3", False) == 84


def test_file_png() -> None:
    # WARNING
    # this should maybe return 84 later
    assert video("assets/pictures/london_walking_pic_00001.png", False) == 0


def test_file_normal() -> None:
    assert video("assets/videos/rabbit.mp4", False) == 0
