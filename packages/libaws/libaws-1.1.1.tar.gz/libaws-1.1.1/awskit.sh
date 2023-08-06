#########################################################################
# File Name: run_upload.sh
# Author: wukan
# mail: kan.wu@genetalks.com
# Created Time: Mon 23 May 2016 01:36:35 PM CST
#########################################################################
#!/bin/bash

basepath=$(cd "$(dirname "$0")"; pwd)
env_dir=${basepath}/../
src_dir=${basepath}


source ${env_dir}/bin/activate
${env_dir}/bin/awskit $*
