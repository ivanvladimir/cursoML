#!/usr/bin/env python
# -*- coding: utf-8
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/IIMAS/UNAM
# ----------------------------------------------------------------------
# live.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------

# System libraries
import argparse
import pyaudio
import wave
import sys
import os.path
import cmd
import time
import pickle
from scipy.signal import resample
import numpy as np
from sklearn.ensemble import RandomForestClassifier as RFC

import numpy as np
import scikits.audiolab as audiolab
from scipy.stats import kurtosis
import pylab as plt
import glob
import essentia
from essentia.standard import *
#os.system('cls')
w = Windowing(type = 'hann')
sample_r=2048
jump_r=sample_r/2
D_mfccs = 1024 / 44100.0
Row = []
Mega_win = []
Stats = []
ind=0;
song=0;
w = Windowing(type = 'blackmanharris62')
spectrum = Spectrum()
mfcc = essentia.standard.MFCC()
 
def Stats_Es(mfccs_s): 
   Mega_win=np.array(mfccs_s)
   kurt=kurtosis(Mega_win,axis=0)
   prom=np.mean(Mega_win,axis=0)
   vmax=np.amax(Mega_win,axis=0)
   vmin=np.amin(Mega_win,axis=0)
   dstd=np.std(Mega_win,axis=0)
   p1=np.percentile(Mega_win,25,axis=0)
   p2=np.percentile(Mega_win,50,axis=0)
   p3=np.percentile(Mega_win,75,axis=0)
   Row=[]
   for k in range(13):
       Row.append(kurt[k])
       Row.append(prom[k])
       Row.append(vmax[k])
       Row.append(vmin[k])
       Row.append(dstd[k])
       Row.append(p1[k])
       Row.append(p2[k])
       Row.append(p3[k])
   Stats.append(np.vstack(Row))
   return Stats

audio = pyaudio.PyAudio()

# STATUS OF THE APP
recording=False
identifying=False
act_status=False
collect=[]
nturnoff=0
wf=None
from scipy.stats import gmean

identifying=False
resampling=1.0

class BirdCLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.promtp = "> "
        self.intro = "Bienvenidios a la identificación de géneros"

    def do_identify(self,args):
        global identifying
        if identifying:
            print "Error: Already indetifying..."
        else:
            print "Wait for 10 seconds... buffering"
            time.sleep(10)
            identifying=True
    
    def do_stop(self,args):
        global identifying,odir
        if not identifying:
            print "Error: Not identifying"
        else:
            print "Error: Stoping identifying"
            identifying=False

    def do_hist(self,args):
        print self._hist

    def do_quit(self,args):
        return -1

    def do_exit(self,args):
        return -1

    def do_EOF(self,args):
        return self.do_exit(args)

    def do_help(self, args):
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        return stop

    def emptyline(self):    
        pass

    def default(self, line):
        pass


def callback(in_data, frame_count, time_info, status):
    global abuffer, recording, identifying, resampling, \
            ncalls, act_status, collect, nturnoff, buffer_size
    global wf,ratei,odir,model,keys,filename
    # If there is nothing to do
    if not identifying:
        return (in_data,pyaudio.paContinue)
    # If there is something to do
    in_data = np.fromstring(in_data, dtype='Int16')
    in_data = in_data/32767.0
    if resampling != 1.0:
        in_data=resample(in_data,in_data*resmpling)
    abuffer.append(in_data)

    if len(abuffer)>buffer_size:
        in_data = np.concatenate(abuffer[-buffer_size:])
        if identifying:
            # AQUI VA EL CODIGO DE
            # Extraer MFCC
            # Extraer estadísticas
            # Predecir
              mfccs =[]
        audio = essentia.array(in_data)
        for frame in FrameGenerator(audio, frameSize = 2048 , hopSize = 1024):
            mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
            mfccs.append(mfcc_coeffs)
        mfccs = essentia.array(mfccs).T
        stats = Stats_Es(mfccs)
        print stats.shape
        print model.predict(stats)       
        abuffer.pop(len(abuffer)-buffer_size)
    if not stop:
        return (in_data,pyaudio.paContinue)
    else:
        return (in_data,pyaudio.paComplete)

# MAIN
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser(description="Identifica géneros musicales")
    p.add_argument("-m", "--model",default=None, type=str,
            action="store", dest="model",
            help="Model for birds [off]")
    p.add_argument("-l", "--list",default=False,
            action="store_true", dest="list",
            help="Lists devices availables")
    p.add_argument("-d", "--device",default=None,type=int,
            action="store", dest="device",
            help="Lists devices availables")
    p.add_argument("--buffer_size",type=int,default=10,
            action="store", dest="buffer_size",
            help="Buffer size segs")
    p.add_argument("--rate",type=int,default=44100,
            action="store", dest="rate",
            help="Frequency record rate")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    # Parsing commanls line arguments
    args = p.parse_args()

    # Defining verbose function
    if args.verbose:
       def verbose(*args):
            print >> sys.stderr, "".join([str(x) for x in args]) 
    else:   
        verbose = lambda *a: None  


    # DEFAULTS FOR VAD
    avg_intensity1=0.0
    avg_intensity2=0.0
    ncalls=0
    

    if args.list:
        verbose('List devices mode')
        for i in range(audio.get_device_count()):
            info=audio.get_device_info_by_index(i)
            if info['name'].startswith('H4'):
                print "ZOOM interface present"
            print '  {0} - {1}'.format(
                    i,
                    info['name']
                )
        sys.exit()

    if not args.device:
        info=audio.get_default_input_device_info()
        verbose('Conecting to default device, ',info['name'])
    else:
        info=audio.get_device_info_by_index(args.device)
        verbose('Connecting to device ',info['name'])

    resampling=(args.rate*1.0)/int(info['defaultSampleRate'])

    model=None
    if args.model:
        verbose('Loading model from ',args.model)
        model = pickle.load(open(args.model,'rb'))
 
    rate=args.rate
    stream = audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=int(info['defaultSampleRate']),
            input_device_index=args.device,
            input=True,
            stream_callback=callback
        )


    buffer_size=args.buffer_size*int(info['defaultSampleRate'])/2048
    verbose('Setting rate to ',rate)
    
    abuffer=[]
    stop=False
    stream.start_stream()

    console=BirdCLI()
    console.cmdloop()


    stop=True
    verbose('Stoping audio stream ...')
    #if not stream.is_stopped():
    #    stream.stop_stream()
    verbose('Closing audio stream ...')
    stream.close()
    verbose('Terminating connection')
    audio.terminate()

