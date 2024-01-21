from datetime import datetime
from random import choice

def get_status(statuslog_path: str) -> str:
    try:
        with open(statuslog_path, 'r') as file:
            lines = file.readlines()
            if lines:
                date_format = '%Y-%m-%d %H:%M:%S.%f'

                last_line=lines[-1].strip() 
                first_line =lines[0].strip()    # general_start=####
                general_start=datetime.strptime(first_line.split('=')[1], date_format)

                if last_line[0:7]=='current':  #indicates that there is a simulation running
                    # Split the line into its components
                    components = last_line.split(';')
                    # Create a dictionary to store the values
                    current_status = {}
                    for component in components:
                        key, value = component.split('=')
                        current_status[key.strip()] = value.strip()
                    #current_sim=1112PeV; start_time=####; exceptions=@@@,@@@,@@@
                    date_format = '%Y-%m-%d %H:%M:%S.%f'
                    now=datetime.now()
                    current_status['start_time']=datetime.strptime(current_status['start_time'], date_format)
                    elapsed_time_current_sim=str(now-current_status['start_time']).split('.')[0]
                    elapsed_time_general=str(now-general_start).split('.')[0]

                    status= f'''Corsika is currently running a simulation of {current_status['current_sim']} that has been in progress for a duration of [{elapsed_time_current_sim}]. 
                    The entire simulation process for all energies has been running for a time period of [{elapsed_time_general}].
                    By now, the following exceptions have been encountered: {current_status['exceptions']}'''
                    return status

                elif last_line=='finished':
                    return 'Corsika has finished with all the simulations. Data is ready for processing'
                elif last_line==first_line:
                    return "No simulation has started"                   
                else:
                    return "Something went wrong. Status log was probably not correctly registered"



            else:
                return 'Empty log. No previous simulation found'  # El archivo está vacío
    except Exception as e:
        
        return f"Exception while reading status: {e}"

    

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == 'bot status':
        return 'Up and running >:3'
    elif lowered == 'simulation status':
        statuslog_path='CORSIkawaii\status_log.txt'
        status: str = get_status(statuslog_path)
        return status
    elif lowered=='insulta al niu':
        return choice(['niu ctm','el niu se la come','el niu se chocó en el little caesars'])
    else:
        return 'Command not found'
