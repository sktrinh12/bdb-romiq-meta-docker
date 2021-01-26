import paramiko
import os
# from datetime import datetime
# import pandas as pd
# from db_class import PostgresConn
# import json

# def fetch_recent(cur):
#     """
#     fetch the most recent postgresql row
#     """
#     cur.execute("""SELECT * FROM meta ORDER BY ts DESC FETCH FIRST ROW ONLY""")
#     data = list(cur.fetchone())
#     data[0] = format_datetime(data[0])
#     return data

# def select_str_colnames():
#     return [
#             "Control.Row",                #7
#             "Target.Species",             #8
#             "Specificity..CD.",           #9
#             "Isotype.Host.Species",       #10
#             "Clone",                      #11
#             "Fluorochrome",               #12
#             "Parameter",                  #13
#             "units",                      #16
#             "Sample.Types",               #17
#             "Sample.Species",             #18
#             "Sample.Strain",              #19
#             "Donor.ID",                   #20
#             "spec1_range",                #21
#             "spec2_range",                #22
#             "spec3_range",                #23
#             "gating_method",              #24
#             ]


# def sort_columns(df):
#     """
#     sort the dataframe by the specified order, 25 entries
#     """
#     colm_order = [
#             "Filename",                   #1
#             "Well.ID",                    #2
#             "Plate.ID",                   #3
#             "Stain.Date",                 #4
#             "Plate.Row",                  #5
#             "Plate.Column",               #6
#             "Control.Row",                #7
#             "Target.Species",             #8
#             "Specificity..CD.",           #9
#             "Isotype.Host.Species",       #10
#             "Clone",                      #11
#             "Fluorochrome",               #12
#             "Parameter",                  #13
#             "Batch.Number",               #14
#             "ug.test",                    #15
#             "units",                      #16
#             "Sample.Type",                #17
#             "Sample.Species",             #18
#             "Sample.Strain",              #19
#             "Donor.ID",                   #20
#             "spec1_range",                #21
#             "spec2_range",                #22
#             "spec3_range",                #23
#             "gating_method",              #24
#             "gating_argument"             #25
#             ]
#     if all([c in df.columns for c in colm_order]):
#         pass
#     else:
#         colm_order[0] += 's'
#         colm_order[16] += 's'

    # print('changed columns')
    # print(df.columns)
    # return df[colm_order]


# def convert_pd_tuple(json_data, barcode):
#     """
#     convert the inputted json data to a pandas dataframe then a list of tuples
#     return a tuple with timestamp and barcode for that metadata set and the dataframe
#     """
#     df = pd.read_json(json_data)
#     df = sort_columns(df)
#     df['Batch.Number'].fillna("NA", inplace=True)
#     df['Batch.Number'] = df['Batch.Number'].astype(str)
#     # df[select_str_colnames()].fillna("NA", inplace=True)
#     # df = df.replace('NaN', 'NA')
#     print(df.dtypes)
#     ts = format_datetime(datetime.now())
#     df.insert(0, column = 'timestamp', value=ts)
#     df.insert(1, column = 'barcode', value=barcode)
#     print(f'number of columns: {len(df.columns)}')
#     dt = [tuple(x) for x in df.to_numpy()]
#     # print(df.head())
#     return ts, dt

# def insert_meta(data_list):
#     """
#     post http request to insert entire meta dataframe into postgresql database; 27 values
#     """
#     pg_sql = """INSERT INTO meta VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
#                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#     with PostgresConn() as conn:
#         cur = conn.cursor()
#         cur.executemany(pg_sql, data_list)
#         recent_data = fetch_recent(cur)
#         conn.commit()
#     print('sucecssfullly uploaded data')
#     return recent_data

# def get_meta(barcode):
#     """
#     get http request to grab current metadata based on barcode
#     """
#     stmt = """SELECT * FROM META WHERE BARCODE = %s"""
#     with PostgresConn() as conn:
#         # cur = conn.cursor(cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print('running sql stmt...')
#         cur.execute(stmt, (barcode,))
#         res = format_for_json(cur.fetchall())
#         meta = json.dumps(res, indent=2)
#         cur.close()
#     return meta

# def format_for_json(result):
#     """
#     convert timestamp to string in order to pass as json
#     """
#     result_list = []
#     for r in result:
#         r = list(r)
#         r[0] = format_datetime(r[0])
#         result_list.append(r)
#     return result_list

# def format_datetime(timestamp):
#     """
#     convert datetime object to string
#     """
#     return timestamp.strftime('%Y-%b-%d %H:%M:%S')


# def convert_ts(timestamp):
#     """
#     convert the string from url (as passed arg) to timestamp object
#     """
#     timestamp = datetime.strptime(timestamp, '%Y-%m-%d_%H_%M_%S')
#     return timestamp


def run_script_ssh(script_name, **kwargs):
    """
    use paramiko library to ssh into docker container and run Rscript command
    """
    host = os.getenv("HOSTNAME")
    print(f'hostname: {host}')
    port = 22
    username = os.getenv("UNAME")
    password = os.getenv("PASSWORD")
    version = os.getenv("VERSION")
    omiq_path = os.path.join("/home", username, "R")
    if script_name == "main_driver":
        rscript_path = os.path.join(omiq_path, f"omiq_v{version}",
                                    "OmiqPipeline",f"{script_name}.R")
    else:
        rscript_path = os.path.join(omiq_path, f"{script_name}.R")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    # run rscript
    ssh_cmd = f"Rscript {rscript_path}"
    barcode = kwargs.get('barcode', '')
    re_run = kwargs.get('re_run', '')
    if barcode:
        ssh_cmd += f" {barcode}"
    else:
        raise("need to supply barcode argument")
    if re_run not in ['', None]:
        ssh_cmd += f" {re_run}"
    print('='*40)
    print(f'running command: \"{ssh_cmd}\"')
    print('='*40)
    stdin, stdout, stderr = ssh.exec_command(ssh_cmd)
    stdout_lines = ' '.join(stdout.readlines())
    ssh.close()
    print(stdout_lines)
    if stderr:
        stderr_lines = ' '.join(stderr.readlines())
        print(stderr_lines)
    return stdout_lines
