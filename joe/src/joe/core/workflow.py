import os

import yaml

from joe.core.command import Cijoe, config_from_file
from joe.core.resources import Resource


class Workflow(Resource):

    SUFFIX = ".workflow"

    def __init__(self, path, pkg=None):
        super().__init__(path, pkg)

        self.yml = None
        self.docstring = ""
        self.steps = []
        self.collector = None

    def load_yaml(self):
        """Load yaml from file"""

        with self.path.open() as yml_file:
            self.yml = yaml.load(yml_file, Loader=yaml.SafeLoader)

    def lint(self, collector=None):
        """Returns a list of errors"""

        errors = []

        if not self.yml:
            try:
                self.load_yaml()
            except yaml.YAMLError as exc:
                errors.append(f"Invalid Workflow-YAML; exception({exc})")
                return errors

        if "docstring" not in self.yml:
            errors.append("Missing key: 'docstring'; workflow must have a description")
            return False
        if "steps" not in self.yml:
            errors.append("Missing key: 'steps'; workflow must have steps to perform")

        valid_keys = set(["name", "run", "uses", "with"])

        for count, step in enumerate(self.yml["steps"]):
            keys = set(step.keys()) - set(["name"])  # ignore the optional name-key

            if len(keys - valid_keys):
                errors.append(f"Invalid step({count}); has unsupported keys({keys})")
                continue

            if len(keys & set(["run", "uses"])) == 2:
                errors.append(f"Invalid step({count}); has both 'run' and 'uses'")
                continue
            if len(keys & set(["run", "uses"])) == 0:
                errors.append(f"Invalid step({count}); has neither 'run' nor 'uses'")
                continue

            if "with" in keys and "uses" not in keys:
                errors.append(f"Invalid step({count}); has 'with' missing 'uses'")
                continue
            if "with" in keys and "args" not in step["with"]:
                errors.append(f"Invalid step({count}); has 'with' missing 'with:args'")
                continue

            if collector is None:
                continue
            if "uses" in keys and step["uses"] not in collector.resources["worklets"]:
                errors.append(
                    f"Invalid step({count}); unknown resource: worklet({step['uses']})"
                )
                continue

        return errors

    def load(self, collector):
        """Load raw yaml, lint it, then construct the object properties"""

        if not self.yml:
            try:
                self.load_yaml()
            except yaml.YAMLError:
                return False

        errors = self.lint(collector)
        if errors:
            return False

        for count, entry in enumerate(self.yml["steps"], 1):
            step = {
                "id": "",  # file-system-safe identifier
                "count": count,
                "name": entry.get("name", "") if entry.get("name") else "unnamed step",
                "run": "",
                "uses": "",
                "with": {},
            }

            if "uses" in entry:
                step["uses"] = entry.get("uses")
                step["with"] = entry.get("with", {})
                step["type"] = "worklet"
                step["id"] = f"{step['count']}_{step['type']}_{step['uses']}"
            elif "run" in entry:
                step["type"] = "run"
                step["run"] = entry.get("run").strip().splitlines()
                step["id"] = f"{step['count']}_{step['type']}"
            else:
                return False

            self.steps.append(step)

        self.collector = collector

        return True

    def run(self, args):
        """Run the workflow using the given configuration"""

        cijoe = Cijoe(config_from_file(args.config) if args.config else {}, args.output)
        resources = self.collector.resources

        for step in self.steps:
            cijoe.set_output_ident(step["id"])
            os.makedirs(os.path.join(cijoe.output_path, step["id"]), exist_ok=True)

            if step["type"] == "run":
                for cmd in step["run"]:
                    cijoe.run(cmd)
            elif step["type"] == "worklet":
                worklet_ident = step["uses"]
                if worklet_ident not in resources["worklets"]:
                    print(f"Unknown worklet({worklet_ident})")
                    continue

                resources["worklets"][worklet_ident].load(self.collector)
                resources["worklets"][worklet_ident].func(cijoe, args, step)

        return True
