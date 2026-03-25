"""
Base Watcher — abstract template all watchers inherit from.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

VAULT_PATH = Path("/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault")


class BaseWatcher(ABC):
    def __init__(self, check_interval: int = 60):
        self.vault_path = VAULT_PATH
        self.needs_action = self.vault_path / "Needs_Action"
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process."""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder."""
        pass

    def run(self):
        self.logger.info(f"Starting {self.__class__.__name__} (interval: {self.check_interval}s)")
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    path = self.create_action_file(item)
                    self.logger.info(f"Action file created: {path.name}")
            except Exception as e:
                self.logger.error(f"Error: {e}")
            time.sleep(self.check_interval)
