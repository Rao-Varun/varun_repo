 <?php
       
    function get_query_for_contactus()
    {
        $first_name = $_POST["first_name"];
        $last_name = $_POST["last_name"];
        $email = $_POST["email"];
        $phone = $_POST["phone"];
        $comments = $_POST["comments"];
        $query= "INSERT INTO contactUs(first_name, last_name, email, phone, comments) VALUES('$first_name', '$last_name', '$email', '$phone', '$comments')";
        return $query;
    }

    function perform_insert_query()
    {   
        require("db_ops.php");
        $query = get_query_for_contactus();
        try
        {
            $db_ops = new DBOps("varunrao_client", "clientclient", "localhost");
            $db_ops->create_db_connection();
            $db_ops->execute_insert_query($query);
        }
        catch(PDOException $e)
        {
           echo "Connection failed: " . $e->getMessage();
        }
    }
    perform_insert_query();
 ?>