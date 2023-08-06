Testing with DevStack
=====================

This document describes how to test OpenStack with OVN using DevStack. We will
start by describing how to test on a single host.

Single Node Test Environment
----------------------------

1. Create a test system.

It's best to use a throwaway dev system for running DevStack.  In this example
I'm using a Fedora 21 VM with 4 GB of RAM.  You should be able to use any
distribution that is supported by DevStack.  So far, networking-ovn is being
tested on Fedora 21 and Ubuntu 14.04.

Create a user and grant it sudo access. Install git.

2. Get DevStack and networking-ovn.

::

     $ git clone http://git.openstack.org/openstack-dev/devstack.git
     $ git clone http://git.openstack.org/openstack/networking-ovn.git

3. Configure DevStack to use networking-ovn.

networking-ovn comes with a sample DevStack configuration file you can start
with.  For example, you may want to set some values for the various PASSWORD
variables in that file so DevStack doesn't have to prompt you for them.  Feel
free to edit it if you'd like, but it should work as-is.

::

    $ cd devstack
    $ cp ../networking-ovn/devstack/local.conf.sample local.conf

4. Run DevStack.

This is going to take a while.  It installs a bunch of packages, clones a bunch
of git repos, and installs everything from these git repos.

::

    $ ./stack.sh

Once DevStack completes successfully, you should see output that looks
something like this::

    This is your host ip: 192.168.122.8
    Horizon is now available at http://192.168.122.8/
    Keystone is serving at http://192.168.122.8:5000/
    The default users are: admin and demo
    The password: password
    2015-04-30 22:02:40.220 | stack.sh completed in 515 seconds.

Environment Variables
---------------------

Once DevStack finishes successfully, we're ready to start interacting with
OpenStack APIs.  OpenStack provides a set of command line tools for interacting
with these APIs.  DevStack provides a file you can source to set up the right
environment variables to make the OpenStack command line tools work.

::

    $ . openrc

If you're curious what environment variables are set, they generally start with
an OS prefix::

    $ env | grep OS
    OS_REGION_NAME=RegionOne
    OS_IDENTITY_API_VERSION=2.0
    OS_PASSWORD=password
    OS_AUTH_URL=http://192.168.122.8:5000/v2.0
    OS_USERNAME=demo
    OS_TENANT_NAME=demo
    OS_VOLUME_API_VERSION=2
    OS_CACERT=/opt/stack/data/CA/int-ca/ca-chain.pem
    OS_NO_CACHE=1

Default Network Configuration
-----------------------------

By default, DevStack creates a network called ``private``. Run the following
command to see the existing networks::

    $ neutron net-list
    +--------------------------------------+---------+----------------------------------------------------------+
    | id                                   | name    | subnets                                                  |
    +--------------------------------------+---------+----------------------------------------------------------+
    | 266371ca-904e-4433-b653-866f9204d22e | private | 64bc14c2-52a6-4188-aaeb-d24922125c2c fde5:95da:6b50::/64 |
    |                                      |         | 299d182b-2f2c-44e2-9bc9-d094b9ea317b 10.0.0.0/24         |
    +--------------------------------------+---------+----------------------------------------------------------+

A Neutron network is implemented as an OVN logical switch.  networking-ovn
creates logical switches with a name in the format neutron-<network UUID>.  So,
we can use ``ovn-nbctl`` to list the configured logical switches and see that
their names correlate with the output from ``neutron net-list``::

    $ ovn-nbctl ls-list
    c628c46a-372f-412b-8edf-eb3408b021ca (neutron-266371ca-904e-4433-b653-866f9204d22e)

    $ ovn-nbctl get Logical_Switch neutron-266371ca-904e-4433-b653-866f9204d22e external_ids
    {"neutron:network_name"=private}

There will be one port created automatically when not using OVN native DHCP.
This port corresponds to the Neutron DHCP agent that is providing DHCP services
to the ``private`` network.

