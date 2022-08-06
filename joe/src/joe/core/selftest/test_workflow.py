from joe.core.resources import Collector
from joe.core.workflow import Workflow


def test_workflow_load():
    collector = Collector()
    collector.collect()

    res = collector.resources["workflows"]["core.example"]

    workflow = Workflow(res.path, res.pkg)
    assert workflow

    workflow.load(collector)
    assert workflow.yml

    assert workflow.lint(collector), "Linting failed on 'core.example' workflow"
