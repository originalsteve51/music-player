"""
This module contains a reusable MusicPlayer class that is based
on an audio player application named mpg123.
"""

import subprocess
import time
from threading import Thread

#-------------------------------------------------------------------
# AudioEngineUnavailableError class
#-------------------------------------------------------------------
class AudioEngineUnavailableError(Exception):
    """
    When the required player application (mpg123) is not available
    this Exception is raised.
    """
    pass 

#-------------------------------------------------------------------
# NoPlaybackError class
#-------------------------------------------------------------------
class NoPlaybackError(Exception):
    """
    When an attempt is made to control playback but nothing is
    being played, this Exception is raised.
    """
    pass 

#-------------------------------------------------------------------
# MusicPlayer class
#-------------------------------------------------------------------
class MusicPlayer():
    """
    Start a subprocess running audio player mpg123 to play a specified
    mp3 file. Provide controls to stop/start and quit playback.
    """
    def __init__(self):
        self._audioengine = 'mpg123' # Only supported player is mpg123
        self._p = None
        self._is_paused = False
        self._process_running = False
        self._return_code = None


    def play(self, sound_file):
        try:
            self._p = subprocess.Popen([self._audioengine, 
                                  '-C',     # Enable commands to be read from stdin
                                  '-q',     # Be quiet
                                  sound_file],
                                  stdin=subprocess.PIPE, # Pipe input via bytes
                                  stdout=None,   
                                  stderr=None)

            # Since we are using stdin for commands, we have to send something
            # to keep mpg123 from complaining when we exit. The complaint is
            # not a serious one, but it is annoying. If stdin is not used the
            # terminal is posted with "Can't set terminal attributes" at exit.
            # I send an empty string below to keep mpg123 happy.
            self._p.stdin.write(b'')
            self._p.stdin.flush()

            monitor_thread = Thread(target=self.process_monitor,args=()) 
            monitor_thread.start()

        except FileNotFoundError as e:
            raise AudioEngineUnavailableError(f'AudioEngineUnavailableError: {e}')

    def quit_playing(self):
        self._p.stdin.write(b'q')
        self._p.stdin.flush()

        # Wait for process to end
        while self._process_running:
            time.sleep(0.1)


    def pause(self):
        if self._process_running:
            if self._is_paused:
                pass
            else:
                self._p.stdin.write(b's')
                self._p.stdin.flush()
                self._is_paused = True
        else:
            raise NoPlaybackError('Cannot pause playback because nothing is playing.')
                    

    def resume(self):
        if self._process_running:
            if not self._is_paused:
                pass
            else:
                self._p.stdin.write(b's')
                self._p.stdin.flush()
                self._is_paused = False
        else:
            raise NoPlaybackError('Cannot resume playback because nothing is playing.')

    def is_playing(self):
        return self._process_running

    def return_code(self):
        return self._return_code

    def process_monitor(self):
        # Indicate that the process is running at the start, it
        # should be
        self._process_running = True

        # When a process exits, p.poll() returns the code it set upon
        # completion
        self._return_code = self._p.poll()

        # See whether the process has already exited. This will cause a
        # value (i.e. not None) to return from p.poll()
        if self._return_code == None:
            # Wait for the process to complete, get its return code directly
            # from the wait() call (i.e. do not use p.poll())
            self._return_code = self._p.wait()

        # When we get here, the process has exited and set a return code
        self._process_running = False



def main():
    """
    A function that instantiates a MusicPlayer and demonstrates its features.
    """
    player = MusicPlayer()

    player.play('./1968_top_ten/mony.mp3')
    print(f'Player is playing: {player.is_playing()}')
    time.sleep(2)
    player.pause()
    time.sleep(2)
    player.resume()
    time.sleep(2)

    player.quit_playing()
    print(f'Player is playing: {player.is_playing()}')
    print(f'Return code: {player.return_code()}')

    player.play('./1968_top_ten/grazing.mp3')
    while player.is_playing():
        time.sleep(1)
        print('*')



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

            

       