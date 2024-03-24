from datetime import datetime
from random import choice
import os

def get_status(statuslog_path: str) -> str:
    try:
        with open(statuslog_path, 'r') as file:
            lines = file.readlines()
            if lines:
                date_format = '%Y-%m-%d %H:%M:%S'

                last_line=lines[-1].strip() 
                first_line =lines[0].strip()    # "start: Script is running simulations from $START_ENERGY GeV to $END_ENERGY GeV with steps of $INCREMENT GeV; general_start=$general_start_time"
                
                general_start=datetime.strptime(first_line.split('=')[1], date_format)
                if last_line==first_line:
                    return "No simulation has started, but the script is running" 
                elif last_line[0:7]=='current':  #indicates that there is a simulation running
                    # Split the line into its components
                    components = last_line.split(';')
                    # Create a dictionary to store the values
                    current_status = {}
                    for component in components:
                        key, value = component.split('=')
                        current_status[key.strip()] = value.strip()
                    #current_sim=1112PeV; start_time=####
                    date_format = '%Y-%m-%d %H:%M:%S'
                    now=datetime.now()
                    current_status['start_time']=datetime.strptime(current_status['start_time'], date_format)
                    elapsed_time_current_sim=str(now-current_status['start_time']).split('.')[0]
                    elapsed_time_general=str(now-general_start).split('.')[0]

                    status= f"Current energy {current_status['current_sim']}GeV.\nCurrent simulation time: [{elapsed_time_current_sim}].\nTotal simulation time: [{elapsed_time_general}]."
                    return status
                elif last_line[0:8]=='finished':
                    finish_time=last_line[12:]
                    status = f"Corsika has finished all the simulations at {finish_time}"
                    return status
                    
                else:
                    return "Something went wrong. Status log was probably not correctly registered"

            else:
                return 'Empty log. No previous simulation found'  # El archivo está vacío
    except Exception as e:
        return f"Exception while reading status: {e}"

def get_info(statuslog_path: str) -> str:
    try:
        with open(statuslog_path, 'r') as file:
            lines = file.readlines()
            if lines :
                first_line =lines[0].strip()    # "start: Script is running simulations from $START_ENERGY GeV to $END_ENERGY GeV with steps of $INCREMENT GeV; general_start=$general_start_time"
                energy_range_str=first_line.split(';')[0].split(':')[1].strip()
                general_start_str=first_line.split('=')[1]
                info=f"{energy_range_str}\nSimulations started at {general_start_str}!"
                return info
            else:
                return 'Empty log. No previous simulation found'  # El archivo está vacío
    except Exception as e:
        return f"Exception while reading status: {e}"
    first_line



def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    statuslogs_parent_dir='./' ##UPDATE PATH (the same)
    statuslogs = []
    
    for filename in os.listdir(statuslogs_parent_dir):
        if filename.startswith("statuslog") and filename.endswith(".txt"):
            statuslogs.append(os.path.join(statuslogs_parent_dir, filename))
    
    if lowered == 'bot status':
        return 'Bot ready'
        
    elif lowered == 'simulation status':
        partial_status_list=[]
        for statuslog_path in statuslogs:
            partial_status: str = get_status(statuslog_path)
            thread_id=statuslog_path.split('/')[-1][9:-4]
            partial_status_list.append(f"Thread {thread_id}:\n{partial_status}\n\n")
            
        status=''.join(partial_status_list)
        return status
        
    elif lowered=='simulation info':
        partial_info_list=[]
        for statuslog_path in statuslogs:
            partial_info: str = get_info(statuslog_path)
            thread_id=statuslog_path.split('/')[-1][9:-4]
            partial_info_list.append(f"Thread {thread_id}:\n{partial_info}\n\n")
            
        info=''.join(partial_info_list)
        return info
        
    elif lowered == 'current time':
        now=datetime.now()
        now_str=str(now).split('.')[0]
        return f'Current time in server: {now_str}'
    else:
        return 'Command not found'
