import mysql.connector
import json

class DatabaseSingleton:
    """
    A singleton class for managing a database connection.

    This class ensures that only one database connection is created and shared across the application.

    Attributes
    ----------
    conn : mysql.connector.connection.MySQLConnection or None
        The active database connection.

    Methods
    -------
    new_conn()
        Establishes a new database connection using configuration settings.
    close_conn()
        Closes the database connection.
    readconfig(key)
        Reads a database configuration value from a JSON file.
    """
    conn = None

    def __new__(cls):
        """
        Ensures a single instance of the database connection.

        Returns
        -------
        mysql.connector.connection.MySQLConnection
            The active database connection.

        Examples
        --------
        >>> db1 = DatabaseSingleton()
        >>> db2 = DatabaseSingleton()
        >>> db1 is db2
        True
        """
        if not cls.conn:
            cls.new_conn()
        return cls.conn
    
    @classmethod
    def new_conn(cls):
        """
        Establishes a new database connection using configuration settings.

        This method retrieves connection details from the configuration file and connects to the database.

        Examples
        --------
        >>> DatabaseSingleton.new_conn()
        """
        connection = mysql.connector.connect(
        host=cls.readconfig("host"),
        port=cls.readconfig("port"),
        user=cls.readconfig("user"),
        password=cls.readconfig("password"),
        database=cls.readconfig("database"),
        )
        cls.conn = connection
    
    @classmethod
    def close_conn(cls):
        """
        Closes the active database connection if it exists.

        This method ensures that resources are properly released.

        Examples
        --------
        >>> DatabaseSingleton.close_conn()
        """
        if(cls.conn):
            cls.conn.close()
            cls.conn = None

    @classmethod
    def readconfig(cls,key):
        """
        Reads a database configuration value from a JSON file.

        Parameters
        ----------
        key : str
            The configuration key to retrieve.

        Returns
        -------
        str or None
            The corresponding configuration value, or None if the key is not found.

        Examples
        --------
        >>> DatabaseSingleton.readconfig("host")
        '127.0.0.1'
        """
        with open("./Bank/appconfig.json","r") as f:
            config = json.load(f)
            return config.get("database").get(key)

