import configparser
import pickle
import logging
import argparse
from typing import List, Type, Dict  # noqa
from .service import Service, ALL_SERVICES


class Bot(object):
    def __init__(self, name: str) -> None:
        logging.basicConfig(level=logging.INFO)

        # Set log levels for common chatty packages
        logging.getLogger('requests').setLevel(logging.WARN)
        logging.getLogger('tweepy').setLevel(logging.WARN)

        self.log = logging.getLogger(__name__)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--live', action='store_true',
                                 help='Actually post updates. Without this flag, runs in dev mode.')
        self.parser.add_argument('--setup', action='store_true',
                                 help='Configure accounts')
        self.name = name
        self.services = []  # type: List[Service]
        self.state = {}  # type: Dict

    def run(self) -> None:
        self.args = self.parser.parse_args()
        self.config_path = '%s.conf' % self.name
        self.state_path = '%s.state' % self.name
        self.read_config()

        if self.args.setup:
            self.setup()
            return

        if not self.args.live:
            self.log.warn("Running in test mode - not posting updates. Pass --live to run in live mode.")

        for Svc in ALL_SERVICES:
            if Service.name in self.config:
                svc = Svc(self.config, self.args.live)
                svc.auth()
                self.services.append(svc)

        if len(self.services) == 0:
            self.log.warning("Not posting to any services!")

        self.load_state()
        self.log.info("Running")
        try:
            self.main()
        finally:
            self.save_state()
            self.log.info("Shut down")

    def setup(self) -> None:
        print("Polybot setup")
        print("=" * 80)
        for Svc in ALL_SERVICES:
            if Svc.name not in self.config:
                result = input("Configure %s (y/n)? " % Svc.name)
                if result[0] == 'y':
                    if Svc(self.config, False).setup():
                        print("Configuring %s succeeded, writing config" % Svc.name)
                        self.write_config()
                    else:
                        print("Configuring %s failed." % Svc.name)
                else:
                    print("OK, skipping.")
            else:
                print("Service %s is already configured" % Svc.name)
            print('-' * 80)
        print("Setup complete. To reconfigure, remove the service details from %s" % self.config_path)

    def main(self) -> None:
        raise NotImplementedError()

    def load_state(self) -> None:
        try:
            with open(self.state_path, "rb") as f:
                self.state = pickle.load(f)
        except IOError:
            self.log.info("No state file found")

    def save_state(self) -> None:
        if len(self.state) != 0:
            self.log.info("Saving state...")
            with open(self.state_path, "wb") as f:
                pickle.dump(self.state, f, pickle.HIGHEST_PROTOCOL)

    def post(self, status: str, imagefile=None, lat: float=None, lon: float=None) -> None:
        self.log.info("> %s", status)
        for service in self.services:
            service.post(status, imagefile, lat, lon)

    def read_config(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def write_config(self) -> None:
        with open(self.config_path, 'w') as fp:
            self.config.write(fp)
