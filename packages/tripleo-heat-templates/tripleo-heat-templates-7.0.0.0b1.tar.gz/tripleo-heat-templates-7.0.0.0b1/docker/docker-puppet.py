#!/usr/bin/env python
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# Shell script tool to run puppet inside of the given docker container image.
# Uses the config file at /var/lib/docker-puppet/docker-puppet.json as a source for a JSON
# array of [config_volume, puppet_tags, manifest, config_image, [volumes]] settings
# that can be used to generate config files or run ad-hoc puppet modules
# inside of a container.

import json
import os
import subprocess
import sys
import tempfile
import multiprocessing


# this is to match what we do in deployed-server
def short_hostname():
    subproc = subprocess.Popen(['hostname', '-s'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    cmd_stdout, cmd_stderr = subproc.communicate()
    return cmd_stdout.rstrip()


def pull_image(name):
    print('Pulling image: %s' % name)
    subproc = subprocess.Popen(['/usr/bin/docker', 'pull', name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    cmd_stdout, cmd_stderr = subproc.communicate()
    print(cmd_stdout)
    print(cmd_stderr)


def rm_container(name):
    if os.environ.get('SHOW_DIFF', None):
        print('Diffing container: %s' % name)
        subproc = subprocess.Popen(['/usr/bin/docker', 'diff', name],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        cmd_stdout, cmd_stderr = subproc.communicate()
        print(cmd_stdout)
        print(cmd_stderr)

    print('Removing container: %s' % name)
    subproc = subprocess.Popen(['/usr/bin/docker', 'rm', name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    cmd_stdout, cmd_stderr = subproc.communicate()
    print(cmd_stdout)
    print(cmd_stderr)

process_count = int(os.environ.get('PROCESS_COUNT',
                                   multiprocessing.cpu_count()))

config_file = os.environ.get('CONFIG', '/var/lib/docker-puppet/docker-puppet.json')
print('docker-puppet')
print('CONFIG: %s' % config_file)
with open(config_file) as f:
    json_data = json.load(f)

# To save time we support configuring 'shared' services at the same
# time. For example configuring all of the heat services
# in a single container pass makes sense and will save some time.
# To support this we merge shared settings together here.
#
# We key off of config_volume as this should be the same for a
# given group of services.  We are also now specifying the container
# in which the services should be configured.  This should match
# in all instances where the volume name is also the same.

configs = {}

for service in (json_data or []):
    if service is None:
        continue
    if isinstance(service, dict):
        service = [
            service.get('config_volume'),
            service.get('puppet_tags'),
            service.get('step_config'),
            service.get('config_image'),
            service.get('volumes', []),
        ]

    config_volume = service[0] or ''
    puppet_tags = service[1] or ''
    manifest = service[2] or ''
    config_image = service[3] or ''
    volumes = service[4] if len(service) > 4 else []

    if not manifest or not config_image:
        continue

    print('---------')
    print('config_volume %s' % config_volume)
    print('puppet_tags %s' % puppet_tags)
    print('manifest %s' % manifest)
    print('config_image %s' % config_image)
    print('volumes %s' % volumes)
    # We key off of config volume for all configs.
    if config_volume in configs:
        # Append puppet tags and manifest.
        print("Existing service, appending puppet tags and manifest\n")
        if puppet_tags:
            configs[config_volume][1] = '%s,%s' % (configs[config_volume][1],
                                                   puppet_tags)
        if manifest:
            configs[config_volume][2] = '%s\n%s' % (configs[config_volume][2],
                                                    manifest)
        if configs[config_volume][3] != config_image:
            print("WARNING: Config containers do not match even though"
                  " shared volumes are the same!\n")
    else:
        print("Adding new service\n")
        configs[config_volume] = service

print('Service compilation completed.\n')

def mp_puppet_config((config_volume, puppet_tags, manifest, config_image, volumes)):

    print('---------')
    print('config_volume %s' % config_volume)
    print('puppet_tags %s' % puppet_tags)
    print('manifest %s' % manifest)
    print('config_image %s' % config_image)
    print('volumes %s' % volumes)
    hostname = short_hostname()
    sh_script = '/var/lib/docker-puppet/docker-puppet-%s.sh' % config_volume

    with open(sh_script, 'w') as script_file:
        os.chmod(script_file.name, 0755)
        script_file.write("""#!/bin/bash
        set -ex
        mkdir -p /etc/puppet
        cp -a /tmp/puppet-etc/* /etc/puppet
        rm -Rf /etc/puppet/ssl # not in use and causes permission errors
        echo '{"step": %(step)s}' > /etc/puppet/hieradata/docker.json
        TAGS=""
        if [ -n "%(puppet_tags)s" ]; then
            TAGS='--tags "%(puppet_tags)s"'
        fi
        FACTER_hostname=%(hostname)s FACTER_uuid=docker /usr/bin/puppet apply --verbose $TAGS /etc/config.pp

        # Disables archiving
        if [ -z "%(no_archive)s" ]; then
            rm -Rf /var/lib/config-data/%(name)s

            # copying etc should be enough for most services
            mkdir -p /var/lib/config-data/%(name)s/etc
            cp -a /etc/* /var/lib/config-data/%(name)s/etc/

            if [ -d /root/ ]; then
              cp -a /root/ /var/lib/config-data/%(name)s/root/
            fi
            if [ -d /var/lib/ironic/tftpboot/ ]; then
              mkdir -p /var/lib/config-data/%(name)s/var/lib/ironic/
              cp -a /var/lib/ironic/tftpboot/ /var/lib/config-data/%(name)s/var/lib/ironic/tftpboot/
            fi
            if [ -d /var/lib/ironic/httpboot/ ]; then
              mkdir -p /var/lib/config-data/%(name)s/var/lib/ironic/
              cp -a /var/lib/ironic/httpboot/ /var/lib/config-data/%(name)s/var/lib/ironic/httpboot/
            fi

            # apache services may files placed in /var/www/
            if [ -d /var/www/ ]; then
             mkdir -p /var/lib/config-data/%(name)s/var/www
             cp -a /var/www/* /var/lib/config-data/%(name)s/var/www/
            fi
        fi
        """ % {'puppet_tags': puppet_tags, 'name': config_volume,
               'hostname': hostname,
               'no_archive': os.environ.get('NO_ARCHIVE', ''),
               'step': os.environ.get('STEP', '6')})

    with tempfile.NamedTemporaryFile() as tmp_man:
        with open(tmp_man.name, 'w') as man_file:
            man_file.write('include ::tripleo::packages\n')
            man_file.write(manifest)

        rm_container('docker-puppet-%s' % config_volume)
        pull_image(config_image)

        dcmd = ['/usr/bin/docker', 'run',
                '--user', 'root',
                '--name', 'docker-puppet-%s' % config_volume,
                '--volume', '%s:/etc/config.pp:ro' % tmp_man.name,
                '--volume', '/etc/puppet/:/tmp/puppet-etc/:ro',
                '--volume', '/usr/share/openstack-puppet/modules/:/usr/share/openstack-puppet/modules/:ro',
                '--volume', '/var/lib/config-data/:/var/lib/config-data/:rw',
                '--volume', 'tripleo_logs:/var/log/tripleo/',
                '--volume', '%s:%s:rw' % (sh_script, sh_script) ]

        for volume in volumes:
            if volume:
                dcmd.extend(['--volume', volume])

        dcmd.extend(['--entrypoint', sh_script])

        env = {}
        # NOTE(flaper87): Always copy the DOCKER_* environment variables as
        # they contain the access data for the docker daemon.
        for k in filter(lambda k: k.startswith('DOCKER'), os.environ.keys()):
            env[k] = os.environ.get(k)

        if os.environ.get('NET_HOST', 'false') == 'true':
            print('NET_HOST enabled')
            dcmd.extend(['--net', 'host', '--volume',
                         '/etc/hosts:/etc/hosts:ro'])
        dcmd.append(config_image)

        subproc = subprocess.Popen(dcmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=env)
        cmd_stdout, cmd_stderr = subproc.communicate()
        print(cmd_stdout)
        print(cmd_stderr)
        if subproc.returncode != 0:
            print('Failed running docker-puppet.py for %s' % config_volume)
        rm_container('docker-puppet-%s' % config_volume)
        return subproc.returncode

# Holds all the information for each process to consume.
# Instead of starting them all linearly we run them using a process
# pool.  This creates a list of arguments for the above function
# to consume.
process_map = []

for config_volume in configs:

    service = configs[config_volume]
    puppet_tags = service[1] or ''
    manifest = service[2] or ''
    config_image = service[3] or ''
    volumes = service[4] if len(service) > 4 else []

    if puppet_tags:
        puppet_tags = "file,file_line,concat,augeas,%s" % puppet_tags
    else:
        puppet_tags = "file,file_line,concat,augeas"

    process_map.append([config_volume, puppet_tags, manifest, config_image, volumes])

for p in process_map:
    print '--\n%s' % p

# Fire off processes to perform each configuration.  Defaults
# to the number of CPUs on the system.
p = multiprocessing.Pool(process_count)
returncodes = list(p.map(mp_puppet_config, process_map))
config_volumes = [pm[0] for pm in process_map]
success = True
for returncode, config_volume in zip(returncodes, config_volumes):
    if returncode != 0:
        print('ERROR configuring %s' % config_volume)
        success = False

if not success:
    sys.exit(1)
