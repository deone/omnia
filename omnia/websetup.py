"""Setup the omnia application"""
import logging

from paste.deploy import appconfig
from pylons import config

from omnia.config.environment import load_environment
from omnia.model import meta

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup omnia here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    logging.info("Creating tables")
    meta.metadata.create_all(bind=meta.engine)
    logging.info("Finished setting up")