::

    $ neutron port-list
    +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------------------------------------+
    | id                                   | name | mac_address       | fixed_ips |
    +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------------------------------------+
    | 51f98e51-143b-4968-a7a9-e2d8d419b246 |      | fa:16:3e:6e:63:b1 | {"subnet_id": "299d182b-2f2c-44e2-9bc9-d094b9ea317b", "ip_address": "10.0.0.2"}                             |
    |                                      |      |                   | {"subnet_id": "64bc14c2-52a6-4188-aaeb-d24922125c2c", "ip_address": "fde5:95da:6b50:0:f816:3eff:fe6e:63b1"} |
    +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------------------------------------+

..

One can determine the DHCP port by running:

``neutron port-list --device-owner 'network:dhcp'``

This will return the DHCP port that was created by Neutron.

The owner of the port, that is, the 'device_owner', will have details of the
port owner. For example the port owned by a Nova instance will have
device_owner 'compute:None' when availability zone is not set.

Booting VMs
-----------

In this section we'll go through the steps to create two VMs that have a
virtual NIC attached to the ``private`` Neutron network.

DevStack uses libvirt as the Nova backend by default.  If KVM is available, it
will be used.  Otherwise, it will just run qemu emulated guests.  This is
perfectly fine for our testing, as we only need these VMs to be able to send
and receive a small amount of traffic so performance is not very important.

1. Get the Network UUID.

Start by getting the UUID for the ``private`` network from the output of
``neutron net-list`` from earlier and save it off::

    $ PRIVATE_NET_ID=266371ca-904e-4433-b653-866f9204d22e

2. Create an SSH keypair.

Next create an SSH keypair in Nova.  Later, when we boot a VM, we'll ask that
the public key be put in the VM so we can SSH into it.

::

    $ nova keypair-add demo > id_rsa_demo
    $ chmod 600 id_rsa_demo

3. Choose a flavor.

We need minimal resources for these test VMs, so the ``m1.nano`` flavor is
sufficient.

::

    $ nova flavor-list
    +----+-----------+-----------+------+-----------+------+-------+-------------+-----------+
    | ID | Name      | Memory_MB | Disk | Ephemeral | Swap | VCPUs | RXTX_Factor | Is_Public |
    +----+-----------+-----------+------+-----------+------+-------+-------------+-----------+
    | 1  | m1.tiny   | 512       | 1    | 0         |      | 1     | 1.0         | True      |
    | 2  | m1.small  | 2048      | 20   | 0         |      | 1     | 1.0         | True      |
    | 3  | m1.medium | 4096      | 40   | 0         |      | 2     | 1.0         | True      |
    | 4  | m1.large  | 8192      | 80   | 0         |      | 4     | 1.0         | True      |
    | 42 | m1.nano   | 64        | 0    | 0         |      | 1     | 1.0         | True      |
    | 5  | m1.xlarge | 16384     | 160  | 0         |      | 8     | 1.0         | True      |
    | 84 | m1.micro  | 128       | 0    | 0         |      | 1     | 1.0         | True      |
    +----+-----------+-----------+------+-----------+------+-------+-------------+-----------+

    $ FLAVOR_ID=42

4. Choose an image.

DevStack imports the CirrOS image by default, which is perfect for our testing.
It's a very small test image.

::

    $ glance image-list
    +--------------------------------------+---------------------------------+
    | ID                                   | Name                            |
    +--------------------------------------+---------------------------------+
    | 990e80d3-5260-40c4-8ece-e5a428e1b6d7 | cirros-0.3.4-x86_64-uec         |
    | 1a76e6c3-857a-4975-bdff-1ebe6f3ce193 | cirros-0.3.4-x86_64-uec-kernel  |
    | 11fa05eb-c88a-4de7-b2f7-1da203eafc9c | cirros-0.3.4-x86_64-uec-ramdisk |
    +--------------------------------------+---------------------------------+

    $ IMAGE_ID=990e80d3-5260-40c4-8ece-e5a428e1b6d7

5. Setup a security rule so that we can access the VMs we will boot up next.

By default, DevStack does not allow users to access VMs, to enable that, we
will need to add a rule.  We will allow both ICMP and SSH.

