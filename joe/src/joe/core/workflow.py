import os
import pprint
import re
from pathlib import Path

import yaml
from joe.core.resources import Resource
from joe.core.command import Cijoe, config_from_file


class Workflow(Resource):

    SUFFIX = ".workflow"

    def __init__(self, path, pkg=None):
        super().__init__(path, pkg)

        self.yml = None
        self.steps = []
        self.docstring = ""

    def load_yaml(self):
        """Load yaml from file"""

        with self.path.open() as yml_file:
            self.yml = yaml.load(yml_file, Loader=yaml.SafeLoader)

    def lint(self, resources = None):
        """Returns a list of errors"""

        errors = []

        if not self.yml:
            try:
                self.load_yaml()
            except:
                errors.append("Failed parsing Workflow-YAML")
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

            if "with" in keys and not "uses" in keys:
                errors.append(f"Invalid step({count}); has 'with' missing 'uses'")
                continue
            if "with" in keys and not "args" in step["with"]:
                errors.append(f"Invalid step({count}); has 'with' missing 'with:args'")
                continue

            if resources is None:
                continue
            if "uses" in keys and step["uses"] not in resources["worklets"]:
                errors.append(
                    f"(Invalid step({count}); unknown resource: worklet({step['uses']})"
                )
                continue

        return errors

    def load(self, resources):
        """Load raw yaml, lint it, then construct the object properties"""

        if not self.yml:
            self.load_yaml()

        errors = self.lint()
        for error in errors:
            print(error)

        if errors:
            return False

        # TODO: construct object properties from yml and collector

        return True


def paths_to_workflow_fpaths(paths):
    """Return list of workflow files in the given list of files and directories"""

    workflow_files = []
    for path in [Path(p).resolve() for p in paths]:
        if path.is_dir():
            workflow_files.extend(
                [p for p in path.iterdir() if p.name.endswith(f"{Workflow.SUFFIX}")]
            )
        elif path.is_file() and path.name.endswith(f"{Workflow.SUFFIX}"):
            workflow_files.append(path)

    return workflow_files


#
# TODO
#
# * linting is needed to ensure the workflow is well-defined and provide proper
#   error-messages when it is not
#
def workflow_from_fpath(fpath):
    """Returns a workflow from the given 'fpath'"""

    with open(fpath) as workflow_file:
        yml = yaml.load(workflow_file, Loader=yaml.SafeLoader)

    if not workflow_lint(yml):
        print("Invalid workflow file")
        return False

    workflow = {
        "docstring": yml["docstring"],
        "steps": [],
    }

    count = 0
    for entry in yml.get("steps", []):
        count += 1
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
            return None

        workflow["steps"].append(step)

    return workflow


# TODO:
# * Add use of the test-linter before attempting to run the workflow
# * Add error-handling
# * Improve the path-mangling for the cijoe-instance, especially when delegated to
#   worklets
def run_workflow_files(args, resources):
    """Run workflow files"""

    joe = Cijoe(config_from_file(args.config) if args.config else {}, args.output)

    for workflow_fpath in paths_to_workflow_fpaths(args.file_or_dir):
        workflow = workflow_from_fpath(workflow_fpath)

        for step in workflow["steps"]:
            joe.set_output_ident(step["id"])
            os.makedirs(os.path.join(joe.output_path, step["id"]), exist_ok=True)

            if step["type"] == "run":
                for cmd in step["run"]:
                    joe.run(cmd)
            elif step["type"] == "worklet":
                worklet_ident = step["uses"]
                if worklet_ident not in resources["worklets"]:
                    print(f"Unknown worklet({worklet_ident})")
                    continue

                resources["worklets"][worklet_ident].load(resources)
                resources["worklets"][worklet_ident].func(joe, args, step)

    return 0
