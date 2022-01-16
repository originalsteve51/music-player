import subprocess
import time

# Start a new process to run mpg123 to play the specified sound file
def play_sound(sound_file):
    p = subprocess.Popen(['mpg123',
                          '-C',
                        sound_file],
                        stdin=subprocess.PIPE,
                        stdout=None,stderr=None)
    return p

if __name__ == '__main__':
    sf = './1968_top_ten/mony.mp3'

    p = play_sound(sf)

    # Sleep here for 4 seconds. Notice that the external process that plays the
    # mp3 is unaffected by this and continues to play. 
    time.sleep(4)

    # After playing for 4 seconds, write a character 's' to the external process
    # using the stdin stream to that process.
    p.stdin.write(b's')
    p.stdin.flush()

    print('Playback is stopped briefly')
    
    # Sleep here while playback is stopped. The external process is still out there,
    # it's just stopped until we restart it.
    time.sleep(4)

    # After pausing playback for 4 seconds, write another character 's' to the
    # external process using the stdin stream to that process. Note that 's' is
    # a toggling command. First it stops, then it starts playback.
    p.stdin.write(b's')
    p.stdin.flush()


    print('Playback has restarted. After 10 seconds, quit playback of this file.')
    time.sleep(10)
    p.stdin.write(b'q')
    p.stdin.flush()

    print('We have quit playing back the mp3. The external process has ended.')
    time.sleep(5)

    # Instead of using 'q' to quit and end the player process, you can call terminate()
    # as seen below. This sends a SIGTERM from the OS to the process, ending it.
    # I think its better to either use 'q' to quit playing or just let the file
    # playback end naturally.
    # p.terminate()

    print('Process terminated')

