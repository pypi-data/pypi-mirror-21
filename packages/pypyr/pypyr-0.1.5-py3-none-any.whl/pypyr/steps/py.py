"""pypyr step that executes a string as python.

Uses python's exec() to evaluate and execute arbitrary python code.
"""
import pypyr.log.logger
import pypyr.validate.asserts

# logger means the log level will be set correctly
logger = pypyr.log.logger.get_logger(__name__)


def run_step(context):
    """Executes dynamic python code.

    Context is a dictionary or dictionary-like.
    Context must contain key 'pycode'
    Will exec context['pycode'] as dynamically interpreted python statements.

    context is mandatory. When you execute the pipeline, it should look
    something like this:
        pipeline-runner [name here] --context 'pycode=print(1+1)'.
    """
    logger.debug("started")
    pypyr.validate.asserts.key_in_context_has_value(
        context, 'pycode', 'py step')

    logger.debug(f"Executing python string: {context['pycode']}")
    locals_dictionary = locals()
    exec(context['pycode'], globals(), locals_dictionary)

    try:
        # It looks like this dance might be unnecessary in python 3.6
        logger.debug("looking for context update in exec")
        exec_context = locals_dictionary['context']
        context.update(exec_context)
        logger.debug("exec output context merged with pipeline context")
    except KeyError:
        # there wouldn't be a context key if the yaml didn't do anything with
        # it
        logger.debug("exec didn't alter context")
        pass

    logger.debug("done")
    return context
