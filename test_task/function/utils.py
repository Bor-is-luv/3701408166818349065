from datetime import datetime
import re
from io import BytesIO
import sys

import numpy as np
import matplotlib.pyplot as plt

from django.core.files.base import ContentFile

from .models import Function


replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
}

allowed_words = [
    't',
    'sin',
    'cos',
    'sqrt',
    'exp',
]


def at_least_one_num_is_out_of_bounds(array):
    for item in array:
        if item > sys.maxsize * 0.95 or item < -sys.maxsize * 0.95:
            raise ValueError('Warning. One or more values is too large. Maybe smth wrong!')

    return array


def string2func(string: str):
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            raise ValueError(
                '"{}" is forbidden to use in math expression'.format(word)
            )

    for old, new in replacements.items():
        string = string.replace(old, new)

    def func(t):
        return at_least_one_num_is_out_of_bounds(eval(string))

    return func


def gen_graph_and_save(func_id: int):
    function = Function.objects.get(pk=func_id)
    equation = function.equation
    dt = function.dt
    interval = function.interval
    now_datetime = datetime.now()
    now = int(now_datetime.timestamp())

    t = np.arange(now - interval*86400, now, dt*3600)

    try:
        func = string2func(equation)
    except Exception as ex:
        function.exception = ex.args[0]
        function.datetime = now_datetime
        function.save()
        return

    try:
        plt.plot(t, func(t))
    except Exception as ex:
        function.exception = ex.args[0]
        function.datetime = now_datetime
        function.save()
        plt.close()
        return

    plt.grid()

    f = BytesIO()
    plt.savefig(f)

    content_file = ContentFile(f.getvalue())
    function.graph.save(f'{func_id}', content_file)
    function.datetime = now_datetime
    function.save()
    plt.close()






