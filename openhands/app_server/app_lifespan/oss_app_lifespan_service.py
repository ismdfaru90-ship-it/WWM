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

    def _check_database_has_tables(self) -> bool:
        """Check if the database has the required tables."""
        from openhands.app_server.config import get_global_config
        from openhands.app_server.services.db_session_injector import DbSessionInjector
        
        config = get_global_config()
        db_session = DbSessionInjector.from_app_config(config)
        db_path = os.path.join(db_session.persistence_dir, 'openhands.db')
        if not os.path.exists(db_path):
            return False
        
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='app_conversation_start_task'")
        result = cursor.fetchone()
        conn.close()
        return result is not None

    async def __aenter__(self):
        print('OssAppLifespanService.__aenter__ called', flush=True)
        if self.run_alembic_on_startup:
            if self._check_database_has_tables():
                print('Database has tables, skipping alembic migration', flush=True)
            else:
                print('Database missing tables, running alembic migration', flush=True)
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
