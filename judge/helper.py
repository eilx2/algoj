import signal
from contextlib import contextmanager
from subprocess import Popen, PIPE
import subprocess
import uuid
import traceback
import shlex
import base64

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
        with time_limit(120):
            p = subprocess.run(['docker', 'run','-i', '-a', 'stdin', '-a', 'stdout', '-a', 'stderr',
                       '--name', ctr_name, '--rm',  'judge-docker',
                       'bash', 'run_sol.sh', code, str(tl)], stdout=PIPE, stderr=PIPE, input=input_data.encode())
            
            out = p.stdout
            err = p.stderr
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
        return ('The judge took too long. Try submitting another time. Aborting operation...','judge_err')
    except Exception as e:
        return (traceback.format_exc(),'judge_err')


def quote(s):
    ns=''

    for i in range(len(s)):
        if s[i]=='\'':
            ns+='\\\''
        elif s[i]=='\"':
            ns+='\\"'
        else:
            ns+=s[i]

    return "'"+ns+"'"

def run_with_judge(judge_code, code, tl, input_data):
    ctr_name = str(uuid.uuid4())
   
    try:
        with time_limit(120):

            code_cmd = "echo "+shlex.quote(code)+" > sol.py"
            judge_cmd="echo "+shlex.quote(judge_code)+" > judge.py"
            run_cmd = "timeout -s SIGKILL "+str(tl)+" python3 judge.py"

            cmd=code_cmd+" && "+judge_cmd+" && "+run_cmd
            cmd = base64.b64encode(cmd.encode())
            cmd = cmd.decode()

            print(cmd)
            p = Popen(['docker', 'run','-i', '-a', 'stdin', '-a', 'stdout', '-a', 'stderr',
                       '--name', ctr_name, '--rm',  'judge-docker',
                       'bash','run.sh',cmd], 
                       stdout=PIPE, stdin=PIPE, stderr=PIPE)
            

            out, err = p.communicate(input=input_data.encode())
            print('Return code:',p.returncode)
            print(out.decode())
            if p.returncode == 124:
                kill_and_remove(ctr_name)
                return ('Time limit exceeded!','tle')
            
            if p.returncode != 0:    
                return (err.decode()+'\n'+'Return code from solution: '+str(p.returncode),'user_err')

            return (out.decode(),'ok')

    except TimeoutException:
        print('Timeout occured, wtf..')
        kill_and_remove(ctr_name)
        return ('The judge took too long. Try submitting another time. Aborting operation...','judge_err')
    except Exception as e:
        return (traceback.format_exc(),'judge_err')




timeout_loc = "timeout"

def unsafe_run(code, tl, input_data):
    p = Popen([timeout_loc, '-s', 'SIGKILL', str(tl), 'python3', '-c', code],
                stdout = PIPE, stdin = PIPE, stderr = PIPE)

    out, err = p.communicate(input=input_data.encode())

    if p.returncode!=0:
        return ('The judge experienced an error.\n Return code: ' + str(p.returncode)+'\n'+err.decode(),'judge_err')

    return (out.decode(), 'ok')



