#!/usr/bin/env python

#    LXC Management Scripts,
#
#    Inspired from ezjail in FreeBSD
#
#    TODO:
#       * use libvirt-python instead of os.system('virsh')
#       * use config file for global variables
#       * add btrfs support
#       * add glusterfs if it supports subvolumes or similar
#       * replace _all_ os.system calls with proper API calls
#       * add network support
#       * add basejail support

import argh
import subprocess
import os
import tempfile

import os, errno

# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise


LXCROOT='/home/izhar/btrfs/jail'
RELEASEFILE='/home/izhar/btrfs/jail/fedora-release-15-3.noarch.rpm'
YUMCONF='/etc/yum.conf'

@argh.command
def create(name):
    """
        Create container
    """
    basejaildir = '%s/%s' % (LXCROOT, name)
    if not os.path.exists(basejaildir):
        mkdir_p(basejaildir)

    cmds = [
        'rpm -ivh %s --root %s' % (RELEASEFILE,basejaildir),
        'mkdir %s/etc/' % LXCROOT,
        'cp %s %s/etc/' % (YUMCONF, LXCROOT),
        'yum --installroot %s install yum bash net-tools vim-enhanced' % (
            basejaildir),
    ]

    for cmd in cmds:
        os.system(cmd)
    
    config = '''
    <domain type='lxc'>
      <name>%(name)s</name>
      <memory>51200</memory>
      <os>
        <type>exe</type>
        <init>/bin/sh</init>
      </os>
      <devices>
        <console type='pty'/>
        <filesystem type='mount'>
           <source dir='%(path)s'/>
           <target dir='/'/>
         </filesystem>
      </devices>
    </domain>
    ''' % {
        'name': name,
        'path': basejaildir
    }

    xmlfile = '%s.xml' % tempfile.mktemp()
    open(xmlfile, 'w').write(config)

    os.system('virsh -c lxc:// define %s' % xmlfile)
    

@argh.command
def start(name):
    """
        Start a container
    """
    os.system('virsh -c lxc:// start %s' % name)

@argh.command
def stop(name):
    """
        Stop a container
    """
    os.system('virsh -c lxc:// destroy %s' % name)

@argh.command
@argh.alias('list')
def list_():
    """
        List containers
    """
    os.system('virsh -c lxc:// list')


def main():
    p = argh.ArghParser()
    p.add_commands([
        create, start, stop, list_
    ])
    p.dispatch()
