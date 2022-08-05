from joe.core.workflow import Workflow
from joe.core.resources import Collector

def test_workflow_load():
    col = Collector()
    col.collect()

    res = col.resources["workflows"]["core.example"]

    workflow = Workflow(res.path, res.pkg)
    assert workflow

    workflow.load(col.resources)
    assert workflow.yml

    assert workflow.lint(col.resources), "Linting failed on 'core.example' workflow"
