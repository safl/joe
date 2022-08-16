import os
import re
import time
import pprint

import jinja2
import yaml

from joe.core.command import Cijoe
from joe.core.misc import h3
from joe.core.resources import (
    Collector,
    Resource,
    Config,
    dict_from_yamlfile,
    dict_substitute,
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
        self.collector = None
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
            errors.append(f"Missing required top-level key: 'steps'")
            return errors

        for step in topic["steps"]:
            if "run" not in step.keys():
                continue

            step["uses"] = "core.cmdrunner"
            step["with"] = {"commands": step["run"].splitlines()}

            del step["run"]

        return errors

    @staticmethod
    def dict_lint(topic: dict, collector=None):
        """Returns a list of integrity-errors for the given workflow-dict(topic)"""

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

            if collector is None:
                continue
            if step["uses"] not in collector.resources["worklets"]:
                errors.append(
                    f"Invalid step({count}); unknown resource: worklet({step['uses']})"
                )
                continue

        return errors

    def load(self, collector, config):
        """
        Load the workflow-yamlfile, normalize it, lint it, substitute, then construct
        the object properties
        """

        errors = []

        if self.state:
            return errors

        self.collector = collector

        workflow_dict = dict_from_yamlfile(self.path)

        errors += Workflow.dict_normalize(workflow_dict)
        if errors:
            print(errors)
            h3("Workflow.normalize() : Failed; Check workflow with 'joe -l'")
            return errors

        errors += Workflow.dict_lint(workflow_dict, collector)
        if errors:
            print(errors)
            h3("Workflow.lint() : Failed; Check workflow with 'joe -l'")
            return errors

        errors += dict_substitute(workflow_dict, config)
        if errors:
            print(errors)
            h3("Collector.dict_substitute() : Failed; Check workflow with 'joe -l'")
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

        resources = self.collector.resources
        cfg = Config(args.config)
        errors = cfg.load()
        if errors:
            print(f"cfg.load() : Failed; Check the workflow using 'joe -l'")
            return 1

        pprint.pprint(cfg.state)
        pprint.pprint(args.config)

        cijoe = Cijoe(args.config, args.output)

        if not self.load(self.collector, cfg.state):
            print(f"workflow.load() : Failed; Check the workflow using 'joe -l'")
            return 1

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

                self.collector.resources["worklets"][worklet_ident].load()
                err = self.collector.resources["worklets"][worklet_ident].func(
                    args, self.collector, cijoe, step
                )
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
