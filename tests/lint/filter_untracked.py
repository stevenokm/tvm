#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import os.path
import subprocess
import sys


def main():
    script_dir = os.path.dirname(__file__) or os.getcwd()
    toplevel_dir = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=script_dir, encoding="utf-8"
    ).strip("\n")
    # NOTE: --ignore-submodules because this can drag in some problems related to mounting a git
    # worktree in the docker VM in a different location than it exists on the host. The problem
    # isn't quite clear, but anyhow it shouldn't be necessary to filter untracked files in
    # submodules here.
    git_status_output = subprocess.check_output(
        ["git", "status", "-s", "--ignored"], encoding="utf-8", cwd=toplevel_dir
    )
    untracked = [
        line[3:]
        for line in git_status_output.split("\n")
        if line.startswith("?? ") or line.startswith("!! ")
    ]

    # also add .git in case rat picks up files in .git or the .git file (if a worktree).
    toplevel_git_dentry = os.path.join(toplevel_dir, ".git")
    if os.path.isfile(toplevel_git_dentry):
        untracked.append(".git")
    else:
        untracked.append(".git/")

    for line in sys.stdin:
        cleaned_line = line
        if line[:2] == "./":
            cleaned_line = line[2:]
        cleaned_line = cleaned_line.strip("\n")
        if any(
            (cleaned_line.startswith(u) if u[-1] == "/" else cleaned_line == u) for u in untracked
        ):
            continue

        sys.stdout.write(line)


if __name__ == "__main__":
    main()
