from pathlib import Path

from joe.core.collector import (
    collect_resources,
    load_worklets_from_packages,
    load_worklets_from_path,
)


def test_resource_collection():
    """Check that the expected amount of paths are found"""

    resources = collect_resources()

    assert len(resources["configs"]) == 2

    assert len(resources["templates"]) == 1

    assert len(resources["testfiles"]) == 1


def test_load_worklets_from_empty_path():
    """This should return an empty dictionary"""

    worklets = load_worklets_from_path("/tmp/")

    assert len(worklets.items()) == 0, "Did not expect to find any"


def test_load_worklets_from_path():
    """Uses the core package, to have something to load."""

    searchpath = Path(__file__).parent.parent.joinpath("worklets")

    worklets = load_worklets_from_path(searchpath)

    assert len(worklets.items()) == 4, "Failed loading from path"


def test_load_worklets_from_packages():

    worklets = load_worklets_from_packages("joe.core")

    assert len(worklets.items()) == 4, "Failed loading from packages"


def test_compare_from_path_with_from_package():
    """This is just to give hint to whether it is 'from_path' or 'from_packages'"""

    searchpath = Path(__file__).parent.parent.joinpath("worklets")

    worklets_from_path = load_worklets_from_path(searchpath)
    worklets_from_packages = load_worklets_from_packages("joe.core")

    assert len(worklets_from_path) == len(worklets_from_packages)