::

    $ neutron security-group-rule-create --direction ingress --ethertype IPv4 --port-range-min 22 --port-range-max 22 --protocol tcp default
    $ neutron security-group-rule-create --direction ingress --ethertype IPv4 --protocol ICMP default
    $ neutron security-group-rule-list
    +--------------------------------------+----------------+-----------+-----------+---------------+-----------------+
    | id                                   | security_group | direction | ethertype | protocol/port | remote          |
    +--------------------------------------+----------------+-----------+-----------+---------------+-----------------+
    | 8b2edbe6-790e-40ef-af54-c7b64ced8240 | default        | ingress   | IPv4      | 22/tcp        | any             |
    | 5bee0179-807b-41d7-ab16-6de6ac051335 | default        | ingress   | IPv4      | icmp          | any             |
    ...
    +--------------------------------------+----------------+-----------+-----------+---------------+-----------------+

6. Boot some VMs.

Now we will boot two VMs.  We'll name them ``test1`` and ``test2``.

::

    $ nova boot --nic net-id=$PRIVATE_NET_ID --flavor $FLAVOR_ID --image $IMAGE_ID --key-name demo test1
    +--------------------------------------+----------------------------------------------------------------+
    | Property                             | Value                                                          |
    +--------------------------------------+----------------------------------------------------------------+
    | OS-DCF:diskConfig                    | MANUAL                                                         |
    | OS-EXT-AZ:availability_zone          | nova                                                           |
    | OS-EXT-STS:power_state               | 0                                                              |
    | OS-EXT-STS:task_state                | scheduling                                                     |
    | OS-EXT-STS:vm_state                  | building                                                       |
    | OS-SRV-USG:launched_at               | -                                                              |
    | OS-SRV-USG:terminated_at             | -                                                              |
    | accessIPv4                           |                                                                |
    | accessIPv6                           |                                                                |
    | adminPass                            | aQJMqi8vAWJP                                                   |
    | config_drive                         |                                                                |
    | created                              | 2015-05-01T01:55:27Z                                           |
    | flavor                               | m1.nano (42)                                                   |
    | hostId                               |                                                                |
    | id                                   | 571f622e-8f65-4617-9b39-6a04438f394f                           |
    | image                                | cirros-0.3.4-x86_64-uec (990e80d3-5260-40c4-8ece-e5a428e1b6d7) |
    | key_name                             | demo                                                           |
    | metadata                             | {}                                                             |
    | name                                 | test1                                                          |
    | os-extended-volumes:volumes_attached | []                                                             |
    | progress                             | 0                                                              |
    | security_groups                      | default                                                        |
    | status                               | BUILD                                                          |
    | tenant_id                            | c41f413079aa4389b7a41932cd8a6be6                               |
    | updated                              | 2015-05-01T01:55:27Z                                           |
    | user_id                              | 98978389ceb3433cb1db3f64da217ee0                               |
    +--------------------------------------+----------------------------------------------------------------+

    $ nova boot --nic net-id=$PRIVATE_NET_ID --flavor $FLAVOR_ID --image $IMAGE_ID --key-name demo test2
    +--------------------------------------+----------------------------------------------------------------+
    | Property                             | Value                                                          |
    +--------------------------------------+----------------------------------------------------------------+
    | OS-DCF:diskConfig                    | MANUAL                                                         |
    | OS-EXT-AZ:availability_zone          | nova                                                           |
    | OS-EXT-STS:power_state               | 0                                                              |
    | OS-EXT-STS:task_state                | scheduling                                                     |
    | OS-EXT-STS:vm_state                  | building                                                       |
    | OS-SRV-USG:launched_at               | -                                                              |
    | OS-SRV-USG:terminated_at             | -                                                              |
    | accessIPv4                           |                                                                |
    | accessIPv6                           |                                                                |
    | adminPass                            | HxAQk8pSi53d                                                   |
    | config_drive                         |                                                                |
    | created                              | 2015-05-01T01:55:33Z                                           |
    | flavor                               | m1.nano (42)                                                   |
    | hostId                               |                                                                |
    | id                                   | 7a8c12da-54b3-4adf-bba5-74df9fd2e907                           |
    | image                                | cirros-0.3.4-x86_64-uec (990e80d3-5260-40c4-8ece-e5a428e1b6d7) |
    | key_name                             | demo                                                           |
    | metadata                             | {}                                                             |
    | name                                 | test2                                                          |
    | os-extended-volumes:volumes_attached | []                                                             |
    | progress                             | 0                                                              |
    | security_groups                      | default                                                        |
    | status                               | BUILD                                                          |
    | tenant_id                            | c41f413079aa4389b7a41932cd8a6be6                               |
    | updated                              | 2015-05-01T01:55:33Z                                           |
    | user_id                              | 98978389ceb3433cb1db3f64da217ee0                               |
    +--------------------------------------+----------------------------------------------------------------+

