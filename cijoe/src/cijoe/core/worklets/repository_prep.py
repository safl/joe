"""
   repository_prep
   ===============

   For every key in the configuration which has a subkey named "repository", then
   following is done:

   * git clone (repository.upstream; skip if directory exists)
   * git checkout (repository.branch or repository.tag)
   * git pull --rebase (if repository.branch)
   * git status

   Configuration
   -------------

   Ensure that the "repository.{upstream,path,branch}" have sensible values

   Retargetable: True
   ------------------
"""
import errno
import logging as log
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Clone, checkout branch and pull"""

    rcode, _ = cijoe.run("git --version")
    if rcode:
        log.err("Looks like git is not available")
        return rcode

    for repos in [
        r["repository"] for r in cijoe.config.options.values() if "repository" in r
    ]:
        if len(set(["upstream", "path"]) - set(repos.keys())):
            continue
        if "qemu" in repos["upstream"]:
            continue

        repos_root = Path(repos["path"]).parent

        rcode, _ = cijoe.run(f"mkdir -p {repos_root}")
        if rcode:
            log.error("failed creating repos_root({repos_root}; giving up")
            return rcode

        rcode, _ = cijoe.run(
            f"[ ! -d {repos['path']} ] &&"
            f" git clone {repos['upstream']} {repos['path']} --recursive"
        )
        if rcode:
            log.info("either already cloned or failed cloning; continuing optimisticly")

        do_checkout = repos.get("branch", repos.get("tag", None))
        if do_checkout:
            rcode, _ = cijoe.run(f"git checkout {repos['branch']}", cwd=repos["path"])
            if rcode:
                log.error("Failed checking out; giving up")
                return rcode

            if "branch" in repos.keys():
                rcode, _ = cijoe.run("git pull --rebase", cwd=repos["path"])
                if rcode:
                    log.error("failed pulling; giving up")
                    return rcode
        else:
            log.info("no 'branch' nor 'tag' key; skipping checkout")


        rcode, _ = cijoe.run("git status", cwd=repos["path"])
        if rcode:
            log.error("failed 'git status'; giving up")
            return rcode

    return 0
