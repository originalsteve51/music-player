"""
This program demonstrates a few features of the Python subprocess module.
"""
import subprocess
import time

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
    p = subprocess.Popen(['mpg123', # The program to launch in the subprocess
                          '-C',     # Enable commands to be read from stdin
                          '-q',     # Be quiet
                          sound_file],
                        stdin=subprocess.PIPE, # Pipe input via bytes
                        stdout=None,   
                        stderr=None)
    
    return p

if __name__ == '__main__':
    sf = './1968_top_ten/mony.mp3'

    p = play_sound(sf)

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

    print('Playback has restarted. After 2 seconds, quit playback of this file.')
 
    time.sleep(2)
    p.stdin.write(b'q')
    p.stdin.flush()

    print('We have quit playing the mp3. The external process has ended.')

    # Instead of using 'q' to quit and end the player process, you can call terminate()
    # as seen below. This sends a SIGTERM from the OS to the process, ending it.
    # I think its better to either use 'q' to quit playing or just let the file
    # playback end naturally.
    # p.terminate()

