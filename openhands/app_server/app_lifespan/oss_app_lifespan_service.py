from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config

from openhands.app_server.app_lifespan.app_lifespan_service import AppLifespanService


class OssAppLifespanService(AppLifespanService):
    run_alembic_on_startup: bool = True

    def __init__(self):
        super().__init__()
        if os.environ.get('SKIP_ALEMBIC_ON_STARTUP', '').lower() in ('1', 'true', 'yes'):
            self.run_alembic_on_startup = False

    def _check_database_exists(self) -> bool:
        """Check if the database file exists and has tables."""
        from openhands.app_server.config import get_global_config
        
        config = get_global_config()
        db_path = config.database_url.replace('sqlite:///', '')
        return os.path.exists(db_path) and os.path.getsize(db_path) > 0

    async def __aenter__(self):
        print('OssAppLifespanService.__aenter__ called', flush=True)
        if self.run_alembic_on_startup:
            if self._check_database_exists():
                print('Database exists, skipping alembic migration', flush=True)
            else:
                print('Database does not exist, running alembic migration', flush=True)
                self.run_alembic()
        print('OssAppLifespanService.__aenter__ completed', flush=True)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        print('OssAppLifespanService.__aexit__ called', flush=True)
        pass

    def run_alembic(self):
        # Run alembic upgrade head to ensure database is up to date
        alembic_dir = Path(__file__).parent / 'alembic'
        alembic_ini = alembic_dir / 'alembic.ini'

        # Create alembic config with absolute paths
        alembic_cfg = Config(str(alembic_ini))
        alembic_cfg.set_main_option('script_location', str(alembic_dir))

        # Change to alembic directory for the command execution
        original_cwd = os.getcwd()
        try:
            os.chdir(str(alembic_dir.parent))
            command.upgrade(alembic_cfg, 'head')
        finally:
            os.chdir(original_cwd)
