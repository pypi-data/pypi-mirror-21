

import os, sys
import unittest

# Add the path of all the tests to this path
sys.path.append(os.path.realpath('tests'))



# Import all the test files
from test_example import TestExample
from test_parse_errors import TestParseErrors
from test_parse_cpu_string import TestParseCPUString
from test_invalid_cpu import TestInvalidCPU
from test_linux_debian_8_x86_64 import TestLinuxDebian_8_X86_64
from test_linux_debian_8_5_x86_64 import TestLinuxDebian_8_5_X86_64
from test_linux_debian_8_7_1_ppc64le import TestLinuxDebian_8_7_1_ppc64le
from test_linux_ubuntu_16_04_x86_64 import TestLinuxUbuntu_16_04_X86_64
from test_linux_fedora_24_x86_64 import TestLinuxFedora_24_X86_64
from test_linux_aarch64_64 import TestLinux_Aarch_64
from test_linux_gentoo_2_2_x86_64 import TestLinuxGentoo_2_2_X86_64
from test_linux_beagle_bone_arm import TestLinux_BeagleBone
from test_linux_raspberry_pi_model_b_arm import TestLinux_RaspberryPiModelB
from test_linux_odroid_c2_aarch64 import TestLinux_Odroid_C2_Aarch_64
from test_pcbsd_10_x86_64 import TestPCBSD
from test_free_bsd_11_x86_64 import TestFreeBSD_11_X86_64
from test_osx_10_9_x86_64 import TestOSX_10_9
from test_osx_10_12_x86_64 import TestOSX_10_12
from test_solaris_11_x86_32 import TestSolaris
from test_haiku_x86_32 import TestHaiku
from test_windows_8_x86_64 import TestWindows_8_X86_64
from test_windows_10_x86_64 import TestWindows_10_X86_64
from test_cpuid import TestCPUID
from test_actual import TestActual

if __name__ == '__main__':
	# Get all the tests
	tests = [
		TestParseCPUString,
		TestExample,
		TestParseErrors,
		TestInvalidCPU,
		TestLinuxDebian_8_X86_64,
		TestLinuxDebian_8_5_X86_64,
		TestLinuxDebian_8_7_1_ppc64le,
		TestLinuxUbuntu_16_04_X86_64,
		TestLinuxFedora_24_X86_64,
		TestLinux_Aarch_64,
		TestLinuxGentoo_2_2_X86_64,
		TestLinux_BeagleBone,
		TestLinux_RaspberryPiModelB,
		TestLinux_Odroid_C2_Aarch_64,
		TestFreeBSD_11_X86_64,
		TestPCBSD,
		TestOSX_10_9,
		TestOSX_10_12,
		TestSolaris,
		TestHaiku,
		TestWindows_8_X86_64,
		TestWindows_10_X86_64,
		TestCPUID,
		TestActual
	]

	# Add the tests to the suite
	suite = unittest.TestSuite()
	for test in tests:
		suite.addTest(unittest.makeSuite(test))

	# Run the tests
	runner = unittest.TextTestRunner()
	runner.run(suite)
