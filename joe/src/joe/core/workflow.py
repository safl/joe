import os
import pprint
import re
import time

import yaml

from joe.core.command import Cijoe
from joe.core.misc import h3
from joe.core.resources import (
    Config,
    Resource,
    default_context,
    dict_from_yamlfile,
    dict_substitute,
    get_resources,
)


class Workflow(Resource):

    SUFFIX = ".workflow"
    STATE_FILENAME = "workflow.state"
    STATE = {
        "doc": "",
        "config": {},
        "steps": [],
        "status": {"skipped": 0, "failed": 0, "passed": 0, "elapsed": 0.0},
    }

    def __init__(self, path, pkg=None):
        super().__init__(path, pkg)

        self.state = None
        self.config = None

    def state_dump(self, path):
        """Dump the current workflow-state to yaml-file"""

        with path.open("w+") as state_file:
            yaml.dump(self.state, state_file)

    @staticmethod
    def dict_normalize(topic: dict):
        """Normalize the workflow-dict, transformation of the 'run' shorthand"""

        errors = []

        if "steps" not in topic:
            errors.append("Missing required top-level key: 'steps'")
            return errors

        for step in topic["steps"]:
            if "run" not in step.keys():
                continue

            step["uses"] = "core.cmdrunner"
            step["with"] = {"commands": step["run"].splitlines()}

            del step["run"]

        return errors

    @staticmethod
    def dict_lint(topic: dict):
        """Returns a list of integrity-errors for the given workflow-dict(topic)"""

        resources = get_resources()

        errors = []

        for top in set(topic.keys()) - set(["doc", "config", "steps"]):
            errors.append(f"Unsupported top-level key: '{top}'")
            return False
        for top in ["doc", "steps"]:
            if top not in topic:
                errors.append(f"Missing required top-level key: '{top}'")
                return False

        valid = set(["name", "uses", "with"])
        required = set(["name", "uses"])

        for count, step in enumerate(topic["steps"], 1):
            keys = set(step.keys())

            missing = required - keys
            if missing:
                errors.append(f"Invalid step({count}); required key(s): {missing}")
                continue

            if not re.match("^([a-zA-Z][a-zA-Z0-9\.\-_]*)", step["name"]):
                errors.append(f"Invalid step({count}); invalid chars in 'name'")
                continue

            unsupported = keys - valid
            if unsupported:
                errors.append(f"Invalid step({count}); unsupported keys({unsupported})")
                continue

            if step["uses"] not in resources["worklets"]:
                errors.append(
                    f"Invalid step({count}); unknown resource: worklet({step['uses']})"
                )
                continue

        return errors

    def load(self, config: Config):
        """
        Load the workflow-yamlfile, normalize it, lint it, substitute, then construct
        the object properties
        """

        errors = []

        if self.state:
            return errors

        resources = get_resources()

        workflow_dict = dict_from_yamlfile(self.path)

        errors += Workflow.dict_normalize(workflow_dict)
        if errors:
            print(errors)
            h3("Workflow.normalize() : Failed; Check workflow with 'joe -l'")
            return errors

        errors += Workflow.dict_lint(workflow_dict)
        if errors:
            print(errors)
            h3("Workflow.lint() : Failed; Check workflow with 'joe -l'")
            return errors

        errors += dict_substitute(workflow_dict, default_context(config))
        if errors:
            print(errors)
            h3("dict_substitute() : Failed; Check workflow with 'joe -l'")
            return errors

        state = Workflow.STATE.copy()
        state["doc"] = workflow_dict.get("doc")
        state["config"] = workflow_dict.get("config", {})
        for count, step in enumerate(workflow_dict["steps"], 1):
            step["count"] = count
            step["status"] = {"skipped": 0, "passed": 0, "failed": 0, "elapsed": 0.0}
            step["id"] = f"{count}_{step['name']}"

            state["steps"].append(step)

        self.state = state

        return errors

    def run(self, args):
        """Run the workflow using the given configuration(args.config)"""

        config = Config.from_path(args.config)
        if not config:
            print(f"Config.from_path() : Failed;")
            return 1

        resources = get_resources()
        if not self.load(config):
            print(f"workflow.load() : Failed; Check the workflow using 'joe -l'")
            return 1

        cijoe = Cijoe(config, args.output)
        nsteps = len(self.state["steps"])

        fail_fast = False

        step_names = [step["name"] for step in self.state["steps"]]
        for step_name in args.step:
            if step_name in step_names:
                continue

            print(f"step: '{step_name}' not in workflow; Failed")
            return 1

        self.state_dump(args.output / Workflow.STATE_FILENAME)

        for step in self.state["steps"]:

            h3(f"step({step['name']})")

            begin = time.time()

            cijoe.set_output_ident(step["id"])
            os.makedirs(os.path.join(cijoe.output_path, step["id"]), exist_ok=True)

            if args.step and step["name"] not in args.step:
                step["status"]["skipped"] = 1
            else:
                worklet_ident = step["uses"]

                resources["worklets"][worklet_ident].load()
                err = resources["worklets"][worklet_ident].func(args, cijoe, step)
                step["status"]["failed" if err else "passed"] = 1
                if step["status"]["failed"]:
                    h3(f"step({step['name']}) : failed worklet: {worklet_ident}")

            for key in ["failed", "passed", "skipped"]:
                self.state["status"][key] += step["status"][key]

            step["status"]["elapsed"] = time.time() - begin
            self.state["status"]["elapsed"] += step["status"]["elapsed"]
            self.state_dump(args.output / Workflow.STATE_FILENAME)

            if step["status"]["failed"] and fail_fast:
                h3(f"step({step['name']}) : exiting because ('fail_fast: True')")
                break

        return 1 if self.state["status"]["failed"] else 0
