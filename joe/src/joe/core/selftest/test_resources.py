from pathlib import Path
import joe.core
from joe.core.resources import Collector


def test_resource_collection():
    """Check that the expected amount of paths are found"""

    collector = Collector()
    collector.collect()

    assert len(collector.resources["configs"]) == 2

    assert len(collector.resources["templates"]) == 1

    assert len(collector.resources["testfiles"]) == 1


def test_collect_from_empty_path():
    """This should return an empty dictionary"""

    collector = Collector()
    collector.collect_from_path("/tmp")

    assert len(collector.resources["worklets"]) == 0, "Did not expect to find any"


def test_collect_worklets_from_path():
    """Uses the core package, to have something to collect."""

    collector = Collector()
    collector.collect_from_path(Path(__file__).parent.parent.joinpath("worklets"))

    assert len(collector.resources["worklets"]) == 4, "Failed collecting from path"


def test_collect_from_packages():

    collector = Collector()
    collector.collect_from_packages(joe.core.__path__, joe.core.__name__ + ".")

    assert len(collector.resources["worklets"]) == 4, "Failed collecting from packages"


def test_compare_from_path_with_from_package():
    """This is just to give hint to whether it is 'from_path' or 'from_packages'"""

    collector_path = Collector()
    collector_path.collect_from_path(Path(__file__).parent.parent.joinpath("worklets"))

    collector_pkgs = Collector()
    collector_pkgs.collect_from_packages(joe.core.__path__, joe.core.__name__ + ".")

    assert len(collector_path.resources["worklets"]) == len(
        collector_pkgs.resources["worklets"]
    )
