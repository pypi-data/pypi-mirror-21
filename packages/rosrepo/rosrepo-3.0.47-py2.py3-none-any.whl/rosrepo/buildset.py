# coding=utf-8
#
# ROSREPO
# Manage ROS workspaces with multiple Gitlab repositories
#
# Author: Timo Röhling
#
# Copyright 2016 Fraunhofer FKIE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
import os
from .workspace import get_workspace_location, get_workspace_state, resolve_this
from .cache import Cache
from .config import Config
from .ui import msg, warning, fatal, escape, show_conflicts, show_missing_system_depends, reformat_paragraphs
from .resolver import find_dependees, resolve_system_depends
from .util import iteritems, is_deprecated_package, deprecated_package_info
from .cmd_git import clone_packages


def run(args):
    wsdir = get_workspace_location(args.workspace)
    config = Config(wsdir)
    cache = Cache(wsdir)
    config.set_default("default_build", [])
    config.set_default("pinned_build", [])
    set_name = "pinned_build" if args.pinned else "default_build"
    ws_state = get_workspace_state(wsdir, config, cache, offline_mode=args.offline)
    if args.last:
        args.packages = config.get("last_build", [])
    if args.this:
        args.packages = resolve_this(wsdir, ws_state)
    if args.all:
        args.packages = ws_state.ws_packages.keys()
        if args.command == "exclude":
            config[set_name] = []

    selected = set(args.packages)
    if args.command == "include":
        if not args.replace:
            selected |= set(config.get(set_name, []))
    if args.command == "exclude":
        selected = set(config.get(set_name, [])) - selected
    config[set_name] = sorted(list(selected))

    if config["pinned_build"]:
        msg("@{cf}You have pinned the following packages (they will always be built)@|:\n")
        msg(escape(", ".join(config["pinned_build"]) + "\n\n"), indent=4)

    if config["default_build"]:
        msg("@{cf}You have included the following packages in the default build@|:\n")
        msg(escape(", ".join(config["default_build"]) + "\n\n"), indent=4)
    else:
        msg("@{cf}No packages selected for the default build@|\n\n")

    if args.command == "include":
        depends, system_depends, conflicts = find_dependees(config["pinned_build"] + config["default_build"], ws_state)
        show_conflicts(conflicts)
        if conflicts:
            fatal("cannot resolve dependencies\n")

        extra_depends = set(depends.keys()) - set(config["pinned_build"]) - set(config["default_build"])
        if extra_depends:
            msg("@{cf}The following additional packages are needed to satisfy dependencies@|:\n")
            msg(escape(", ".join(sorted(extra_depends)) + "\n\n"), indent=4)

        clone_packages(os.path.join(wsdir, "src"), depends, ws_state, protocol=args.protocol or config.get("git_default_transport", "ssh"), offline_mode=args.offline, dry_run=args.dry_run)

        if system_depends:
            msg("@{cf}The following system packages are needed to satisfy dependencies@|:\n")
            msg(", ".join(sorted(system_depends)) + "\n\n", indent=4)
        missing = resolve_system_depends(ws_state, system_depends, missing_only=True)
        show_missing_system_depends(missing)

        for name, info in iteritems(depends):
            if is_deprecated_package(info.manifest):
                details = deprecated_package_info(info.manifest)
                warning("package '%s' is deprecated\n" % escape(name))
                if details:
                    msg("@{yf}" + reformat_paragraphs(escape(details)) + "\n\n", indent=4)

    if not args.dry_run:
        config.write()
    return 0
