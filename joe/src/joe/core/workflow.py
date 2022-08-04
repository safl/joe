import os
import pprint
import re
from pathlib import Path

import yaml

from joe.core.command import Cijoe, config_from_file

WORKFLOW_SUFFIX = "workflow"


# TODO:
# * Implement this
def workflow_lint(yml):
    """Do integrity-check of workflow"""

    if "steps" not in yml:
        print("missing 'steps' in workflow file")
        return False
    for step in yml["steps"]:
        if "run" in step:
            continue
        if "uses" in step:
            continue

        print("step has neither 'run' nor 'uses'")
        return False

    return True


def paths_to_workflow_fpaths(paths):
    """Return list of workflow files in the given list of files and directories"""

    workflow_files = []
    for path in [Path(p).resolve() for p in paths]:
        if path.is_dir():
            workflow_files.extend(
                [p for p in path.iterdir() if p.name.endswith(f".{WORKFLOW_SUFFIX}")]
            )
        elif path.is_file() and path.name.endswith(f".{WORKFLOW_SUFFIX}"):
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

                resources["worklets"][worklet_ident].load()
                resources["worklets"][worklet_ident].func(joe, args, step)

    return 0
