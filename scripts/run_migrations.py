import sys
import time
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

from alembic import command
from alembic.config import Config

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


load_dotenv()


def wait_for_db(max_retries=5, delay=5):
    """Wait for the database to become available."""
    from sqlalchemy import create_engine, text

    from app.core.settings import settings

    retries = 0
    while retries < max_retries:
        try:
            # Replace asyncpg with psycopg2 for synchronous operations
            sync_url = settings.DATABASE_URL.replace(
                "postgresql+asyncpg://", "postgresql://"
            )
            engine = create_engine(sync_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            return True
        except OperationalError:
            retries += 1
            if retries == max_retries:
                print(f"Could not connect to database after {max_retries} attempts")
                raise
            print(
                f"Database not ready, retrying in {delay} seconds... "
                f"(attempt {retries}/{max_retries})"
            )
            time.sleep(delay)
    return False


def run_migrations() -> None:
    """Run database migrations."""
    # Wait for database to be ready
    wait_for_db()

    # Get the path to alembic.ini
    alembic_ini_path = project_root / "alembic.ini"

    # Create Alembic configuration
    alembic_cfg = Config(str(alembic_ini_path))

    # Run migrations
    print("Running database migrations...")
    try:
        command.upgrade(alembic_cfg, "head")
        print("Migrations completed successfully.")
    except Exception as e:
        print(f"Error running migrations: {e!s}")
        raise


if __name__ == "__main__":
    run_migrations()
