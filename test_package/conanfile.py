#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    fail_timeout = '30s'
    abort_timeout = '35s'

    requires = (
            "jungle_logstore/0.1.3@sds/testing",
            "picojson/1.3.0@oss/stable",
            "sds_logging/3.3.0@sds/testing",
        )

    def build(self):
        cmake = CMake(self)
        definitions = {'CMAKE_EXPORT_COMPILE_COMMANDS': 'ON'}
        cmake.configure(defs=definitions)
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            self.run("echo $(pwd)")
            bin_path = os.path.join("../../", "run_tests.sh")
            if self.settings.os == "Windows":
                self.run(bin_path)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path))
            else:
                bin_path = "timeout -k {} {} {}".format(self.abort_timeout, self.fail_timeout, bin_path)
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path))
