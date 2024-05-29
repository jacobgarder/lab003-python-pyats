"""
Verify Port-channel interface status.

For each port-channel interface in the testbed topology (type: port-channel),

    * Verify that the interface is running LACP
    * Verify that the portchannel interface running (a "U" is in the flags)
    * Verify that the expected member interfaces are configured on the port-channel
    * Verify that all member interfaces are up (flag "P")
"""
import logging

from pyats import aetest
from genie.testbed import load
from genie.utils import Dq
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)

# TODO: Throughout the testscript, if a Test or Step fails or errors, provide a useful message in the logs


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
            # TODO: Connect to all devices in the testbed.
            # TODO: Do NOT stream device connection details to standard out
            pass
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


class portchannel_checks(aetest.Testcase):
    """Check all Port-channel interfaces are operationally healthy."""

    # TODO: Before running any tests, the setup method should be ran to gather port-channl details from all supported devices
    def setup(self, testbed):
        """
        Learn and save the port-channel summary info from devices.

        By doing this in setup, save time re-pulling details for each test

        Args:
            testbed: pyATS testbed file
        """
        # Store port-channel on Testcase object
        self.learnt_portchannels = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("ios", "iosxe"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning Port-channels (etherchannels) for {device_name}")
                # TODO: Store the parsed and processed output form the command "show etherchannel summary"
                #       - Replace None with the correct method to retrieve the data
                self.learnt_portchannels[device_name] = None

    @aetest.test
    def lacp_test(self, testbed, steps):
        """
        Ensure all port-channels are running LACP.

        Args:
            testbed: pyATS testbed file
            steps: pyATS multi-step test feature
        """
        # Loop over every device in testbed and create a device_step
        for device_name, device in testbed.devices.items():
            # TODO: Every device should be ran as individual Steps. A failure on one device should NOT prevent testing of subsequent devices
            # Learn interface details for the device
            learnt_portchannels = self.learnt_portchannels[device_name]["interfaces"]

            # Create a list of port-channels defined in the testbed for this device
            topology_portchannels = [
                interface for interface, details in device.interfaces.items() if details.type == "port-channel"
            ]

            # Loop over each port-channel and check it's protocol
            # for port_channel, details in learnt_portchannels.items():
            for port_channel in topology_portchannels:
                # TODO: Every port-channel should be ran as sub-steps to the device step. A failure on one port-channel should NOT prevent testing of subsequent interfaces
                learnt_details = learnt_portchannels[port_channel]
                # Check the portchannel protocol to be LACP
                try:
                    # TODO: Check to see if the port-channel is running "lacp" (This test should be case insensitive )
                    #       - The protocol for the port-channel is available at `learnt_details["protocol"]`
                    #       - If the port-channel is NOT running lacp, fail the port-channel step
                    #       - Replace the if statement below with the proper code for the test
                    if 0 == 1:
                        pass
                except KeyError:
                    # TODO: If no port-channel protocol is found, the port-channel step should "error"
                    pass

    # TODO: Run the portchannel_flagtest as a Test Case
    def portchannel_flagtest(self, testbed, steps):
        """
        Ensure all port-channels show an "Up" (ie U) flag.

        Args:
            testbed: pyATS testbed file
            steps: pyATS multi-step test feature
        """
        # Loop over every device in testbed and create a device_step
        for device_name, device in testbed.devices.items():
            # TODO: Every device should be ran as individual Steps. A failure on one device should NOT prevent testing of subsequent devices
            # Learn interface details for the device
            learnt_portchannels = self.learnt_portchannels[device_name]["interfaces"]

            # Check each port-channel interface defined for the device in the testbed
            # TODO: Loop over each device interface defined in the testbed file
            #       - Replace the iteration in the placeholder below
            #       - Within the loop, the variable `interface` should have a value of the current interface name
            #           - See the line below `learnt_details = learnt_portchannels[interface]` where `interface` is used to access port-channel details
            for i in range(0, 0):
                # TODO: Verify the interface "type" is set to "port-channel"
                #       - Replace the if statement below with the proper code for the test
                if 0 == 1:
                    # TODO: Every port-channel should be ran as sub-steps to the device step. A failure on one port-channel should NOT prevent testing of subsequent interfaces
                    learnt_details = learnt_portchannels[interface]
                    # Check to verify that the port-channel report "Up" with a "U" in the flags
                    try:
                        if "U" not in learnt_details["flags"]:
                            # TODO: If the port-channel is not "Up", the port-channel step should fail
                            pass
                    except KeyError:
                        # TODO: If no flag information is found for the port-channel, the port-channel step should "error"
                        pass

    @aetest.test
    def portchannel_memmbers_test(self, testbed, steps):
        """
        Ensure all port-channels are configured with correct members.

        Args:
            testbed: pyATS testbed file
            steps: pyATS multi-step test feature
        """
        # Loop over every device in testbed and create a device_step
        for device_name, device in testbed.devices.items():
            # TODO: Every device should be ran as individual Steps. A failure on one device should NOT prevent testing of subsequent devices
            # Find the learnt port-channel details for this device
            learnt_portchannels = self.learnt_portchannels[device_name]["interfaces"]

            # Create a dictionary of port-channels defined in the testbed for this device
            # by finding all interfaces whose type is set to "port-channel".
            # The interface name is the "key", and the value will be a list of port-channel members
            topology_portchannels = {
                interface: [] for interface, details in device.interfaces.items() if details.type == "port-channel"
            }

            # Find each interface defined in the testbed for the device that is a port-channel interface
            # by finding all interfaces that have an attribute "channel_group".
            # Append this interface to the list of members for the port-channel in the topology_portchannels dict
            for interface, details in device.interfaces.items():
                if hasattr(details, "channel_group"):
                    try:
                        topology_portchannels[f"Port-channel{details.channel_group}"].append(interface)
                    except KeyError:
                        logger.error(f"Port-channel{details.channel_group} not defined in testbed for {device_name}")

            # Loop over each port-channel to verify the member interfaces
            for port_channel, topology_members in topology_portchannels.items():
                # TODO: Every port-channel should be ran as sub-steps to the device step. A failure on one port-channel should NOT prevent testing of subsequent interface
                # Get the learnt port-channel details for comparison
                learnt_details = learnt_portchannels[port_channel]

                # Check if any member interfaces were learnt from the device
                if "members" in learnt_details.keys():
                    learnt_members = learnt_details["port_channel"]["port_channel_member_intfs"]

                    # Verify that the port-channel members configured learned from the device match the defined members in the testbed
                    # TODO: Use set comparison to check if the list of learnt_members match the list of topology_members
                    #       - Replace the if statement below with the proper code for the test
                    if 0 == 1:
                        logger.error(f"learnt_members are {learnt_members}")
                        logger.error(f"topology_members are {topology_members}")
                        portchannel_step.failed("learnt_members do NOT match the topoogy members")
                else:
                    portchannel_step.failed(f"{port_channel} has no learnt_members.'")

    # TODO: Ensure the portchannel_members_flagtest can use test steps
    def portchannel_memmbers_flagtest(self, testbed):
        """
        Ensure all port-channels members are up by checking the member flag.

        Args:
            testbed: pyATS testbed file
            steps: pyATS multi-step test feature
        """
        # Loop over every device in testbed and create a device_step
        for device_name, device in testbed.devices.items():
            # TODO: Every device should be ran as individual Steps. A failure on one device should NOT prevent testing of subsequent devices
            # Find the learnt port-channel details for this device
            learnt_portchannels = self.learnt_portchannels[device_name]["interfaces"]

            # Loop over all interfaces defined in topology for this device
            for interface, details in device.interfaces.items():
                # Check to see if the interface is listed as being a channel_group member
                if hasattr(details, "channel_group"):
                    # Start a new sub-step for the member-interface
                    # TODO: Port-channel member test should be ran as sub-steps to the device step. A failure on one member should NOT prevent testing of subsequent members

                    # Find the flag values for the interface
                    # TODO: Leverage the Dq (Dictionary Query) library to find the member_flags for each interface
                    #       - Search through the "learnt_portchannels" dictionary for paths that contain the "interface"
                    #       - Retrieve the values for they key "flags"
                    #       - Replace the empty list below with proper Dq code
                    member_flags = []

                    # Check to see if a value for flags was returned, if not fail step
                    if len(member_flags) == 0:
                        member_step.failed(f"No flag found for member-interface {interface}")

                    # Check to verify that the flag is "P" indicating successful bundling
                    #   if not fail step
                    elif member_flags[0] != "P":
                        member_step.failed(f"Port-channel member-interface {interface} has a flag of {member_flags[0]}")


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
