from pathlib import Path
from joe.core.collector import load_worklets_from_path


def test_load_worklets_from_empty_path():
    """This should return an empty dictionary"""

    worklets = load_worklets_from_path("/tmp/")

    assert len(worklets.items()) == 0, "Did not expect to find any"


def test_load_worklets_from_path():
    """Uses the core package, to have something to load."""

    searchpath = Path(__file__).parent.parent.joinpath("worklets")

    worklets = load_worklets_from_path(searchpath)

    assert len(worklets.items()) == 4, "Failed loading from path"
