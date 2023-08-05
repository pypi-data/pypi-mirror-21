# Copyright 2017 Bracket Computing, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# https://github.com/brkt/brkt-cli/blob/master/LICENSE
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and
# limitations under the License.
import argparse


def setup_wrap_with_vcenter_args(parser):
    parser.add_argument(
        'vmdk',
        metavar='VMDK-NAME',
        help='The Guest VMDK path (in the datastore) that will be encrypted'
    )
    parser.add_argument(
        "--vcenter-host",
        help="IP address/DNS Name of the vCenter host",
        dest="vcenter_host",
        metavar='DNS_NAME',
        required=True)
    parser.add_argument(
        "--vcenter-port",
        help="Port Number of the vCenter Server",
        metavar='N',
        dest="vcenter_port",
        default="443",
        required=False)
    parser.add_argument(
        "--vcenter-datacenter",
        help="vCenter Datacenter to use",
        dest="vcenter_datacenter",
        metavar='NAME',
        default=None,
        required=False)
    parser.add_argument(
        "--vcenter-datastore",
        help="vCenter datastore to use",
        dest="vcenter_datastore",
        metavar='NAME',
        default=None,
        required=False)
    parser.add_argument(
        "--vcenter-cluster",
        help="vCenter cluster to use",
        dest="vcenter_cluster",
        metavar='NAME',
        default=None,
        required=False)
    parser.add_argument(
        "--vcenter-network-name",
        help="vCenter network name to use",
        dest="network_name",
        metavar='NAME',
        default="VM Network",
        required=False)
    parser.add_argument(
        "--cpu-count",
        help="Number of CPUs to assign to Encryptor VM",
        metavar='N',
        dest="no_of_cpus",
        default="8",
        required=False)
    parser.add_argument(
        "--memory",
        help="Memory to assign to Encryptor VM",
        metavar='GB',
        dest="memory_gb",
        default="32",
        required=False)
    parser.add_argument(
        '--vm-name',
        metavar='NAME',
        dest='vm_name',
        help='Specify the name of the launched VM',
        required=False
    )
    parser.add_argument(
        '--no-verify-cert',
        dest='validate',
        action='store_false',
        default=True,
        help="Don't validate vCenter certificate"
    )
    parser.add_argument(
        '--ovf-source-directory',
        metavar='PATH',
        dest='source_image_path',
        help='Local path to the OVF directory',
        default=None,
        required=False
    )
    parser.add_argument(
        '--metavisor-ovf-image-name',
        metavar='NAME',
        dest='image_name',
        help='Metavisor OVF name',
        default=None,
        required=False
    )
    parser.add_argument(
        '--disk-type',
        metavar='TYPE',
        dest='disk_type',
        help='thin/thick-lazy-zeroed/thick-eager-zeroed (default: thin)',
        default='thin',
        required=False
    )

    # Optional HTTP Proxy argument which can be used in proxied environments
    # Specifies the HTTP Proxy to use for S3/AWS connections
    parser.add_argument(
        '--http-s3-proxy',
        dest='http_proxy',
        metavar='HOST:PORT',
        default=None,
        help=argparse.SUPPRESS
    )
    # Optional VMDK that's used to launch the encryptor instance.  This
    # argument is hidden because it's only used for development.
    parser.add_argument(
        '--encryptor-vmdk',
        metavar='VMDK-NAME',
        dest='encryptor_vmdk',
        help=argparse.SUPPRESS
    )
    # Optional ssh-public key to be put into the Metavisor.
    # Use only with debug instances.
    # Hidden because it is used only for development.
    parser.add_argument(
        '--ssh-public-key',
        metavar='PATH',
        dest='ssh_public_key_file',
        default=None,
        help=argparse.SUPPRESS
    )
    # Optional bucket-name in case dev/qa need to use
    # other internal buckets to fetch the MV image from
    parser.add_argument(
        '--bucket-name',
        metavar='NAME',
        dest='bucket_name',
        help=argparse.SUPPRESS,
        default="solo-brkt-prod-ovf-image"
    )
    # Optional nic-type to be used with VDS
    # Values can be Port, VirtualPort or VirtualPortGroup
    parser.add_argument(
        '--nic-type',
        metavar='NAME',
        dest='nic_type',
        help=argparse.SUPPRESS,
        default="Port"
    )
    # Optional argument to keep the downloaded artifacts. Can we used in
    # cases where the same (downloaded) OVF is used for multiple
    # encryption/update jobs
    parser.add_argument(
        '--no-cleanup',
        dest='cleanup',
        default=True,
        action='store_false',
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--guest-fqdn',
        metavar='FQDN',
        dest='guest_fqdn',
        help=argparse.SUPPRESS
    )
