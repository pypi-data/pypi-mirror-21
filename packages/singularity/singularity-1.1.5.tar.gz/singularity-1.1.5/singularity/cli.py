#!/usr/bin/env python

'''
cli.py: part of singularity package

Last updated: Singularity version 2.1

The MIT License (MIT)

Copyright (c) 2016-2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from singularity.utils import (
    getsudo, 
    run_command, 
    check_install, 
    write_json, 
    write_file
)

from singularity.logman import bot

from glob import glob
import subprocess
import tempfile
import shutil
import json
import os
import re

class Singularity:
    

    def __init__(self,sudo=False,sudopw=None,debug=False,quiet=False):
       '''upon init, store user password to not ask for it again'''

       self.sudopw = sudopw
       self.debug = debug

       # Try getting from environment
       if self.sudopw == None:
           self.sudopw = os.environ.get('pancakes',None)

       if sudo == True and self.sudopw == None:
           self.sudopw = getsudo()


    def run_command(self,cmd,sudo=False,suppress=False):
        '''run_command is a wrapper for the global run_command, checking first
        for sudo (and asking for it to store) if sudo is needed.
        :param cmd: the command to run
        :param sudo: does the command require sudo?
        :param suppress: run os.system instead of os.popen if sudo required
        '''
        if sudo==True:
            if self.sudopw == None:
                self.sudopw = getsudo()
            output = run_command(cmd,sudopw=self.sudopw,suppress=suppress)
        else:
            output = run_command(cmd,suppress=suppress) # suppress doesn't make difference here
        return output



    def help(self,command=None,stdout=True):
        '''help prints the general function help, or help for a specific command
        :param command: the command to get help for, if none, prints general help
        '''
        cmd = ['singularity','--help']
        if command != None:
            cmd.append(command)
        help = self.run_command(cmd)

        if isinstance(help,bytes):
            help = help.decode('utf-8')

        # Print to console, or return string to user
        if stdout == True:
            print(help)
        else:
            return help


    def println(self,output):
        '''print will print the output, given that quiet is not True
        '''
        if self.quiet is False:
            if isinstance(output,bytes):
                output = output.decode('utf-8')
            print(output)


    def create(self,image_path,size=None):
        '''create will create a a new image
        :param image_path: full path to image
        :param size: image sizein MiB, default is 1024MiB
        :param filesystem: supported file systems ext3/ext4 (ext[2/3]: default ext3
        '''        
        if size == None:
            size=1024

        if self.debug == True:
            cmd = ['singularity','--debug','create','--size',str(size),image_path]
        else:
            cmd = ['singularity','create','--size',str(size),image_path]
        output = self.run_command(cmd,sudo=False)
        self.println(output)        
        if os.path.exists(image_path):
            return image_path
        return None


    def bootstrap(self,image_path,spec_path):
        '''create will bootstrap an image using a spec
        :param image_path: full path to image
        :param spec_path: full path to the spec file (Singularity)
        ''' 
        if self.debug == True:
            cmd = ['singularity','--debug','bootstrap',image_path,spec_path]
        else:
            cmd = ['singularity','bootstrap',image_path,spec_path]
        output = self.run_command(cmd,sudo=True)
        self.println(output)        
        return image_path


    def execute(self,image_path,command,writable=False,contain=False):
        '''execute: send a command to a container
        :param image_path: full path to singularity image
        :param command: command to send to container
        :param writable: This option makes the file system accessible as read/write
        :param contain: This option disables the automatic sharing of writable
                        filesystems on your host
        '''
        sudo = False    
        if self.debug == True:
            cmd = ["singularity",'--debug',"exec"]
        else:
            cmd = ["singularity",'--quiet',"exec"]

        cmd = self.add_flags(cmd,writable=writable,contain=contain)

        # Needing sudo?
        if writable == True:
            sudo = True

        if not isinstance(command,list):
            command = command.split(' ')

        cmd = cmd + [image_path] + command
        return self.run_command(cmd,sudo=sudo)



    def export(self,image_path,pipe=False,output_file=None,export_format="tar"):
        '''export will export an image, sudo must be used.
        :param image_path: full path to image
        :param pipe: export to pipe and not file (default, False)
        :param output_file: if pipe=False, export tar to this file. If not specified, 
        will generate temporary directory.
        :param export_format: the export format (only tar currently supported)
        '''
        cmd = ['singularity','export']

        if export_format is not "tar":
            print("Currently only supported export format is tar.")
            return None
    
        # If the user has specified export to pipe, we don't need a file
        if pipe == True:
            cmd.append(image_path)
        else:
            _,tmptar = tempfile.mkstemp(suffix=".%s" %export_format)
            os.remove(tmptar)
            cmd = cmd + ['-f',tmptar,image_path]
            self.run_command(cmd,sudo=False)

            # Was there an error?            
            if not os.path.exists(tmptar):
                print('Error generating image tar')
                return None

            # if user has specified output file, move it there, return path
            if output_file is not None:
                shutil.copyfile(tmptar,output_file)
                return output_file
            else:
                return tmptar

        # Otherwise, return output of pipe    
        output = self.run_command(cmd,sudo=False)
        self.println(output)        
        return output


    def importcmd(self,image_path,input_source):
        '''import will import (stdin) to the image
        :param image_path: path to image to import to. 
        :param input_source: input source or file
        :param import_type: if not specified, imports whatever function is given
        '''
        cmd = ['singularity','import',image_path,input_source]
        output = self.run_command(cmd,sudo=False)
        self.println(output)        
        return image_path


    def pull(self,image_path,pull_folder=None):
        '''pull will pull a singularity hub image
        :param image_path: full path to image
        ''' 
        if pull_folder is not None:
            os.environ['SINGULARITY_PULL_FOLDER'] = pull_folder

        if not image_path.startswith('shub://'):
            bot.logger.error("pull is only valid for the shub://uri, %s is invalid.",image_name)
            sys.exit(1)           

        if self.debug == True:
            cmd = ['singularity','--debug','pull',image_path]
        else:
            cmd = ['singularity','pull',image_path]
        output = self.run_command(cmd)
        self.println(output)        
        return output.split("Container is at:")[-1].strip('\n').strip()
        


    def run(self,image_path,args=None,writable=False,contain=False):
        '''run will run the container, with or withour arguments (which
        should be provided in a list)
        :param image_path: full path to singularity image
        :param args: args to include with the run
        '''
        sudo = False
        cmd = ["singularity",'--quiet',"run"]
        cmd = self.add_flags(cmd,writable=writable,contain=contain)
        cmd = cmd + [image_path]

        # Conditions for needing sudo
        if writable == True:
            sudo = True
        
        if args is not None:        
            if not isinstance(args,list):
                args = command.split(' ')
            cmd = cmd + args

        result = self.run_command(cmd,sudo=sudo)
        if isinstance(result,bytes):
            result = result.decode('utf-8')
        result = result.strip('\n')
        try:
            result = json.loads(result)
        except:
            pass
        return result


    def get_labels(self,image_path):
        '''get_labels will return all labels defined in the image
        '''
        cmd = ['singularity','exec',image_path,'cat','/.singularity/labels.json']
        labels = self.run_command(cmd)
        if isinstance(labels,bytes):
            labels = labels.decode('utf-8')
        if len(labels) > 0:
            return json.loads(labels)
        return labels
        

    def get_args(self,image_path):
        '''get_args will return the subset of labels intended to be arguments
        (in format SINGULARITY_RUNSCRIPT_ARG_*
        '''
        labels = self.get_labels(image_path)
        args = dict()
        for label,values in labels.items():
            if re.search("^SINGULARITY_RUNSCRIPT_ARG",label):
                vartype = label.split('_')[-1].lower()
                if vartype in ["str","float","int","bool"]:
                    args[vartype] = values.split(',')
        return args


    def add_flags(self,cmd,writable,contain):
        '''check_args is a general function for adding flags to a command list
        :param writable: adds --writable
        :param contain: adds --contain
        '''

        # Does the user want to make the container writeable?
        if writable == True:
            cmd.append('--writable')       

        if contain == True:
            cmd.append('--contain')       

        return cmd




#################################################################################
# HELPER FUNCTIONS
#################################################################################

def get_image(image,return_existed=False,size=None,debug=False):
    '''get_image will return the file, if it exists, or if it's docker or
    shub, will use the Singularity command line tool to generate a temporary image
    :param image: the image file or path (eg, docker://)
    :param return_existed: if True, will return image_path,existed to tell if
    an image is temporary (if existed==False)
    :param sudopw: needed to create an image, if docker:// provided
    '''
    existed = True

    # Is the image a docker image?
    if re.search('^docker://',image):
        existed = False
        cli = Singularity(debug=debug)
        tmpdir = tempfile.mkdtemp()
        image_name = "%s.img" %image.replace("docker://","").replace("/","-")
        bot.logger.info("Found docker image %s, creating and importing...",image_name)
        image_path = "%s/%s" %(tmpdir,image_name)
        cli.create(image_path,size=size)
        cli.importcmd(image_path=image_path,
                      input_source=image)
        image = image_path

    if os.path.exists(image):
        image = os.path.abspath(image)
        if return_existed == True:
            return image,existed
        return image
    return None
