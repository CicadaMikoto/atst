#!/bin/bash

# scriptz/global_header.inc: Any basic things that should be executed at the
#                            beginning of any and every script

# If any command fails, immediately exit the script
set -e

# Ensure the working directory is the app root directory
cd "$(dirname "${0}")/.."

# Source all function definition files
source ./script/include/*_functions.inc.sh
