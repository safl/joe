from joe.core.resources import Resource, Config, Worklet


class Collector(object):
    """Collects resources from installed packages and the current working directory"""

    RESOURCES = [
        ("configs", Config.SUFFIX),
        ("perf_reqs", ".perfreq"),
        ("templates", ".html"),
        ("workflows", ".workflow"),
        ("worklets", Worklet.SUFFIX),
        ("auxilary", ".*"),
    ]
    IGNORE = ["__init__.py", "__pycache__", "setup.py"]

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Collector, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.resources = {category: {} for category, _ in Collector.RESOURCES}
        self.is_done = False

    def __process_candidate(self, candidate: Path, category: str, pkg):
        """Inserts the given candidate"""

        if category == "worklets":
            resource = Worklet(candidate, pkg)
            resource.content_from_file()

            if not resource.content_has_worklet_func():
                category = "auxilary"
        else:
            resource = Resource(candidate, pkg)

        self.resources[category][resource.ident] = resource

    def collect_from_path(self, path=None, max_depth=2):
        """Collects non-packaged worklets from the given 'path'"""

        path = Path(path).resolve() if path else Path.cwd().resolve()

        base = len(str(path).split(os.sep))

        for candidate in list(path.glob("*")) + list(path.glob("*/*")):
            level = len(str(candidate).split(os.sep))
            if max_depth and level > base + max_depth:
                continue

            for category, suffix in Collector.RESOURCES:
                if candidate.name in Collector.IGNORE:
                    continue
                if candidate.suffix != suffix:
                    continue

                self.__process_candidate(candidate, category, None)

    def collect_from_packages(self, path=None, prefix=None):
        """Collect resources from CIJOE packages at the given 'path'"""

        if prefix is None:
            prefix = ""

        for pkg in pkgutil.walk_packages(path, prefix):
            comp = pkg.name.split(".")[1:]  # drop the 'joe.' prefix
            if not (
                pkg.ispkg
                and any(cat in comp for cat, _ in Collector.RESOURCES)
                and len(comp) == 2
            ):  # skip non-resource packages
                continue

            _, category = comp
            for candidate in importlib.resources.files(f"{pkg.name}").iterdir():
                if candidate.name in Collector.IGNORE:
                    continue

                self.__process_candidate(candidate, category, pkg)

    def collect(self):
        """Collect from all implemented resource "sources" """

        if self.is_done:
            return

        self.collect_from_packages(joe.__path__, "joe.")
        self.collect_from_path()
        self.is_done = True


def collect():
    """Returns resources collected by Collector"""

    collector = Collector()
    collector.collect()

    return collector.resources
