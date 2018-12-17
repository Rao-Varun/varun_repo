<?php

Class DBOps
{
	private $username;
	private $password;
	private $servername;
    private $connection;

	function __construct($username, $password, $servername)
	{
		$this->username=$username;
		$this->password=$password;
		$this->servername=$servername;
	}

	public function create_db_connection()
    {	
    	try{
//    		echo "vars are $this->username  $this->password  $this->servername";
	    	$this->connection = new PDO("mysql:host=".$this->servername.";dbname=varunrao_petstore", $this->username, $this->password);
	    	// set the PDO error mode to exception
	    	$this->connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
//	    	echo "Connected successfully";
	    }
	    catch(PDOException $e)
    	{
    	   echo "DB connection error: " . $e->getMessage();
    	}
    }

    public function execute_insert_query($query)
    {	try{
            $stmt = $this->connection->prepare($query);
	    	if ($stmt->execute())
	    	{
	    		return TRUE;
	    	}
	    	else
	    	{
	    		die("Row not added to db");
	    	}
	    }
	    catch(PDOException $e)
    	{
    	   echo "DB connection error: " . $e->getMessage();
    	}
    }

    public function execute_select_query($query)
    {
    	try{
    		$result = $this->connection->query("$query")->fetchAll();
    		return $result;
    	}
    	catch(PDOException $e)
    	{
    	   echo "DB connection error: " . $e->getMessage();
    	}
    }

}
?>