import os
import re
import time

import jinja2
import yaml

from joe.core.command import Cijoe
from joe.core.misc import h3
from joe.core.resources import Resource, Collector


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
    def yaml_normalize(yml):
        """Normalize the YAML, currently just a transformation of the 'run' shorthand"""

        errors = []

        if "steps" not in yml:
            errors.append(f"Missing required top-level key: 'steps'")
            return errors

        for step in yml["steps"]:
            if "run" not in step.keys():
                continue

            step["uses"] = "core.cmdrunner"
            step["with"] = {
                "commands": step["run"].splitlines()
            }

            del step["run"]

        return errors

    @staticmethod
    def yaml_lint(yml, collector=None):
        """Returns a list of integrity-errors for the given yml-file"""

        errors = []

        for top in set(yml.keys()) - set(["doc", "config", "steps"]):
            errors.append(f"Unsupported top-level key: '{top}'")
            return False
        for top in ["doc", "steps"]:
            if top not in yml:
                errors.append(f"Missing required top-level key: '{top}'")
                return False

        valid = set(["name", "uses", "with"])
        required = set(["name", "uses"])

        for count, step in enumerate(yml["steps"], 1):
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

    @staticmethod
    def yaml_substitute(yml, config):
        """Substitute workflow place-holders, returns a list of substitution errors"""

        errors = []

        cfg = yml.get("config", {})
        cfg.update(config)

        # Substitute values in workflow-yaml with config entities
        jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        """
        for step in yml["steps"]:
            if "run" in step:
                try:
                    step["run"] = [
                        jinja_env.from_string(ln).render(cfg)
                        for ln in step["run"].splitlines()
                    ]
                except jinja2.exceptions.UndefinedError as exc:
                    errors.append(f"Substitution-error: {exc}")

            # TODO: substitute in "uses"
        """

        return errors

    def load(self, collector, config):
        """Load raw yaml, lint it, then construct the object properties"""

        if self.state:
            return True

        self.collector = collector

        yml = dict_from_yaml(self.path)

        errors = Workflow.yaml_normalize(yml)
        if errors:
            h3("workflow.yaml_normalize() : Failed; Check workflow with 'joe -l'")
            return False

        errors = Workflow.yaml_lint(yml, collector)
        if errors:
            h3("workflow.yaml_lint() : Failed; Check workflow with 'joe -l'")
            return False

        errors = Workflow.yaml_substitute(yml, config)
        if errors:
            h3("workflow.yaml_substitute() : Failed; Check workflow with 'joe -l'")
            return False

        state = Workflow.STATE.copy()
        state["doc"] = yml.get("doc")
        state["config"] = yml.get("config", {})
        for count, step in enumerate(yml["steps"], 1):
            step["count"] = count
            step["status"] = {"skipped": 0, "passed": 0, "failed": 0, "elapsed": 0.0}
            step["id"] = f"{count}_{step['name']}"

            state["steps"].append(step)

        self.state = state

        return True

    def run(self, args):
        """Run the workflow using the given configuration(args.config)"""

        resources = self.collector.resources
        config = dict_from_yaml(args.config) if args.config else {}
        cijoe = Cijoe(args.config, args.output)

        if not self.load(self.collector, config):
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
