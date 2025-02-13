"""
network_test_job.py
"""

import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""

    # Run Test Scripts
    run(
        testscript=os.path.join(SCRIPT_PATH, "testbed_connection.py"),
        runtime=runtime,
        taskid="Device Connections",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "interface_errors.py"),
        runtime=runtime,
        taskid="Interface Errors",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "interface_up.py"),
        runtime=runtime,
        taskid="Interface Up Check",
    )

    # TODO: Run the Testscript "port_channel_test.py" with a taskid of "Port-channel Tests"
    run(
        testscript=os.path.join(SCRIPT_PATH, "port_channel_test.py"),
        runtime=runtime,
        taskid="Port-channel Tests",
    )