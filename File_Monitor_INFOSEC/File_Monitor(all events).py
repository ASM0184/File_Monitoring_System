import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import multiprocessing
import mysql.connector
import pytz
import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(process)s - %(processName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

db_config = {
    "host": "localhost",   #Enter your MySQL host
    "user": "root",        #Enter your user name
    "password": "@$m_!!T27",  #Enter your password
    "database": "file_database" ,  #Enter your databse name
}

event_handler = FileSystemEventHandler()
observer = Observer()


db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()


def process_file(file_path, event_type, modification_time, deletion_time):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]
    file_size = os.path.getsize(file_path)
    local_tz = pytz.timezone('Asia/Kolkata')   #Enter timezone according to your preferrence , here I have used IST
    creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path), local_tz)


    insert_query = """
    INSERT INTO monitored_files 
    (file_path, file_name, file_extension, file_size, event_type, creation_time, modification_time, deletion_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (file_path, file_name, file_extension, file_size, event_type, creation_time, modification_time, deletion_time)

    cursor.execute(insert_query, values)
    db_connection.commit()

processed_events = set()

def on_created(event):
    file_path = event.src_path

    if "$RECYCLE.BIN" in file_path.upper():
        return
 
    if file_path not in processed_events:
        try:
            if os.path.isdir(file_path):
                # If the created item is a directory, log only the directory creation
                logging.info(f"Folder created: {file_path}")
                process_file(file_path, "created", None, None)
            else :
                process_file(file_path, "created" ,None ,None)
                processed_events.add(file_path)
                logging.info(f"File created: {file_path}")
        except Exception as e:
            logging.error(f"Error processing file: {file_path}. Error: {str(e)}")


def on_modified(event):
        file_path = event.src_path

        if "$RECYCLE.BIN" in file_path.upper():
            return
    
        if event.event_type == 'modified':
            modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path), pytz.timezone('Asia/Kolkata'))
            process_file(file_path, "modified", modification_time, None)
            logging.info(f"File modified: {file_path}")

   
def on_deleted(event):
    file_path = event.src_path

    if "$RECYCLE.BIN" in file_path.upper():
        return

    if os.path.exists(file_path):  # Check if the file still exists
        if event.is_directory:
            logging.info(f"Folder deleted: {file_path}")
        else:
            processed_events.add(file_path)
            deletion_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            process_file(file_path, "deleted", None, deletion_time)
            logging.info(f"File deleted: {file_path}")
    else:
        logging.info(f"File deleted: {file_path}")




event_handler.on_created = on_created
event_handler.on_modified = on_modified
event_handler.on_deleted = on_deleted

def monitor_single_folder(folder_name):
    observer.schedule(event_handler, folder_name, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    folder1 = "A:\\"  #Enter location of the directory to be monitored. Here I have used A: drive in my PC
    folder2 = "B:\\"  #Enter location of the directory to be monitored. Here I have used B: drive in my PC
                      #Add as many folders you want here

    create_table_query = """
    CREATE TABLE IF NOT EXISTS monitored_files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_path VARCHAR(255),
        file_name VARCHAR(255),
        file_extension VARCHAR(10),
        file_size INT,
        event_type VARCHAR(20),
        creation_time DATETIME,
        modification_time DATETIME,
        deletion_time DATETIME
    )
    """
    cursor.execute(create_table_query)

    process1 = multiprocessing.Process(target=monitor_single_folder, args=(folder1,))
    process2 = multiprocessing.Process(target=monitor_single_folder, args=(folder2,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    cursor.close()
    db_connection.close()


