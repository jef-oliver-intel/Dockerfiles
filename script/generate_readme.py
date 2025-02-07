#!/usr/bin/python3

from pathlib import Path
import re
import os
import sys

REPO_LINK = "https://github.com/OpenVisualCloud/Dockerfiles/blob/v21.3/"

#Platform to full name
platform_subs = {
                "Xeon" : "Xeon&reg; platform",
                "QAT" : "QAT platform",
                "SG1": "SG1 platform"
                }

#When image is based on another OVC image, this is used to find path of inherited image
path_subs = {
                "xeon-centos7-media-ffmpeg" : "Xeon/centos-7/media/ffmpeg/",
                "xeon-ubuntu2004-media-ffmpeg" : "Xeon/ubuntu-20.04/media/ffmpeg/",
                "xeon-centos7-media-dev" : "Xeon/centos-7/media/dev/",
                "xeon-ubuntu2004-media-dev" : "Xeon/ubuntu-20.04/media/dev/",
                }

#OS subs to their version detail 
os_subs = {
                "centos-7" : "CentOS-7",
                "ubuntu-20.04" : "Ubuntu 20.04"
          }

#included components links
included_subs = {
                "nginx" : ["[NGINX](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/nginx.md)"],
                "svt" : ["[SVT](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/svt.md)"],
                "owt" : ["[OWT](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/owt.md)"],
                "owt360" : ["[OWT360](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/owt360.md)"],
                "ffmpeg" : ["[FFmpeg](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/ffmpeg.md)"],
                "ffmpeg-vmaf" : ["[FFmpeg](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/ffmpeg.md)"],
                "gst" : ["[GStreamer](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/gst.md)"],
                "dev" : ["[FFmpeg](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/ffmpeg.md)","[GStreamer](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/gst.md)"]
                }

# License to be included based on m4 templates
license_subs = {
                "xeon-centos7-media-ffmpeg" : "Xeon/centos-7/media/ffmpeg/",
                "xeon-ubuntu2004-media-ffmpeg" : "Xeon/ubuntu-20.04/media/ffmpeg/",
                "xeon-centos7-media-dev" : "Xeon/centos-7/media/dev/",
                "xeon-ubuntu2004-media-dev" : "Xeon/ubuntu-20.04/media/dev/"
                }

#OS subs to their version detail 
os_subs = {
                "centos-7" : "CentOS-7",
                "ubuntu-20.04" : "Ubuntu 20.04"
          }

#included components links
included_subs = {
                "nginx" : ["[NGINX](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/nginx.md)"],
                "svt" : ["[SVT](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/svt.md)"],
                "owt" : ["[OWT](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/owt.md)"],
                "owt360" : ["[OWT360](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/owt360.md)"],
                "ffmpeg" : ["[FFmpeg](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/ffmpeg.md)"],
                "gst" : ["[GStreamer](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/gst.md)"],
                "dev" : ["[FFmpeg](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/ffmpeg.md)","[GStreamer](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/gst.md)"]
                }