Once both VMs have been started, they will have a status of ``ACTIVE``::

    $ nova list
    +--------------------------------------+-------+--------+------------+-------------+--------------------------------------------------------+
    | ID                                   | Name  | Status | Task State | Power State | Networks                                               |
    +--------------------------------------+-------+--------+------------+-------------+--------------------------------------------------------+
    | 571f622e-8f65-4617-9b39-6a04438f394f | test1 | ACTIVE | -          | Running     | private=fde5:95da:6b50:0:f816:3eff:fe92:579a, 10.0.0.3 |
    | 7a8c12da-54b3-4adf-bba5-74df9fd2e907 | test2 | ACTIVE | -          | Running     | private=fde5:95da:6b50:0:f816:3eff:fe42:cbc7, 10.0.0.4 |
    +--------------------------------------+-------+--------+------------+-------------+--------------------------------------------------------+

Our two VMs have addresses of ``10.0.0.3`` and ``10.0.0.4``.  If we list
Neutron ports again, there are two new ports with these addresses associated
with the::

    $ neutron port-list
    +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------------------------------------+
    | id                                   | name | mac_address       | fixed_ips                                                                                                   |
    +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------------------------------------+
    | 51f98e51-143b-4968-a7a9-e2d8d419b246 |      | fa:16:3e:6e:63:b1 | {"subnet_id": "299d182b-2f2c-44e2-9bc9-d094b9ea317b", "ip_address": "10.0.0.2"}                             |
    |                                      |      |                   | {"subnet_id": "64bc14c2-52a6-4188-aaeb-d24922125c2c", "ip_address": "fde5:95da:6b50:0:f816:3eff:fe6e:63b1"} |
    | d660a917-5095-4bd0-92c5-d0abdffb600b |      | fa:16:3e:42:cb:c7 | {"subnet_id": "299d182b-2f2c-44e2-9bc9-d094b9ea317b", "ip_address": "10.0.0.4"}                             |
    |                                      |      |                   | {"subnet_id": "64bc14c2-52a6-4188-aaeb-d24922125c2c", "ip_address": "fde5:95da:6b50:0:f816:3eff:fe42:cbc7"} |
    | e3800c90-24d4-49ad-abb2-041a2e3dd259 |      | fa:16:3e:92:57:9a | {"subnet_id": "299d182b-2f2c-44e2-9bc9-d094b9ea317b", "ip_address": "10.0.0.3"}                             |
    |                                      |      |                   | {"subnet_id": "64bc14c2-52a6-4188-aaeb-d24922125c2c", "ip_address": "fde5:95da:6b50:0:f816:3eff:fe92:579a"} |
    +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------------------------------------+

    $ TEST1_PORT_ID=e3800c90-24d4-49ad-abb2-041a2e3dd259
    $ TEST2_PORT_ID=d660a917-5095-4bd0-92c5-d0abdffb600b

Now we can look at OVN using ``ovn-nbctl`` to see the logical switch ports
that were created for these two Neutron ports.  The first part of the output
is the OVN logical switch port UUID.  The second part in parentheses is the
logical switch port name. Neutron sets the logical switch port name equal to
the Neutron port ID.

