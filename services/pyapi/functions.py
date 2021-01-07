from datetime import datetime
import pandas as pd
from db_class import PostgresConn
import paramiko
import os
import json

def fetch_recent(cur):
    """
    fetch the most recent postgresql row
    """
    cur.execute("""SELECT * FROM meta ORDER BY ts DESC FETCH FIRST ROW ONLY""")
    data = list(cur.fetchone())
    data[0] = format_datetime(data[0])
    return data

def sort_columns(df):
    """
    sort the dataframe by the specified order
    """
    colm_order = ["Filename",
            "Well.ID",
            "Plate.ID",
            "Stain.Date",
            "Plate.Row",
            "Plate.Column",
            "Control.Row",
            "Target.Species",
            "Specificity..CD.",
            "Specificity..non.CD.",
            "Isotype.Host.Species",
            "Clone",
            "Fluorochrome",
            "Parameter",
            "Batch.Number",
            "ug.test",
            "units",
            "Sample.Type",
            "Sample.Species",
            "Sample.Strain",
            "Donor.ID",
            "spec1_range",
            "spec2_range",
            "spec3_range",
            "gating_method",
            "gating_argument"]
    return df[colm_order]


def convert_pd_tuple(json_data):
    """
    convert the inputted json data to a pandas dataframe then a list of tuples
    return a tuple with timestamp for that metadata set and the dataframe
    """
    df = pd.read_json(json_data)
    df = sort_columns(df)
    print(df.dtypes)
    # df.to_csv('/users/spencertrinh/Downloads/pandas.csv', index=False)
    ts = format_datetime(datetime.now())
    df.insert(0, column = 'timestamp', value=ts)
    # print(df.head())
    print(df.columns)
    print(len(df.columns))
    dt = [tuple(x) for x in df.to_numpy()]
    return ts, dt

def insert_meta(data_list):
    """
    post http request to insert entire meta dataframe into postgresql database; 26 values
    """
    pg_sql = """INSERT INTO meta VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    with PostgresConn() as conn:
        cur = conn.cursor()
        cur.executemany(pg_sql, data_list)
        recent_data = fetch_recent(cur)
        conn.commit()
    print('sucecssfullly uploaded data')
    return recent_data

def get_meta(timestamp):
    """
    get http request to grab current metadata based on timestamp
    """
    stmt = """SELECT * FROM META WHERE TS = %s"""
    with PostgresConn() as conn:
        # cur = conn.cursor(cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print('running sql stmt...')
        cur.execute(stmt, (timestamp,))
        res = format_for_json(cur.fetchall())
        meta = json.dumps(res, indent=2)
        cur.close()
    return meta

def format_for_json(result):
    """
    convert timestamp to string in order to pass as json
    """
    result_list = []
    for r in result:
        r = list(r)
        r[0] = format_datetime(r[0])
        result_list.append(r)
    return result_list

def format_datetime(timestamp):
    """
    convert datetime object to string
    """
    return timestamp.strftime('%Y-%b-%d %H:%M:%S')


def convert_ts(timestamp):
    """
    convert the string from url (as passed arg) to timestamp object
    """
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d_%H_%M_%S')
    return timestamp


def run_script_ssh(script_name, **kwargs):
    """
    use paramiko library to ssh into docker container and run Rscript command
    """
    host = "romiq"
    port = 22
    username = os.getenv("UNAME")
    password = os.getenv("PASSWORD")
    version = os.getenv("VERSION")
    if script_name == "main_driver":
        rscript_path = os.path.join("/home", username, "R", f"omiq_v{version}",
                                    "OmiqPipeline",f"{script_name}.R")
    else:
        rscript_path = os.path.join("/home", username, "R", f"{script_name}.R")
    ssh_cmd = f"Rscript {rscript_path}"
    timestamp = kwargs.get('timestamp', '')
    re_run = kwargs.get('re_run', '')
    if timestamp != '':
        ssh_cmd += f" {timestamp.replace(' ', '_')}"
    if re_run != '':
        ssh_cmd += f" {re_run}"
    print(ssh_cmd)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(ssh_cmd)
    stdout_lines = ' '.join(stdout.readlines())
    ssh.close()
    print(stdout_lines)
    if stderr:
        stderr_lines = ' '.join(stderr.readlines())
        print(stderr_lines)
    return lines
