run-job: 
	pyats run job network_tests/network_test_job.py --testbed testbed.yaml

run-portchannel-test: 
	python network_tests/port_channel_test.py --testbed testbed.yaml 

log-viewer: 
	pyats logs view