"""
   repository_prep
   ===============

   For every key in the configuration which has a subkey named "repository", then
   following is done:

   * git clone (repository.upstream; skip if directory exists)
   * git checkout (repository.branch)
   * git pull --rebase
   * git status
"""
import logging as log
import errno


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

        repos_root = Path(repos['path']).parent

        rcode, _ = cijoe.run(f"mkdir -p {repos_root}")
        if rcode:
            log.error("failed creating dir for repository; giving up")
            return rcode

        rcode, _ = cijoe.run(
            f"[ ! -d {repos['path'].parent} ] &&"
            f" git clone {repos['upstream']} {repos['path']}"
        )
        if rcode:
            log.info("either already cloned or failed cloning; continuing optimisticly")

        rcode, _ = cijoe.run(f"git checkout {repos['branch']}", cwd=repos['path'])
        if rcode:
            log.error("Failed checking out; giving up")
            return rcode

        rcode, _ = cijoe.run("git pull --rebase", cwd=repos['path'])
        if rcode:
            log.info("failed pulling; continuing optimisticly")

        rcode, _ = cijoe.run("git status", cwd=repos['path'])
        if rcode:
            log.error("failed getting git status; giving up")
            return rcode

    return 0