::

    $ ovn-nbctl lsp-list neutron-$PRIVATE_NET_ID
    1117ac4e-1c83-4fd5-bb16-6c9c11150446 (e3800c90-24d4-49ad-abb2-041a2e3dd259)
    9be0ab27-1565-4b92-b2d2-c4578e90c46d (d660a917-5095-4bd0-92c5-d0abdffb600b)
    1e81abcf-574b-4533-8202-da182491724c (51f98e51-143b-4968-a7a9-e2d8d419b246)

These three ports correspond to the DHCP agent plus the two VMs we created.

Adding Another Compute Node
---------------------------

After completing the earlier instructions for setting up devstack, you can use
a second VM to emulate an additional compute node.  This is important for OVN
testing as it exercises the tunnels created by OVN between the hypervisors.

Just as before, create a throwaway VM but make sure that this VM has a
different host name. Having same host name for both VMs will confuse Nova and
will not produce two hypervisors when you query nova hypervisor list later.
Once the VM is setup, create a user with sudo access and install git.

::

     $ git clone http://git.openstack.org/openstack-dev/devstack.git
     $ git clone http://git.openstack.org/openstack/networking-ovn.git

networking-ovn comes with another sample configuration file that can be used
for this::

     $ cd devstack
     $ cp ../networking-ovn/devstack/computenode-local.conf.sample local.conf

You must set SERVICE_HOST in local.conf.  The value should be the IP address of
the main DevStack host.  You must also set HOST_IP to the IP address of this
new host.  See the text in the sample configuration file for more
information.  Once that is complete, run DevStack::

    $ cd devstack
    $ ./stack.sh

This should complete in less time than before, as it's only running a single
OpenStack service (nova-compute) along with OVN (ovn-controller, ovs-vswitchd,
ovsdb-server).  The final output will look something like this::

    This is your host ip: 172.16.189.10
    2015-05-09 01:21:49.565 | stack.sh completed in 308 seconds.

Now go back to your main DevStack host.  You can use admin credentials to
verify that the additional hypervisor has been added to the deployment::

    $ cd devstack
    $ . openrc admin

    $ nova hypervisor-list
    +----+------------------------------------+-------+---------+
    | ID | Hypervisor hostname                | State | Status  |
    +----+------------------------------------+-------+---------+
    | 1  | ovn-devstack-1                     | up    | enabled |
    | 2  | ovn-devstack-2                     | up    | enabled |
    +----+------------------------------------+-------+---------+

You can also look at OVN and OVS to see that the second host has shown up.  For
example, there will be a second entry in the Chassis table of the
OVN_Southbound database.  You can use the ``ovn-sbctl`` utility to list
chassis, their configuration, and the ports bound to each of them::

    $ ovn-sbctl show

    Chassis "9f844100-bf55-445a-8107-8f1cba584ac5"
        Encap geneve
            ip: "172.16.189.3"
        Port_Binding "e3800c90-24d4-49ad-abb2-041a2e3dd259"
        Port_Binding "d660a917-5095-4bd0-92c5-d0abdffb600b"
        Port_Binding "51f98e51-143b-4968-a7a9-e2d8d419b246"
    Chassis "52fd2e32-f9ca-4abd-a8e4-fdf1842079d2"
        Encap geneve
            ip: "172.16.189.10"

You can also see a tunnel created to the other compute node::

    $ ovs-vsctl show

    ...

    Bridge br-int
        fail_mode: secure
        Port "ovn-90b4d4-0"
            Interface "ovn-90b4d4-0"
                type: geneve
                options: {key=flow, remote_ip="172.16.189.10"}

    ...

Provider Networks
-----------------

Neutron has a "provider networks" API extension that lets you specify
some additional attributes on a network.  These attributes let you
map a Neutron network to a physical network in your environment.
The OVN ML2 driver is adding support for this API extension.  It currently
supports "flat" and "vlan" networks.

Here is how you can test it:

First you must create an OVS bridge that provides connectivity to the
provider network on every host running ovn-controller.  For trivial
testing this could just be a dummy bridge.  In a real environment, you
would want to add a local network interface to the bridge, as well.

::

    $ ovs-vsctl add-br br-provider

ovn-controller on each host must be configured with a mapping between
a network name and the bridge that provides connectivity to that network.
In this case we'll create a mapping from the network name "providernet"
to the bridge 'br-provider".

