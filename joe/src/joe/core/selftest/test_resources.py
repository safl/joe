from pathlib import Path
import joe.core
from joe.core.resources import Collection


def test_resource_collection():
    """Check that the expected amount of paths are found"""

    col = Collection()
    col.collect()

    assert len(col.resources["configs"]) == 2

    assert len(col.resources["templates"]) == 1

    assert len(col.resources["testfiles"]) == 1


def test_collect_worklets_from_empty_path():
    """This should return an empty dictionary"""

    col = Collection()
    col.collect_worklets_from_path("/tmp")

    assert len(col.resources["worklets"]) == 0, "Did not expect to find any"


def test_collect_worklets_from_path():
    """Uses the core package, to have something to collect."""

    col = Collection()
    col.collect_worklets_from_path(Path(__file__).parent.parent.joinpath("worklets"))

    assert len(col.resources["worklets"]) == 4, "Failed collecting from path"


def test_collect_worklets_from_packages():

    col = Collection()
    col.collect_from_packages(joe.core.__path__, joe.core.__name__ + ".")

    assert len(col.resources["worklets"]) == 4, "Failed collecting from packages"


def test_compare_from_path_with_from_package():
    """This is just to give hint to whether it is 'from_path' or 'from_packages'"""

    col_path = Collection()
    col_path.collect_worklets_from_path(
        Path(__file__).parent.parent.joinpath("worklets")
    )

    col_pkgs = Collection()
    col_pkgs.collect_from_packages(joe.core.__path__, joe.core.__name__ + ".")

    assert len(col_path.resources["worklets"]) == len(col_pkgs.resources["worklets"])
