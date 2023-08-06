# -*- coding: utf-8 -*-
from ..decorators import attribute


@attribute(
    operators=(
        'to', 'has', 'have', 'satisfy',
        'satisfies', 'include', 'do', '_is', 'that', 'which'
    )
)
def be(ctx):
    """
    Semantic attributes providing chainable declarative DSL
    for assertions.
    """
    ctx.negate = False


@attribute(operators=(
    'not_to', 'to_not', 'does_not', 'do_not', '_not', 'not_satisfy',
    'not_have', 'not_has', 'have_not', 'has_not', 'dont', 'is_not',
))
def not_be(ctx):
    """
    Semantic negation attributes providing chainable declarative DSL
    for assertions.
    """
    ctx.negate = True