# License to be included based on m4 templates
license_subs = {
                "dav1d" : ["|dav1d|BSD 2-clause \"Simplified\" License|"],
                "dldt-ie" : ["|OpenVINO|Apache License v2.0|"],
                "ffmpeg" : ["|FFmpeg|GNU Lesser General Public License v2.1 or later|"],
                "gmmlib" : ["|Intel Graphics Memory Management Library| MIT License|"],
                "gmmlib.sg1" : ["|Intel Graphics Memory Management Library| MIT License|"],
                "gst-core" : ["|gstreamer|GNU Lesser General Public License v2.1 or later|"],
                "gst-plugins-base" : ["|gst plugins base|GNU Lesser General Public License v2.1 or later|"],
                "gst-plugins-bad" : ["|gst plugins bad|GNU Lesser General Public License v2.1 or later|"],
                "gst-plugins-good" : ["|gst plugins good|GNU Lesser General Public License v2.1 or later|"],
                "gst-libav" : ["|gst libav|GNU Library General Public License Version 2.1 or later|"],
                "gst-python" : ["|gst python|GNU Library General Public License Version 2.1|"],
                "gst-svt" : ["|gst svt|GNU Lesser General Public License v2.1 or later|"],
                "gst-plugins-ugly" : ["|gst plugins ugly|GNU Lesser General Public License v2.1 or later|"],
                "gst-vaapi" : ["|gst vaapi|GNU Lesser General Public License v2.1 or later|"],
                "gst-gva" : ["|gst video analytics|MIT License|"],
                "hddl-openvino" : ["|openvino|End User License Agreement for the Intel(R) Software Development Products|"],
                "libaom" : ["|Aomedia AV1 Codec Library|BSD 2-clause \"Simplified\" License|"],
                "libdrm" : ["|libdrm|MIT license|"],
                "libjsonc" : ["|json-c|MIT License|"],
                "libnice014" : ["|libnice|GNU Lesser General Public License|"],
                "libogg" : ["|libogg|BSD 3-clause \"New\" or \"Revised\" License|"],
                "libopus" : ["|Opus Interactive Audio Codec|BSD 3-clause \"New\" or \"Revised\" License|"],
                "librdkafka" : ["|librdkafka|BSD 2-clause \"Simplified\" License|"],
                "libpahomqtt" : ["|paho.mqtt.c|Eclipse Public License - v 2.0|"],
                "libre" : ["|libre|BSD 3-clause License|"],
                "libsrtp2" : ["|libsrtp2|BSD 3-clause License|"],
                "libva2" : ["|Intel libva| MIT License"],
                "libva2.sg1" : ["|Intel libva| MIT License"],
                "libvorbis" : ["|libvorbis|BSD 3-clause \"New\" or \"Revised\" License|"],
                "libvpx" : ["|libvpx|BSD 3-clause \"New\" or \"Revised\" License|"],
                "libx264" : ["|x264|GNU General Public License v2.0 or later|"],
                "libx265" : ["|x265|GNU General Public License v2.0 or later|"],
                "libvmaf" : ["|libvmaf|BSD-2-Clause Plus Patent License|"],
                "media-driver" : ["|Intel media driver | MIT License|"],
                "media-driver.sg1" : ["|Intel media driver | MIT License|"],
                "msdk" : ["|Intel media SDK|MIT License|"],
                "msdk.sg1" : ["|Intel media SDK|MIT License|"],
                "nginx-flv" : ["|nginx http flv|BSD 2-clause \"Simplified\" License|"],
                "nginx" : ["|nginx|BSD 2-clause \"Simplified\" License|"],
                "nginx-upload" : ["|nginx upload module|BSD 3-clause \"Simplified\" License|"],
                "nodetools" : ["|nodejs| MIT Open Source License|"],
                "opencl" : ["|Intel opencl | MIT License|"],
                "opencv" : ["|OpenCV|BSD 3-clause \"New\" or \"Revised\" License|"],
                "openssl" : ["|OpenSSL|Apache License 2.0|"],
                "openvino" : ["|OpenVINO|End User License Agreement for the Intel(R) Software Development Products|"],
                "owt360" : ["|owt-server|Apache License v2.0|","|owt-sdk|Apache License v2.0|","|owt-deps-webrtc|BSD 3-clause License|"],
                "owt" : ["|owt-server|Apache License v2.0|","|owt-sdk|Apache License v2.0|","|owt-deps-webrtc|BSD 3-clause License|"],
                "owt-gst-base" : ["|gst plugins base|GNU Lesser General Public License v2.1 or later|"],
                "owt-gst-bad" : ["|gst plugins bad|GNU Lesser General Public License v2.1 or later|"],
                "owt-gst-good" : ["|gst plugins good|GNU Lesser General Public License v2.1 or later|"],
                "owt-gst-gva" : ["|gst video analytics|MIT License|"],
                "owt-gst-ugly" : ["|gst plugins ugly|GNU Lesser General Public License v2.1 or later|"],
                "qat-cryptomb" : ["|ipp crypo|Apache-2.0 License|"],
                "qat-engine" : ["|QAT OpenSSL engine|BSD 3-clause \"New\" or \"Revised\" License|"],
                "qat-nginx" : ["|asynch mode nginx |BSD 3-clause \"New\" or \"Revised\" License|"],
                "qat-openssl" : ["|OpenSSL|Apache License 2.0|"],
                "qat-zip" : ["|QATzip|BSD 3-clause \"New\" or \"Revised\" License|"],
                "scvp" : ["|360SCVP|BSD 3-clause \"New\" or \"Revised\" License|"],
                "srs" : ["|Simple Realtime Server|MIT License|"],
                "svt-av1" : ["|Intel SVT-AV1|BSD-2-Clause Plus Patent License|"],
                "svt-hevc.1-3-0" : ["|Intel SVT-HEVC|BSD-2-Clause Plus Patent License|"],
                "svt-hevc" : ["|Intel SVT-HEVC|BSD-2-Clause Plus Patent License|"],
                "svt-vp9" : ["|Intel SVT-VP9|BSD-2-Clause Plus Patent License|"],
                "usrsctp" : ["|usrsctp|BSD 3-clause \"New\" or \"Revised\" License|"],
               }

