from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser


def read_db_config(filename='config.ini',section='mysql'):
    """ 
	Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def execute(query,db_config=read_db_config(),multi=False,commit=False):
    """
    Execute query passed as a string
    :query: query passed as string
    """
    conn = None
    result = None
    
    try:
        conn = MySQLConnection(**db_config)
        print('Connected...')
        
        cursor = conn.cursor()
        print('Executing...')
        cursor.execute(query,multi=multi)
        
        if commit:
            conn.commit()
        
        result = cursor.fetchall()
        print('Done...')
        
    except Error as error:
        print("Something Errored!!!\n\n\n")
        print(error)
        
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result
    
    
def insert(query,values,db_config=read_db_config(),commit=False):
    """
    Insert values into database
    """
    conn = None
    result = None
    
    try:
        conn = MySQLConnection(**db_config)
        print('Connected...')
        
        cursor = conn.cursor()
        print('Executing...')
        
        
        cursor.executemany(query,values)
        
        if commit:
            conn.commit()
        
        result = cursor.fetchall()
        print('Done...')
        
    except Error as error:
        print("Something Errored!!!\n\n\n")
        print(error)
        
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result