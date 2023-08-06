#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#
# This file belongs to coshsh.
# Copyright Gerhard Lausser.
# This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

import os
import sys
import re
import logging
from logging.handlers import RotatingFileHandler
import coshsh
from coshsh.recipe import Recipe, RecipePidAlreadyRunning, RecipePidNotWritable, RecipePidGarbage
from coshsh.util import odict

logger = None

class Generator(object):

    base_dir = os.path.dirname(os.path.dirname(__file__))
    messages = []

    def __init__(self):
        self.recipes = coshsh.util.odict()
        self._logging_on = False

    def add_recipe(self, *args, **kwargs):
        try:
            recipe = coshsh.recipe.Recipe(**kwargs)
            self.recipes[kwargs["name"]] = recipe
        except Exception, e:
            logging.getLogger('coshsh').error("exception creating a recipe: %s" % e)
        pass

    def run(self):
        if not self._logging_on:
            self.setup_logging(logdir=".")
        for recipe in self.recipes.values():
            try:
                if recipe.pid_protect():
                    if recipe.collect():
                        recipe.render()
                        recipe.output()
                    recipe.pid_remove()
            except coshsh.recipe.RecipePidAlreadyRunning:
                logging.getLogger('coshsh').info("skipping recipe %s. already running" % (recipe.name))
            except coshsh.recipe.RecipePidNotWritable:
                logging.getLogger('coshsh').error("skipping recipe %s. cannot write pid file to %s" % (recipe.name, recipe.pid_dir))
            except coshsh.recipe.RecipePidGarbage:
                logging.getLogger('coshsh').error("skipping recipe %s. pid file %s contains garbage" % (recipe.name, recipe.pid_file))
            except Exception, exp:
                logging.getLogger('coshsh').error("skipping recipe %s (%s)" % (recipe.name, exp))
            else:
                pass

    def setup_logging(self, logdir=".", logfile="coshsh.log", scrnloglevel=logging.INFO, txtloglevel=logging.INFO):
        logdir = os.path.abspath(logdir)
        if not os.path.exists(logdir):
            os.mkdir(logdir)
    
        log = logging.getLogger('coshsh')
        if log.handlers:
            # this method can be called multiple times in the unittests
            log.handlers = []
        log.setLevel(logging.DEBUG)
        log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
        txt_handler = RotatingFileHandler(os.path.join(logdir, logfile), backupCount=2, maxBytes=20*1024*1024)
        #txt_handler.doRollover()
        txt_handler.setFormatter(log_formatter)
        txt_handler.setLevel(txtloglevel)
        log.addHandler(txt_handler)
        log.info("Logger initialised.")

        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(scrnloglevel)
        log.addHandler(console_handler)

        self._logging_on = True
        logger = logging.getLogger('coshsh')