# M4 files for which no license is needed
license_exclude = ['automake', 'build-tools', 'build-tools-hddl', 'build-tools-hddl-layer', 'cleanup', 'cmake', 'install', 'install.pkgs', 'install.pkgs.owt', 'libfdk-aac', 'libmp3lame', 'nasm', 'nginx-cert', 'nginx-conf', 'qat-core', 'transform360', 'yasm', 'libva-utils', 'libusb','begin','end','ubuntu', 'centos-repo','ipsecmb','meson','boost']

# Find image platform / OS / image type / image name from file path
def parse_ingredients(path):
    path_components = path.split('/')
    image_name = path_components[-1]
    image_type = path_components[-2]
    image_os = path_components[-3]
    image_platform = path_components[-4]
    return [image_platform, image_os, image_type, image_name]

#method that generates URL placeholder for link to DOckerfiles
def url_generator(local_path, image_name, image_type, image_os, image_platform):
    url = ' - ['+image_platform.lower()+'-'+image_os.lower().replace('.','')+'-'+image_type.lower()+'-'+image_name.lower()+']('+REPO_LINK+local_path.split('Dockerfiles/')[1]+'/Dockerfile'+')'
    return url

# Generate links to docs of included components
def included_components(image_name):
    print("Included Components")
    print(image_name)
    included_holder = ''
    if image_name in included_subs:
        print("Inside IF")
        print(image_name)
        included_holder += "- #### Usage instructions:\n  "
        for comp in included_subs[image_name]:
            included_holder += comp
            included_holder += '\t'
    included_holder += '\n\n'
    return included_holder
    
# Generate quick reference part of README
def quick_reference(local_path, image_name, image_type, image_os, image_platform):
    print("In quick_reference")
    print(image_name)
    text_holder = "## Quick reference\n"
    text_holder += "- #### Supported platform and OS\n"
    text_holder += "  Intel&reg; "+platform_subs[image_platform]+", "+os_subs[image_os]
    text_holder += "\n\n"
    text_holder += included_components(image_name)
    text_holder +="""
- #### Getting started with Dockerfiles:
  [OpenVisualCloud Dockerfiles Wiki](https://github.com/OpenVisualCloud/Dockerfiles/wiki)

- #### File issues:
  [OpenVisualCloud Dockerfiles Issues](https://github.com/OpenVisualCloud/Dockerfiles/issues)
"""
    text_holder += "\n\n"
    return text_holder