::

    $ ovs-vsctl set open . \
    external-ids:ovn-bridge-mappings=providernet:br-provider

Now create a Neutron provider network.

::

    $ neutron net-create provider --shared \
    --provider:physical_network providernet \
    --provider:network_type flat

Alternatively, you can define connectivity to a VLAN instead of a flat network:

::

    $ neutron net-create provider-101 --shared \
    --provider:physical_network providernet \
    --provider:network_type vlan \
    --provider:segmentation_id 101

Observe that the OVN ML2 driver created a special logical switch port of type
localnet on the logical switch to model the connection to the physical network.

::

    $ ovn-nbctl show
    ...
     switch 5bbccbbd-f5ca-411b-bad9-01095d6f1316 (neutron-729dbbee-db84-4a3d-afc3-82c0b3701074)
         port provnet-729dbbee-db84-4a3d-afc3-82c0b3701074
             addresses: ["unknown"]
    ...

    $ ovn-nbctl lsp-get-type provnet-729dbbee-db84-4a3d-afc3-82c0b3701074
    localnet

    $ ovn-nbctl lsp-get-options provnet-729dbbee-db84-4a3d-afc3-82c0b3701074
    network_name=providernet

If VLAN is used, there will be a VLAN tag shown on the localnet port as well.

Finally, create a Neutron port on the provider network.

::

    $ neutron port-create provider

or if you followed the VLAN example, it would be:

::

    $ neutron port-create provider-101

Run Unit Tests
--------------
Run the unit tests in the local environment with ``tox``.

::

    $ tox -e py27
    $ tox -e py27 networking_ovn.tests.unit.test_ovn_db_sync
    $ tox -e py27 networking_ovn.tests.unit.test_ovn_db_sync.TestOvnSbSyncML2
    $ tox -e py27 networking_ovn.tests.unit.test_ovn_db_sync.TestOvnSbSyncML2
      .test_ovn_sb_sync

Run Functional Tests
--------------------
you can run the functional tests with ``tox`` in your devstack environment:

::

     $ cd networking_ovn/tests/functional
     $ tox -e dsvm-functional
     $ tox -e dsvm-functional networking_ovn.tests.functional.test_mech_driver\
       .TestPortBinding.test_port_binding_create_port

If you want to run functional tests in your local clean environment, you may
need a new working directory.

::

     $ export BASE=/opt/stack
     $ mkdir -p /opt/stack/new
     $ cd /opt/stack/new

Next, get networking_ovn, neutron and devstack.

::

     $ git clone http://git.openstack.org/openstack/networking-ovn.git
     $ git clone http://git.openstack.org/openstack/neutron.git
     $ git clone http://git.openstack.org/openstack-dev/devstack.git

Then execute the script to prepare the environment.

::

     $ cd networking-ovn/
     $ ./networking_ovn/tests/contrib/gate_hook.sh

Finally, run the functional tests with ``tox``

::

     $ cd networking_ovn/tests/functional
     $ tox -e dsvm-functional
     $ tox -e dsvm-functional networking_ovn.tests.functional.test_mech_driver\
       .TestPortBinding.test_port_binding_create_port

Skydive
-------

`Skydive <https://github.com/skydive-project/skydive>`_ is an open source
real-time network topology and protocols analyzer. It aims to provide a
comprehensive way of understanding what is happening in the network
infrastructure. Skydive works by utilizing agents to collect host-local
information, and sending this information to a central agent for
further analysis. It utilizes elasticsearch to store the data.

To enable Skydive support with OVN and devstack, enable it on the control
and compute nodes.

On the control node, enable it as follows:

::

    enable_plugin skydive https://github.com/skydive-project/skydive.git
    enable_service skydive-analyzer

On the compute nodes, enable it as follows:

::

    enable_plugin skydive https://github.com/skydive-project/skydive.git
    enable_service skydive-agent

Troubleshooting
---------------

If you run into any problems, take a look at our :doc:`troubleshooting` page.

Additional Resources
--------------------

See the documentation and other references linked from the :doc:`readme` page.
