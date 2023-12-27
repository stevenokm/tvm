#!/bin/bash
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

set -e
set -u
set -o pipefail

cd /usr
git clone https://github.com/apache/tvm.git tvm --recursive
cd /usr/tvm
# checkout a hash-tag
# git checkout 4b13bf668edc7099b38d463e5db94ebc96c80470
git checkout v0.14.0

echo set\(USE_LLVM llvm-config-16\) >> config.cmake
echo set\(USE_CUDA ON\) >> config.cmake
echo set\(USE_CUDNN ON\) >> config.cmake
echo set\(USE_CUBLAS ON\) >> config.cmake
echo set\(USE_CURAND ON\) >> config.cmake
echo set\(USE_CUTLASS ON\) >> config.cmake
echo set\(SUMMARIZE ON\) >> config.cmake
echo set\(USE_PAPI ON\) >> config.cmake
echo set\(USE_RPC ON\) >> config.cmake
echo set\(USE_GRAPH_EXECUTOR ON\) >> config.cmake
echo set\(USE_PROFILER ON\) >> config.cmake
echo set\(USE_RANDOM ON\) >> config.cmake
echo set\(USE_SORT ON\) >> config.cmake
mkdir -p build
cd build
cmake .. -DCMAKE_CUDA_ARCHITECTURES=61
# NOTE: the setting is for GTX 1080ti or later, reffer to https://developer.nvidia.com/cuda-gpus
make -j10
