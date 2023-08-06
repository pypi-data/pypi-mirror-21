# -*- coding:utf-8 -*-
from zenmai.core.evaluator import Evaluator
from zenmai.core.context import Context
from zenmai.core.loader import Loader
from dictknife import loading


def compile(d, module, filename=None, evaluator_factory=Evaluator, loader_factory=Loader, context_factory=Context):
    evalator = evaluator_factory()
    loader = loader_factory(d, rootfile=filename)
    context = context_factory(module, loader, evalator, filename=filename)
    return evalator.eval(context, d)


def compilefile(module, filename):
    loading.setup()
    d = loading.loadfile(filename)
    return compile(d, module, filename=filename)
