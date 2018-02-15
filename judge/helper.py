import signal
from contextlib import contextmanager
from subprocess import Popen, PIPE
import uuid
import traceback

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def kill_and_remove(ctr_name):
    try:
        for action in ('kill',):
            p = Popen('docker %s %s' % (action, ctr_name), shell=True,
                      stdout=PIPE, stderr=PIPE)
            if p.wait() != 0:
                raise RuntimeError(p.stderr.read())
    except:
        pass

def run(code, tl, input_data):
    ctr_name = str(uuid.uuid4())
   
    try:
        with time_limit(tl+30):
            p = Popen(['docker', 'run','-i', '-a', 'stdin', '-a', 'stdout', '-a', 'stderr',
                       '--name', ctr_name, '--rm', 'judge-docker',
                       'timeout', '-s', 'SIGKILL', str(tl), 'python3', '-c', code],
                      stdout=PIPE, stdin=PIPE, stderr=PIPE)
            
            out, err = p.communicate(input=input_data.encode())
            print('Return code:',p.returncode)

            if p.returncode == 124:
                kill_and_remove(ctr_name)
                return ('Time limit exceeded!','tle')
            
            if p.returncode != 0:    
                return (err.decode()+'\n'+'Return code from solution: '+str(p.returncode),'user_err')

            return (out.decode(),'ok')

    except TimeoutException:
        print('Timeout occured, wtf..')
        kill_and_remove(ctr_name)
        return ('The judge took too long. Aborting operation...','judge_err')
    except Exception as e:
        return (traceback.format_exc(),'judge_err')




timeout_loc = "/usr/local/opt/coreutils/libexec/gnubin/timeout"

def unsafe_run(code, tl, input_data):
    p = Popen([timeout_loc, '-s', 'SIGKILL', str(tl), 'python3', '-c', code],
                stdout = PIPE, stdin = PIPE, stderr = PIPE)

    out, err = p.communicate(input=input_data.encode())

    if p.returncode!=0:
        return ('The judge experienced an error.\n Return code: ' + str(p.returncode)+'\n'+err.decode(),'judge_err')

    return (out.decode(), 'ok')



