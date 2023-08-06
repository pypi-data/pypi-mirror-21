import sys
import time
import argparse
import os
from functools import wraps
import inspect
import infrasim.model as model
from infrasim.init import infrasim_init
from infrasim.version import version
import infrasim.helper as helper
from infrasim.config_manager import NodeMap
from infrasim import InfraSimError
from infrasim.workspace import Workspace
from texttable import Texttable

nm = NodeMap()


def args(*args, **kwargs):
    def _decorator(func):
        func.__dict__.setdefault('args', []).insert(0, (args, kwargs))
        return func
    return _decorator


def node_workspace_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe()
        frame_args, _, _, values = inspect.getargvalues(frame)
        node_name = values["args"][1]
        if not Workspace.check_workspace_exists(node_name):
            print "Node {} runtime workspace doesn't exist".format(node_name)
            return
        return func(*args, **kwargs)
    return wrapper


class ConfigCommands(object):
    @args("node_name", help="Specify node name to add configuration mapping")
    @args("config_file", help="Node Config File Path")
    def add(self, node_name, config_file):
        try:
            nm.add(node_name, config_file)
        except InfraSimError, e:
            print e.value

    @args("node_name", help="Specify node name to delete configuration mapping")
    def delete(self, node_name):
        try:
            nm.delete(node_name)
        except InfraSimError, e:
            print e.value

    @args("node_name", help="Specify node name to update configuration mapping")
    @args("config_file", help="Node Config File Path")
    def update(self, node_name, config_file):
        try:
            nm.update(node_name, config_file)
        except InfraSimError, e:
            print e.value

        if Workspace.check_workspace_exists(node_name):
            print "Node {0} runtime workspace exists.\n" \
                  "If you want to apply updated configuration, please destroy node runtime workspace first.\n" \
                  "You can run commands: \n" \
                  "    infrasim node destroy {0}\n" \
                  "    infrasim node start {0}".format(node_name)

    @args("node_name", nargs='?', default="default",
          help="Specify node name to open its configuration in editor")
    def edit(self, node_name):
        if node_name not in nm.get_name_list():
            print "Fail to find node {0} configuration. It is not registered. Check by:\n" \
                  "    infrasim config list".format(node_name)
            return

        editor = os.environ.get('EDITOR', 'vi')
        config_path = os.path.join(nm.get_mapping_folder(),
                                   "{}.yml".format(node_name))
        try:
            os.system("{} {}".format(editor, config_path))
        except OSError, e:
            print e

    def list(self):
        try:
            nm.list()
        except InfraSimError, e:
            print e.value


class NodeCommands(object):

    def _node_preinit(self, node, ignore_check=False):
        node.init()

        if ignore_check:
            return

        node.precheck()

    @args("node_name", nargs='?', default="default", help="Specify node name to start")
    def start(self, node_name):
        try:
            if Workspace.check_workspace_exists(node_name):
                node_info = Workspace.get_node_info_in_workspace(node_name)
            else:
                node_info = nm.get_node_info(node_name)
            node = model.CNode(node_info)
            self._node_preinit(node)
        except InfraSimError, e:
            print e.value
            return

        node.start()

        vnc_port = node_info["compute"].get("vnc_display", 1) + 5900

        # get IP address
        print "Infrasim service started.\n" \
            "Node {} graphic interface accessible via: \n" \
            "VNC port: {} \n" \
            "Either host IP: {} \n" \
            "depending on host in which network VNC viewer is running". \
            format(node.get_node_name(), vnc_port, helper.ip4_addresses(netns=node_info.get("namespace")))

    @node_workspace_exists
    @args("node_name", nargs='?', default="default", help="Specify node name to stop")
    def stop(self, node_name):
        try:
            node_info = Workspace.get_node_info_in_workspace(node_name)
            node = model.CNode(node_info)
            self._node_preinit(node, ignore_check=True)
            node.stop()
        except InfraSimError, e:
            print e.value
            return

    @node_workspace_exists
    @args("node_name", nargs='?', default="default", help="Specify node name to restart")
    def restart(self, node_name):
        self.stop(node_name)
        time.sleep(0.5)
        self.start(node_name)

    @node_workspace_exists
    @args("node_name", nargs='?', default="default", help="Specify node name to check status")
    def status(self, node_name):
        try:
            node_info = Workspace.get_node_info_in_workspace(node_name)
            node = model.CNode(node_info)
            self._node_preinit(node, ignore_check=True)
            node.status()
        except InfraSimError, e:
            print e.value

    @args("node_name", nargs='?', default="default", help="Specify node name to destroy")
    def destroy(self, node_name):
        if Workspace.check_workspace_exists(node_name):
            try:
                node_info = Workspace.get_node_info_in_workspace(node_name)
            except InfraSimError, e:
                print e.value
                return
        else:
            print "Node {} runtime workspace is not found, destroy action is not applied.".\
                format(node_name)
            return
        node = model.CNode(node_info)
        try:
            self._node_preinit(node, ignore_check=True)
            node.stop()
        except InfraSimError, e:
            print e.value
        node.terminate_workspace()

    @node_workspace_exists
    @args("node_name", nargs='?', default="default", help="Specify node name to get information")
    def info(self, node_name, type=True):
        try:
            node_info = Workspace.get_node_info_in_workspace(node_name)
            node_info_net = node_info['compute']['networks']
            node_info_stor = node_info['compute']['storage_backend']

            print "{:<20}{}\n" \
                  "{:<20}{}\n" \
                  "{:<20}{}\n" \
                  "{:<20}{}\n" \
                  "{:<20}{}\n" \
                  "{:<20}{}" . \
                format("node name:", node_name,
                       "type:", node_info['type'],
                       "memory size:", node_info['compute']['memory']['size'],
                       "sol_enable:", node_info['sol_enable'],
                       "cpu quantities:", node_info['compute']['cpu']['quantities'],
                       "cpu type:", node_info['compute']['cpu']['type'])
            print "{:<20}".format("network(s):") + "-" * 22
            table = Texttable()
            table_type = ~(Texttable.HEADER | Texttable.BORDER | Texttable.HLINES | Texttable.VLINES)
            table.set_deco(table_type)
            table.set_cols_align(["l", "l", "l", "l"])
            row = []
            row.append([" " * 17, "device", "mode", "name"])
            for i in range(1, len(node_info_net) + 1):
                net = node_info_net[i-1]
                row.append([" " * 17, net['device'], net['network_mode'], net['network_name']])
            table.add_rows(row)
            print table.draw()

            print "{:<20}".format("storage backend:") + "-" * 30
            table = Texttable()
            table.set_deco(table_type)
            table.set_cols_align(["l", "l", "l", "l"])
            row = []
            row.append([" " * 17, "type", "max drive", "drive size"])
            for i in range(1, len(node_info_stor) + 1):
                stor = node_info_stor[i - 1]
                node_info_drives = stor['drives']
                for j in range(1, len(node_info_drives) + 1):
                    drive = node_info_drives[j - 1]
                    if j == 1:
                        row.append([" " * 17, stor['type'],
                                    stor['max_drive_per_controller'], drive['size']])
                    else:
                        row.append([" " * 17, "", "", drive['size']])
            table.add_rows(row)
            print table.draw()

        except InfraSimError, e:
            print e.value
            return


