from Software.content.api_com import fuse_route

def test_fusion_non_existant() -> None:
    assert fuse_route("hello", "ok") == ""

def test_fusion_room_normal() -> None:
    assert fuse_route("current_room", "") == "/camera//room"

def test_fusion_report_normal() -> None:
    assert fuse_route("report", "") == "/report_auto/"