# Populate license info based on if the image is based of another image
def inheritance_populate(handler_list, inherited_file_path):
    inherited_entry_holder = ''
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'+inherited_file_path+'/Dockerfile.m4', 'r') as fh:
        line = fh.readline()
        while line:
            if 'm4' in line:
                m = re.search('[a-zA-Z0-9\-\.\_]+.m4', line)
                if m:
                    handler = (m.group(0).split('.m4')[0])
                    if handler not in license_exclude and handler not in handler_list:
                        for license_entry in license_subs[handler]:
                            inherited_entry_holder += license_entry
                            inherited_entry_holder += '\n'
            line = fh.readline()
    return inherited_entry_holder

def parse_inherited_file(inherited_file,image_os):
   parsed_inherited_file = ''
   image_os1 = image_os.replace("-","").replace(".","")
   parsed_inherited_file = inherited_file.replace("OS_NAME`'patsubst(OS_VERSION,\\.)", image_os1)
   return parsed_inherited_file

# Parse M4 to populate license info
def parse_m4(local_path,image_os):
    entry_holder = ''
    os_flag = False
    ovc_inheritance_flag = False
    handler_list = []
    with open(local_path+'/Dockerfile.m4', 'r') as fp:
        line = fp.readline()
        while line:
            if 'ubuntu' in image_os and not os_flag:
                entry_holder += '|Ubuntu| [Various](https://hub.docker.com/_/ubuntu) |'
                entry_holder += '\n'
                os_flag = True
            elif 'centos' in image_os and not os_flag:
                entry_holder += '|CentOS| [Various](https://hub.docker.com/_/centos) |'
                entry_holder += '\n'
                os_flag = True
            elif 'FROM openvisualcloud' in line and not ovc_inheritance_flag:
                inherited_file = line.split('/')[1].split(':')[0]
                inherited_file_1 = parse_inherited_file(inherited_file,image_os)
                entry_holder += inheritance_populate(handler_list, path_subs[inherited_file_1])
                ovc_inheritance_flag = True
            if 'm4' in line:
                m = re.search('[a-zA-Z0-9\-\.\_]+.m4', line)
                if m:
                    handler = (m.group(0).split('.m4')[0])
                    handler_list.append(handler)
                    if handler not in license_exclude:
                        for license_entry in license_subs[handler]:
                            entry_holder += license_entry
                            entry_holder += '\n'
            line = fp.readline()
    return entry_holder

# Main method
def generate_license(local_path, image_name, image_type, image_os, image_platform):
    text_holder = """## License
This docker installs third party components licensed under various open source licenses.  The terms under which those components may be used and distributed can be found with the license document that is provided with those components.  Please familiarize yourself with those terms to ensure your distribution of those components complies with the terms of those licenses.\n\n
"""
    text_holder += "| Components | License |\n"
    text_holder += "| ----- | ----- |\n"
    text_holder += parse_m4(local_path, image_os) 
    text_holder += "\n\n"
    text_holder += """More license information can be found in [components source package](https://github.com/OpenVisualCloud/Dockerfiles-Resources).   
As for any pre-built image usage, it is the image user's responsibility to ensure that any use of this image complies with any relevant licenses and potential fees for all software contained within. We will have no indemnity or warranty coverage from suppliers.
"""
    return text_holder

