"""
Verify all interfaces defined in the testbed topology are up/up.

Admin status checked by looked at "enabled" state.
Operartional status checked by looking at "oper_status".

"""
import logging

from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    """
    Setup the resources for the testscript.

    Prep the testbed and connect to devices.
    """

    @aetest.subsection
    def load_testbed(self, testbed):
        """
        Load the pyATS testbed into a Genie Testbed file for full library features.

        Args:
            testbed: pyATS testbed file
        """
        testbed = load(testbed)

        # Save the testbed as a parameter for the script
        self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):
        """
        Establishes connection to all your testbed devices.

        Args:
            testbed: pyATS testbed file
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        # connect to all testbed devices
        #   By default ANY error in the CommonSetup will fail the entire test run
        #   Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
            testbed.connect(log_stdout=False)
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


class interface_up(aetest.Testcase):
    """Check all defined interfaces in the testbed are in an up/up state."""

    @aetest.test
    def up_up_test(self, testbed, steps):
        """
        Ensure all defined interfaces in testbed are up/up.

        Args:
            testbed: pyATS testbed file
            steps: pyATS multi-step test feature
        """
        # Loop over every device in testbed and create a device_step
        for device_name, device in testbed.devices.items():
            with steps.start(
                f"Verifying interfaces on {device_name} are up/up.",
                continue_=True,
            ) as device_step:
                # Learn interface details for the device
                learnt_interfaces = device.learn("interface")

                # Loop over each interface in the topology and start an interface_step
                for interface in device.interfaces:
                    with device_step.start(
                        f"Checking interface {interface}",
                        continue_=True,
                    ) as interface_step:

                        # Check to see if the interface from the testbed is configured on the device
                        if interface in learnt_interfaces.info.keys():
                            # Create convenience variables for interface admin (enabled) and oper state
                            enabled = learnt_interfaces.info[interface]["enabled"]
                            enabled_state = "up" if enabled else "down"
                            oper_state = learnt_interfaces.info[interface][
                                "oper_status"
                            ]

                            # Check to see if the interface is up/up (enabled and oper_state up)
                            if not enabled and oper_state != "up":
                                interface_step.failed(
                                    f"Interface {interface} on {device} is {enabled_state}/{oper_state}"
                                )
                        # If interface not configured, fail step
                        else:
                            interface_step.failed(
                                f"Interface {interface} on {device} is not configured"
                            )


if __name__ == "__main__":
    # for stand-alone execution
    import argparse
    from pyats import topology

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        default=None,
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)
