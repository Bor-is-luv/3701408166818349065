from test_task.celery import app
from .utils import *


@app.task
def task_to_gen_graph_and_save(func_id: int):
    gen_graph_and_save(func_id)