def create_readme(path, path_components):
    my_file = open(path+"/README.md","w")
    my_file.write("This docker image is part of Open Visual Cloud software stacks. ")
    image_name = path_components[3]
    print("In Create Readme")
    print(image_name)
    image_type = path_components[2]
    image_os = path_components[1]
    image_platform = path_components[0]
 
    if image_platform=="QAT":
        my_file.write("Optimized for NGINX web server with compute-intensive operations acceleration with Intel® QuickAssist Technology (Intel® QAT).The docker image can be used in the FROM field of a downstream Dockerfile.")
    elif image_name=="dev":
        my_file.write("This is development image aim towards enabling C++ application compilation, debugging (with the debugging, profiling tools) and optimization (with the optimization tools.) You can compile C++ applications with this image and then copy the applications to the corresponding deployment image. ")
        if image_type=="analytics":
            my_file.write("Included what are in FFmpeg & GStreamer media analytics images. ")
        if image_type=="media":
            my_file.write("Included what are in FFmpeg or GStreamer media creation and delivery images . ")
        if image_platform=="SG1":
            my_file.write("Also included Intel hardware accelaration software stack such as media SDK, media driver, gmmlib and libva. ")
        my_file.write("The docker image can be used in the FROM field of a downstream Dockerfile. ")
    elif image_type=="analytics":
        my_file.write("Optimized for Media Analytics. ")
        if image_name=="gst":
            my_file.write("Included what are in media delivery GStreamer image, inferencing engine and video analytics plugins. ")
        if image_name=="ffmpeg":
            my_file.write("Included what are in media delivery FFmpeg image, inferencing engine and video analytics plugins. ")
        if image_name=="hddldaemon":
            my_file.write("With OpenVINO HDDL daemon installed and configured. ")
        if image_platform=="SG1" and image_name!="hddldaemon":
            my_file.write("Also included Intel hardware accelaration software stack such as media SDK, media driver, opencl, gmmlib and libva. ")
        my_file.write("The docker image can be used in the FROM field of a downstream Dockerfile. ")
    elif image_type=="media":
        my_file.write("Optimized for the media creation and delivery use case. ")
        if image_name=="gst":
            my_file.write("Included gstreamer and audio and video plugins that can be connected to process audio and video content, such as creating, converting, transcoding. ")
        if image_name=="ffmpeg":
            my_file.write("Included FFmpeg and codecs such as opus, ogg, vorbis, x264, x265, vp8/9, av1 and SVT-HEVC. ")
        if image_name=="ffmpeg-vmaf":
            my_file.write("Included FFmpeg and codecs such as opus, ogg, vorbis, x264, x265, vp8/9, av1 and SVT-HEVC. It also includes libvmaf for video quality assessment.")
        if image_name=="nginx":
            my_file.write("Optimized for NGINX web server that can be used for serving web content, load balancing, HTTP caching, or a reverse proxy. ")
        if image_name=="svt":
            my_file.write("Image with SVT (Scalable Video Technology) Encoder and decoders. Ready to use SVT apps to try AV1, HEVC, VP9 transcoders. ")
        if image_name=="srs":
            my_file.write("Image with SRS high efficiency, stable and simple RTMP/HLS/FLV streaming cluster. ")
        if image_platform=="SG1":
            my_file.write("Also included Intel hardware accelaration software stack such as media SDK, media driver, gmmlib and libva. ")
        my_file.write("The docker image can be used in the FROM field of a downstream Dockerfile. ")
    elif image_type=="service":
        my_file.write("Optimized for video conferencing service based on the WebRTC technology and Open WebRTC Toolkit (OWT). ")
        if image_name=="owt":
            my_file.write("Optimized for video conferencing service based on the WebRTC technology and Open WebRTC Toolkit (OWT). Included conferencing modes: 1:N, N:N with video and audio processing nodes. ")
        if image_name=="owt360":
            my_file.write("Docker image optimized for ultra-high resolution immersive video low latency streaming, based on the WebRTC technology and the Open WebRTC Toolkit. Included SVT-HEVC tile-based 4K and 8K transcoding and field of view (FoV) adaptive streaming. ")
        my_file.write("The docker image can be used in the FROM field of a downstream Dockerfile. ")

    my_file.write("\n\n")
    my_file.write("## Supported tags and respective Dockerfile links\n")
    my_file.write(url_generator(path, image_name, image_type, image_os, image_platform))
    my_file.write("\n\n")
    my_file.write(quick_reference(path, image_name, image_type, image_os, image_platform))
    my_file.write(generate_license(path, image_name, image_type, image_os, image_platform))
    my_file.close()

if len(sys.argv)<1:
    print("Usage: <README path>\n")
    exit(1)

path=sys.argv[1]
path1=path.split('/')
create_readme(path, parse_ingredients(path))
