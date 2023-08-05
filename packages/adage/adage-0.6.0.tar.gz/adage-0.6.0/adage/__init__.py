import os
import time
import logging
import trackers

from adage.decorators import adageop, adagetask, Rule
from adage.adageobject import adageobject
from adage.pollingexec import setup_polling_execution
from adage.wflowcontroller import InMemoryController

#silence pyflakes
assert adageop
assert adagetask
assert Rule
assert adageobject

log = logging.getLogger(__name__)

def trackprogress(trackerlist,adageobj, method = 'track'):
    '''
    track adage workflow state using a list of trackers

    :param trackerlist: the stackers which should inspect the workflow
    :param adageobj: the adage workflow object
    :param method: tracking method to call. Must be one of ``initialize``, ``track``, ``finalize``
    :return: None
    '''
    map(lambda t: getattr(t,method)(adageobj), trackerlist)

def run_polling_workflow(controller, coroutine, update_interval, trackerlist = None):
    coroutine.send(controller)
    log.info('starting state loop.')

    try:
        trackprogress(trackerlist, controller.adageobj, method = 'initialize')
        for controller in coroutine:
            trackprogress(trackerlist, controller.adageobj)
            time.sleep(update_interval)
    except:
        log.exception('some weird exception caught in adage process loop')
        raise
    finally:
        trackprogress(trackerlist, controller.adageobj, method = 'finalize')

    log.info('adage state loop done.')

    if not controller.validate():
        raise RuntimeError('DAG execution not validating')
    log.info('execution valid. (in terms of execution order)')

    if not controller.successful():
        log.error('raising RunTimeError due to failed jobs')
        raise RuntimeError('DAG execution failed')

    log.info('workflow completed successfully.')

def default_trackerlist(gif_workdir = None, text_loggername = __name__, texttrack_delta = 1):
    workdir = gif_workdir or os.getcwd()
    trackerlist  = [trackers.SimpleReportTracker(text_loggername, texttrack_delta)]
    trackerlist += [trackers.GifTracker(gifname = '{}/workflow.gif'.format(workdir), workdir = '{}/track'.format(workdir))]
    trackerlist += [trackers.TextSnapShotTracker(logfilename = '{}/adagesnap.txt'.format(workdir), mindelta = texttrack_delta)]
    return trackerlist

def rundag(adageobj = None,
           backend = None,
           extend_decider = None,
           submit_decider = None,
           update_interval = 0.01,
           loggername = __name__,
           trackevery = 1,
           workdir = None,
           default_trackers = True,
           additional_trackers = None,
           controller = None,
    ):
    '''
    Main adage entrypoint. It's a convenience wrapper around the main adage coroutine loop and
    sets up the backend, logging, tracking (for GIFs, Text Snapshots, etc..) and possible interactive
    hooks into the coroutine

    :param adageobj: the adage workflow object
    :param backend: the task execution backend to which to submit node tasks
    :param extend_decider: decision coroutine to deal with whether to extend the workflow graph
    :param submit_decider: decision coroutine to deal with whether to submit node tasks
    :param update_interval: minimum looping interval for main adage loop 
    :param loggername: python logger to use
    :param trackevery: tracking interval for default simple report tracker
    :param workdir: workdir for default visual tracker
    :param default_trackers: whether to enable default trackers (simple report, gif visualization, text snapshot)
    :param additional_trackers: list of any additional tracking objects
    :param controller: optional external controller (instead of adageobj parameter)
    '''
    if loggername:
        global log
        log = logging.getLogger(loggername)


    log.info('got logger with name: %s', loggername)
    ## get primed coroutine for polling-style workflow execution
    coroutine = setup_polling_execution(extend_decider, submit_decider)

    ## prepare tracking objects
    trackerlist = default_trackerlist(workdir, loggername, trackevery) if default_trackers else []
    if additional_trackers:
        trackerlist += additional_trackers

    if adageobj:
        ## funny behavior of multiprocessing Pools means that
        ## we can not have backendsubmit = multiprocsetup(2)    in the function sig
        ## so we only initialize them here
        if not backend:
            from backends import MultiProcBackend
            backend = MultiProcBackend(2)

        ## prep controller with backend
        controller = InMemoryController(adageobj, backend)

    run_polling_workflow(controller, coroutine, update_interval, trackerlist)

