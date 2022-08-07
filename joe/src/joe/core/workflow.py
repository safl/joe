import os
import re
import pprint

import jinja2
import yaml

from joe.core.command import Cijoe, config_from_file
from joe.core.resources import Resource
from joe.core.misc import h1, h2, h3

class Workflow(Resource):

    SUFFIX = ".workflow"

    def __init__(self, path, pkg=None):
        super().__init__(path, pkg)

        self.collector = None
        self.yml = None

        self.doc = ""
        self.steps = []

        self.stats = {
            "success": 0,
            "failed": 0,
            "wallclk": 0.0,
        }

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

        if "doc" not in self.yml:
            errors.append("Missing key: 'doc'; workflow must have a description")
            return False
        if "steps" not in self.yml:
            errors.append("Missing key: 'steps'; workflow must have steps to perform")

        valid_keys = set(["name", "run", "uses", "with"])

        for count, step in enumerate(self.yml["steps"]):
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
            }

            if "uses" in entry:
                step["uses"] = entry.get("uses")
                step["with"] = entry.get("with", {})
                step["id"] = f"{step['count']}_worklet_{step['uses']}"
            elif "run" in entry:
                step["run"] = entry.get("run").strip().splitlines()
                step["id"] = f"{step['count']}_inline_commands"
            else:
                return False

            self.steps.append(step)

        self.collector = collector

        return True

    def substitute(self, config):
        """Substitute workflow place-holders"""

        config = config if config else {}

        # Substitute values in workflow with config entities
        jinja_env = jinja2.Environment()
        for index, step in enumerate(self.steps):
            if "run" in step:
                template = jinja_env.from_string("\n".join(step["run"]))
                step["run"] = template.render(*config).split("\n")

            # TODO: substitute in "uses"

    def run(self, args):
        """Run the workflow using the given configuration(args.config)"""

        resources = self.collector.resources
        config = config_from_file(args.config) if args.config else {}
        cijoe = Cijoe(config, args.output)

        self.substitute(config)

        nsteps = len(self.steps)

        step_names = [step["name"] for step in self.steps]
        for step in args.step:
            if step in step_names:
                continue

            print(f"step: '{step}' not in workflow; Failed")
            return 1

        for count, step in enumerate(self.steps, 1):
            h2(f"Step({count}/{len(self.steps)}); '{step['name']}'")

            if args.step and step["name"] not in args.step:
                h3(f"Step({count}/{nsteps}): '{step['name']}'; Skipped")
                continue

            cijoe.set_output_ident(step["id"])
            os.makedirs(os.path.join(cijoe.output_path, step["id"]), exist_ok=True)

            if "run" in step:
                for cmd_count, cmd in enumerate(step["run"], 1):
                    rcode, state = cijoe.run(cmd)
                    if rcode:
                        self.stats["failed"] += 1
                        h3(f"Step({count}/{nsteps}): '{step['name']}'; Failed")
                        print(f"cmd: {cmd}")
                        print(f"rcode: {rcode}")
                        h3()
                        return err

            else:
                worklet_ident = step["uses"]

                resources["worklets"][worklet_ident].load()
                err = resources["worklets"][worklet_ident].func(cijoe, args, step)
                if err:
                    self.stats["failed"] += 1
                    h3(f"Step({count}/{nsteps}): '{step['name']}'; Failed")
                    return err

            self.stats["success"] += 1
            h3(f"Step({count}/{nsteps}): '{step['name']}'; Success")

        return 0
