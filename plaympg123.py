"""
This program demonstrates a few features of the Python subprocess module.
"""
# Global variables with module-local scope (cannot export these dunders)
__process_running__ = False
__return_code__ = None


import subprocess
import time
from threading import Thread

class AudioEngineUnavailable(Exception):
    pass 

# Start a new process to run mpg123 to play the specified sound file
def play_sound(sound_file):
    """
    Plays a sound file using the mpg123 player

    Parameters
    ----------
    sound_file : str
        The path-name of a sound file (mp3) to be played

    Returns
    -------
    p
        A Python process handle that can be used to interact with the 
        executing process

    """
    try:
        p = subprocess.Popen(['mpg123', # The program to launch in the subprocess
                              '-C',     # Enable commands to be read from stdin
                              '-q',     # Be quiet
                              sound_file],
                              stdin=subprocess.PIPE, # Pipe input via bytes
                              stdout=None,   
                              stderr=None)
        
        return p
    except FileNotFoundError as e:
        raise AudioEngineUnavailable(f'AudioEngineUnavailable: {e}')

# Monitor a subprocess, record its state in global variables
# This function is intended to run in its own thread
def process_monitor(p):
    """
    Monitor a subprocess, recording state in global variables

    Parameter:
    p : subprocess.Popen
        The subprocess to monitor
    """
    global __process_running__
    global __return_code__
    
    # Indicate that the process is running at the start, it
    # should be
    __process_running__ = True

    # When a process exits, p.poll() returns the code it set upon
    # completion
    __return_code__ = p.poll()

    # See whether the process has already exited. This will cause a
    # value (i.e. not None) to return from p.poll()
    if __return_code__ == None:
        # Wait for the process to complete, get its return code directly
        # from the wait() call (i.e. do not use p.poll())
        __return_code__ = p.wait()

    # When we get here, the process has exited and set a return code
    __process_running__ = False
    
def is_running():
    """
    For readability-return value of a dunder-named global variable
    """
    return __process_running__

def get_return_code():
    """
    For readability-return value of a dunder-named global variable
    """
    return __return_code__

if __name__ == '__main__':
    sf = './my_mp3_files/this-minimal-technology-12327.mp3'

    try:
        p = play_sound(sf)

        # We need a way to tell if a song is already playing. Start a 
        # thread that tells if the process is running and that sets
        # a global flag with the process running status.
        monitor_thread = Thread(target=process_monitor,args=(p,)) 
        monitor_thread.start()

        print(f'===> Process running flag is: {is_running()}')

        # Sleep here for 4 seconds. Notice that the external process that plays 
        # the mp3 is unaffected by this and continues to play. 
        time.sleep(2)

        # After playing for 2 seconds, write a byte b's' to the external
        # process mpg123 using the stdin stream to that process.
        #
        # Notice that sending to the process uses bytes rather than characters
        p.stdin.write(b's')
        p.stdin.flush()
        
        print(' Playback is stopped briefly.')
        
        # Sleep here while playback is stopped. The process mpg123 is still 
        # running, it's just stopped until we restart it.
        time.sleep(2)

        # After pausing playback for 2 seconds, write another character 's' to the
        # external process using the stdin stream to that process. Note that 's' is
        # a toggling command. 
        p.stdin.write(b's')
        p.stdin.flush()

        time.sleep(2)
        p.stdin.write(b't')
        p.stdin.flush()


        print('Playback has restarted. After 2 seconds, quit playback of this file.')
        time.sleep(2)
        p.stdin.write(b'q')
        p.stdin.flush()

        # There will be a slight delay before the process ends. Wait for it...
        while is_running():
            time.sleep(0.1)

        print(f'===> Process running flag is: {is_running()}')
        print(f'===> The mpg123 process ended with return code of {get_return_code()}')
    except Exception as e:
        print(e)

    # Instead of using 'q' to quit and end the player process, you can call terminate()
    # as seen below. This sends a SIGTERM from the OS to the process, ending it.
    # I think its better to either use 'q' to quit playing or just let the file
    # playback end naturally.
    # p.terminate()
    

