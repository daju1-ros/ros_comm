# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Checks to see if core Python scripts have been installed via pip instead of
using debs
"""

from __future__ import print_function

#A dictionary of ROS pure python scripts to their corresponding .deb packages
py_to_deb_packages = {'bloom': 'python-bloom',
                    'catkin': 'python-catkin',
                    'rospkg': 'python-rospkg',
                    'rosinstall': 'python-rosinstall',
                    'rosrelease': 'python-rosrelease',
                    'rosdep': 'python-rosdep',}

import subprocess 
import importlib
import os

#Not used currently
def get_host_os():
    import rospkg.os_detect
    os_detector = rospkg.os_detect.OsDetect()
    return (os_detector.detect_os())[0]

def is_host_os_ubuntu():
    return (get_host_os() == 'ubuntu')

def get_python_path_directories():
    return os.environ['PYTHONPATH'].split(os.pathsep)

def get_version_number_of_debian_package(deb_pkg):
    pass

#Needed stuff
def is_debian_package_installed(deb_pkg):
    return (subprocess.call('dpkg -l ' + deb_pkg, shell=True, stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w')) == 0)

def is_command_runnable(cmd_name):
    try:
        rc = subprocess.call('command -v ' + cmd_name, shell=True, stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w'))
        if(rc <= 0):
            return True
        else:
            return False
    except subprocess.CalledProcessError:        
        return False

def is_a_pip_path_on_ubuntu(path):
    return ('/usr/local' in path)

def is_python_package_installed(python_pkg):
    try:
        importlib.import_module(python_pkg)
        return True
    except ImportError:
        return False

def is_python_package_installed_via_pip(python_pkg):
    try:
        pkg_handle = importlib.import_module(python_pkg)
        return is_a_pip_path_on_ubuntu(pkg_handle.__file__)
    except ImportError:
        return False;
   
def yes_or_no(bool_val):
    if bool_val:
        return 'Yes'
    else:
        return 'No'

def print_table_line(python_pkg, deb_pkg, is_runnable, is_deb_installed, is_python_pkg_pip_installed):
    print('{0:15} | {1:20} | {2:15} | {3:15} | {4:15}'.format(python_pkg, \
                                            deb_pkg, \
                                            is_runnable, \
                                            is_deb_installed, \
                                            is_python_pkg_pip_installed))

def check_and_print(python_pkg):
    deb_pkg = py_to_deb_packages[python_pkg]
    print_table_line(python_pkg, \
                     deb_pkg, \
                     yes_or_no(is_command_runnable(python_pkg)), \
                     yes_or_no(is_debian_package_installed(deb_pkg)), \
                     yes_or_no(is_python_package_installed_via_pip(python_pkg)))

def run_all_checks_and_print_table():
    print_table_line('Py Package', 'Deb Package', 'Runnable', 'Deb Installed', 'Installed Via Pip')
    print_table_line('----------', '-----------', '--------', '-------------', '-----------------')
    for key in py_to_deb_packages:
        check_and_print(key)
