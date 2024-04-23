import os
import logging as logger
import urllib.parse
from shotgun_api3 import shotgun


class ActionHandler:
    def __init__(self, argv):
        shotgrid_url = "your_shotgrid_url"
        scripts_name = "your_script_name"
        scripts_key = "your_script_key"

        self.sg = shotgun.Shotgun(shotgrid_url, script_name=scripts_name, api_key=scripts_key)

        self.log_file = ''
        self.log_file_setting(argv[0])
        self.log = self._init_log(self.log_file)

        self.url = argv[1]
        self.action, self.params = self._parse_url()

        self.entity_type = ''
        self.selected_ids = ''
        self.selected_ids_filter = []

        self.init_set(self.action)

    def _parse_url(self):
        self.log.info("Parsing full url received: %s" % self.url)

        # get the protocol used
        protocol, path = self.url.split(":", 1)
        self.log.info("protocol: %s" % protocol)

        # extract the action
        action, params = path.split("?", 1)
        action = action.strip("/")
        self.log.info("action: %s" % action)

        # extract the parameters
        # 'column_display_names' and 'cols' occurs once for each column displayed so we store it as a list
        params = params.split("&")
        p = {"column_display_names": [], "cols": []}
        for arg in params:
            key, value = map(urllib.parse.unquote, arg.split("=", 1))
            if key == "column_display_names" or key == "cols":
                p[key].append(value)
            else:
                p[key] = value
        params = p
        self.log.info("params: %s" % params)
        return action, params

    def init_set(self, action):
        if action == 'mp4_download':
            # entity type that the page was displaying
            self.entity_type = self.params["entity_type"]

            # ids of entities that were currently selected
            if len(self.params["selected_ids"]) > 0:
                sids = self.params["selected_ids"].split(",")
                self.selected_ids = [int(sid) for sid in sids]

            # All selected ids of the entities returned by the query in filter format ready
            # to use in a find() query
            self.selected_ids_filter = self._convert_ids_to_filter(self.selected_ids)
            self.log.info("'%s' correct action menu name" % action)
        else:
            self.log.info("'%s' Incorrect action menu name" % action)
            raise IndexError("Incorrect action menu name")

    def _convert_ids_to_filter(self, idents):
        filter_list = []
        for ident in idents:
            filter_list.append(["id", "is", ident])
        self.log.debug("parsed ids into: %s" % filter_list)
        return filter_list

    def log_file_setting(self, argv):
        log_dir = os.path.dirname(argv) + os.sep + 'action_log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        else:
            self.log_file = log_dir + os.sep + 'shotgun_action.log'

    @staticmethod
    def _init_log(filename):
        try:
            logger.basicConfig(
                level=logger.DEBUG,
                format="%(asctime)s %(levelname)-8s %(message)s",
                datefmt="%Y-%b-%d %H:%M:%S",
                filename=filename,
                filemode="w+",
            )
        except IOError as e:
            raise ShotgunActionException("Unable to open logfile for writing: %s" % e)
        logger.info("ShotgunAction logging started.")
        return logger


class ShotgunActionException(Exception):
    pass
