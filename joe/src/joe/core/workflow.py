import os
import re
import time

import jinja2
import yaml

from joe.core.command import Cijoe
from joe.core.misc import dict_from_yaml, h3
from joe.core.resources import Resource


class Workflow(Resource):

    SUFFIX = ".workflow"
    STATE_FILENAME = "workflow.state"
    STATE = {
        "doc": "",
        "config": {},
        "steps": [],
        "status": {"skipped": 0, "failure": 0, "success": 0, "elapsed": 0.0},
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

        valid_keys = set(["name", "run", "uses", "with"])

        for count, step in enumerate(yml["steps"]):
            keys = set(step.keys())

            if "name" not in keys:
                errors.append(f"Invalid step({count}); missing key 'name'")
                continue
            if not re.match("^([a-zA-Z][a-zA-Z0-9\.\-_]*)", step["name"]):
                errors.append(f"Invalid step({count}); invalid chars in 'name'")
                continue

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

    @staticmethod
    def yaml_substitute(yml, config):
        """Substitute workflow place-holders, returns a list of substitution errors"""

        errors = []

        cfg = yml.get("config", {})
        cfg.update(config)

        # Substitute values in workflow-yaml with config entities
        jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined)
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

        return errors

    def load(self, collector, config):
        """Load raw yaml, lint it, then construct the object properties"""

        if self.state:
            return True

        self.collector = collector

        yml = dict_from_yaml(self.path)

        errors = Workflow.yaml_lint(yml, collector)
        if errors:
            return False

        errors = Workflow.yaml_substitute(yml, config)
        if errors:
            return False

        state = Workflow.STATE.copy()
        state["doc"] = yml.get("doc")
        state["config"] = yml.get("config", {})
        for count, step in enumerate(yml["steps"], 1):
            step["count"] = count
            step["status"] = {"skipped": 0, "success": 0, "failure": 0, "elapsed": 0.0}
            step["id"] = f"{count}_{step['name']}"

            state["steps"].append(step)

        self.state = state

        return True

    def run(self, args):
        """Run the workflow using the given configuration(args.config)"""

        resources = self.collector.resources
        config = dict_from_yaml(args.config) if args.config else {}
        cijoe = Cijoe(config, args.output)

        self.load(self.collector, config)

        nsteps = len(self.state["steps"])

        step_names = [step["name"] for step in self.state["steps"]]
        for step_name in args.step:
            if step_name in step_names:
                continue

            print(f"step: '{step_name}' not in workflow; Failed")
            return 1

        self.state_dump(args.output / Workflow.STATE_FILENAME)

        for step in self.state["steps"]:
            cijoe.set_output_ident(step["id"])
            os.makedirs(os.path.join(cijoe.output_path, step["id"]), exist_ok=True)

            h3(f"step({step['name']})")

            if args.step and step["name"] not in args.step:
                step["status"]["skipped"] = 1
            elif "run" in step:
                for cmd_count, cmd in enumerate(step["run"], 1):
                    rcode, state = cijoe.run(cmd)

                    step["status"]["failure" if rcode else "success"] = 1
                    if rcode:
                        break
            else:
                worklet_ident = step["uses"]

                resources["worklets"][worklet_ident].load()
                err = resources["worklets"][worklet_ident].func(
                    args, self.collector, cijoe, step
                )
                step["status"]["failure" if err else "success"] = 1

            for key in ["skipped", "failure", "success"]:
                self.state["status"][key] += step["status"][key]

            if step["status"]["failure"]:
                break

            self.state_dump(args.output / Workflow.STATE_FILENAME)

        time.sleep(1)

        return 0
