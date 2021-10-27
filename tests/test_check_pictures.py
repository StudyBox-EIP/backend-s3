from src.check_pictures import check_pedestrian


def test_pictures_normal() -> None:
    assert check_pedestrian(50) == 0