class ChassisCommands(object):
    @args("node_name", nargs='?', help="Node name")
    def start(self, node_name=None):
        print node_name

    @args("node_name", nargs='?', help="Node name")
    def stop(self, node_name=None):
        print node_name

    @args("node_name", nargs='?', help="Node name")
    def restart(self, node_name=None):
        print node_name

    @args("node_name", nargs='?', help="Node name")
    def destroy(self, node_name=None):
        print node_name


def methods_of(obj):
    result = []
    for i in dir(obj):
        if callable(getattr(obj, i)) and not i.startswith('_'):
            result.append((i, getattr(obj, i)))
    return result


def get_arg_string(args):
    args = args.strip('-')

    if args:
        args = args.replace('-', '_')

    return args


def get_func_args(func, matchargs):
    fn_args = []
    for args, kwargs in getattr(func, 'args', []):
        # The for loop is for supporting short and long options
        for arg in args:
            try:
                arg = kwargs.get('dest') or get_arg_string(args[0])
                parm = getattr(matchargs, arg)
            except AttributeError:
                continue

            fn_args.append(parm)

            # If we already got one params for fn, then exit loop.
            if len(fn_args) > 0:
                break

    return fn_args


CATEGORIES = {
    'node': NodeCommands,
    'chassis': ChassisCommands,
    'config': ConfigCommands
}


def add_command_parsers(subparser):
    for category in CATEGORIES:
        command_object = CATEGORIES[category]()

        parser = subparser.add_parser(category)
        parser.set_defaults(command_object=command_object)

        category_subparsers = parser.add_subparsers(dest="action")

        for (action, action_fn) in methods_of(command_object):
            parser = category_subparsers.add_parser(action)

            action_kwargs = []
            for args, kwargs in getattr(action_fn, 'args', []):
                parser.add_argument(*args, **kwargs)
                parser.set_defaults(dest="dest")

            parser.set_defaults(action_fn=action_fn)
            parser.set_defaults(action_kwargs=action_kwargs)


def command_handler():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="InfraSIM Commands:")
    add_command_parsers(subparsers)

    # for init command
    init_parser = subparsers.add_parser("init", help="init infrasim environment")
    init_parser.set_defaults(init="init")
    init_parser.add_argument("-s", "--skip-installation", action="store_true",
                             help="Ignore qemu/openipmi package installation")
    init_parser.add_argument("-f", "--force", action="store_true", 
                            help="Destroy existing Nodes")
    init_parser.add_argument("-i", "--infrasim-home", action="store",
                             help="Target infrasim home foler, default $HOME/.infrasim")
    exclusive_group = init_parser.add_mutually_exclusive_group()
    exclusive_group.add_argument("-c", "--config-file", action="store", help="Node configuration file")
    exclusive_group.add_argument("-t", "--type", action="store", default="quanta_d51", help="Node type")

    # version command
    version_parser = subparsers.add_parser("version", help="check version of infrasim and dependencies")
    version_parser.set_defaults(version="version")

    args = parser.parse_args(sys.argv[1:])
    if hasattr(args, "init"):
        # Do init
        infrasim_init(args.type, args.skip_installation, args.force, args.infrasim_home, args.config_file)
    elif hasattr(args, "version"):
        # Print version
        print version()
    else:
        fn = args.action_fn

        fn_args = get_func_args(fn, args)

        # Handle the command
        fn(*fn_args)
