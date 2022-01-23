import http
import bisect
import csv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('log_parser')

HTTP_STATUS_CODES = [str(code.value) for code in http.HTTPStatus]

def get_paths(dir: str) -> list:
    '''
    Walk through /log_dir/ for all log files
    param: log_dir - defaults to 'logs'
    returns: list of concatenated dir + file_name 
    '''
    files = os.path.join(os.path.dirname(__file__),'..', dir)
    file_names  = next(os.walk(files))[2]    
    file_paths = ['/'.join([dir, file_name]) for file_name in file_names]
    
    return file_paths

def create_output_file_path(input_file_path: str, 
                            output_dir: str='output',
                            file_type: str='csv') -> str:
    '''
    Replace source dir with output_dir and append file type
    param: output_dir - defaults to 'output'
    param: file_type - defaults to 'csv'
    return: output file path string
    '''
    file_name = input_file_path.split('/')[1]

    return f'{output_dir}/{file_name}.{file_type}'


def create_status_code_dict() -> dict:
    '''
    Create dict for status codes initialized to 0 for 
    instantiated rows when aggregated status codes by minute
    return: {'100': 0, ... '511': 0}
    '''
    return {code: 0 for code in HTTP_STATUS_CODES}


def create_row_dict(minute: str) -> dict:
    '''
    Create new minute-level dict for row aggregation
    param: minute - string of minute to aggregate at
    return: {'time': minute, '100': count, ... '511': count}
    '''
    row_dict = dict({'time': minute})
    row_dict.update(create_status_code_dict())

    return row_dict


def extract_metadata(line: str) -> tuple:
    '''
    Extract minute and status code from line in log
    to insert to ordered list of tuples order by minute
    param: line - log string from log file
    return: tuple of minue and status code
    '''
    line = line.split()
    minute = line[3][1:]
    status_code = line[8]
    
    return (minute, status_code)


def create_tuple_list(file_name: str) -> list:
    '''
    Read log file and create list of tuples ordered
    by minute string for minute-by-minute aggregation
    downstream
    param: file_name - name of log file to read
    return: list of tuples ordered ascendingly by minute
    '''
    tuple_list = []
    with open(file_name) as f:
        logger.info(f'Reading: {file_name}')
        try:
            for line in f.readlines():
                bisect.insort_left(tuple_list, (extract_metadata(line)))
        except IOError as e:
            logger.warning(e)
    return tuple_list


def create_output_list(log_data: list) -> list:
    '''
    Create new rows from list of tuples. Increment status_code counts,
    and append current row when new minute is found. Append final row 
    on completion.
    param: log_data - list of tuples to iterate through
    return: list of row_dicts
    '''
    row_list = []
    row = {}
    minute = None
    for t in log_data:
        # unpack tuple
        new_minute, status_code = t
        # Append new row if current minute is not previous 
        # minute and row is not empty then create new row. 
        # Increment status code in current row.
        if new_minute != minute:
            if row:
                row_list.append(row)
            minute = new_minute
            row = create_row_dict(minute)
        row[status_code] += 1
    row_list.append(row)
    
    return row_list


def write_to_csv(output_list: dict, output_path: str) -> None:
    ''' 
    Create header from same vals as row_dict keys and write each
    row_dict to csv
    param: output_list - list of row_dicts
    param: output_path - file path destination
    '''
    fields = ['time'] + HTTP_STATUS_CODES
    
    output_dir = output_path.split('/')[0]
    if not os.path.exists(output_dir):
        os.mkdir(output_path)

    with open(output_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        logger.info(f'Writing: {output_path}')
        try:    
            for data in output_list:
                writer.writerow(data)
            logger.info(f'Wrote: {len(output_list)} rows to {output_path}')
        except IOError as e:
            logger.warning(e)


if __name__ == '__main__':
    log_file_paths = get_paths('logs')
    for log_file_path in log_file_paths:
        output = create_output_list(create_tuple_list(log_file_path))

        output_path = create_output_file_path(log_file_path)    
        
        write_to_csv(output, output_path)
