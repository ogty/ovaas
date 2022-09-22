import os
import subprocess

from dotenv import load_dotenv

from .function_app import FunctionApp, Deployment, Delete, Create


load_dotenv()


STORAGE = os.environ["STORAGE"]
LOCATION = os.environ["LOCATION"]
PYTHON_VERSION = os.environ["PYTHON_VERSION"]
RESOURCE_GROUP = os.environ["GLOBALLY_UNIQUE_PREFIX"]
FUNCTION_VERSION = os.environ["FUNCTION_VERSION"]
GLOBALLY_UNIQUE_PREFIX = os.environ["GLOBALLY_UNIQUE_PREFIX"]


async def deploy(token: str, username: str):
    app_name = "%s-%s" % (GLOBALLY_UNIQUE_PREFIX, username)
    zip_path = f"media/{token}.zip"

    settings = Deployment(
        name=app_name,
        src=zip_path,
        resource_group=RESOURCE_GROUP,
    )

    function_app = FunctionApp()
    function_app.deployment(settings).run()

    subprocess.run(["rm", zip_path])


def create_function(username: str):
    app_name = "%s-%s" % (GLOBALLY_UNIQUE_PREFIX, username)

    settings = Create(
        name=app_name,
        storage_account=STORAGE,
        consumption_plan_location=LOCATION,
        resource_group=RESOURCE_GROUP,
        os_type="Linux",
        runtime="python",
        runtime_version=PYTHON_VERSION,
        functions_version=FUNCTION_VERSION,
    )

    function_app = FunctionApp()
    function_app.create(settings).run()


def delete_function(username: str) -> None:
    app_name = "%s-%s" % (GLOBALLY_UNIQUE_PREFIX, username)

    settings = Delete(
        name=app_name,
        resource_group=RESOURCE_GROUP,
    )

    function_app = FunctionApp()
    function_app.delete(settings).run()
