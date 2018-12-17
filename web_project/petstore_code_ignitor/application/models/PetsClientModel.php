<?php

class PetsClientModel extends CI_Model
{

    private $client_service_dets = array();



    private function get_insert_values(array $insert_fields)
    {
        $insert_string = "";
        foreach ($insert_fields as $field) {
            $value = $this->client_service_dets[$field];
            if ($insert_string == "") {
                $insert_string = "'$value'";
            } else {
                $insert_string = $insert_string . ", '$value'";
            }
        }
        return $insert_string;
    }

    private function get_client_or_service_details()
    {

        foreach ($_POST as $key => $value) {
            $this->client_service_dets[$key] = $value;
        }
    }

    private function validate_form($key, $regx)
    {
        $subject = $this->client_service_dets[$key];
        if (!preg_match($regx, $subject)) {
            die("Invalid form $key :: $subject");
        }

    }

    private function validate_client_service_details()
    {
        $this->validate_form("first_name", "/[a-zA-Z]+/i");
        $this->validate_form("last_name", "/[a-zA-Z]+/i");
        $this->validate_form("email", "/[\w]+[._]*[\w\d]+\@[a-z]+\.[a-z]+/i");
        $this->validate_form("bname", "/\w+/i");

    }

    private function create_client_or_service_id()
    {
        $first_name = $this->client_service_dets['first_name'];
        $last_name = $this->client_service_dets['last_name'];
        return $first_name . "_" . $last_name;
    }

    private function get_client_db_insert_query()
    {
        $insert_values =
            array("clientid" => $this->client_service_dets["client_id"],
                "fname" => $this->client_service_dets["first_name"],
                "lname" => $this->client_service_dets["last_name"],
                "email" => $this->client_service_dets["email"],
                "phone" => $this->client_service_dets["phone"],
                "serviceid" => $this->client_service_dets["client_id"],
                "userid" => $this->client_service_dets["client_id"]);

        return $insert_values;
    }

    private function insert_client_or_service_details_to_client_db()
    {
        $this->client_service_dets["client_id"] = $this->create_client_or_service_id();
        $clientdb_query = $this->get_client_db_insert_query();
        $this->db->insert("clients", $clientdb_query);
    }

    private function get_users_db_insert_query()
    {
        $insert_values = array(
            "userid" => $this->client_service_dets["client_id"],
            "password" => $this->client_service_dets["password"],
            "email" => $this->client_service_dets["email"],
            "roleid" => $this->client_service_dets["role_id"]);

        return $insert_values;
    }

    private function get_password_for_user()
    {
        $first_name = $this->client_service_dets['first_name'];
        $last_name = $this->client_service_dets['last_name'];
        return $first_name . "_" . $last_name;
    }

    private function insert_user_details_to_user_db()
    {
        $this->client_service_dets['password'] = $this->get_password_for_user();
        $usersdb_query = $this->get_users_db_insert_query();
//        echo "<br/> userdb_query :: $usersdb_query";
        $this->db->insert("users", $usersdb_query);


    }

    private function get_roles_db_query()
    {
        $insert_values = array(
            "roleid" => $this->client_service_dets["role_id"],
            "date" => $this->client_service_dets["date"],
            "description" => $this->client_service_dets["description"]);

        return $insert_values;
    }

    private function insert_role_details_to_roles_db()
    {
        $this->client_service_dets["date"] = date("l jS \of F Y h:i:s A");
        $roledb_query = $this->get_roles_db_query();
        $this->db->insert("roles", $roledb_query);
    }

    private function send_user_password_to_user()
    {
        $subject = "Your Password";
        $to = $this->client_service_dets["email"];
        $password = $this->client_service_dets['password'];
        $message = "Your password is<br/>$password";
        $header = "From: admin@petstore\n\r";
        mail($to, $subject, $message, $header);
    }


    private function get_service_db_query()
    {
        $this->client_service_dets["service_description"] = "NA";
        $insert_values = array(
            "serviceid" => $this->client_service_dets["client_id"],
            "servicedescription" => $this->client_service_dets["service_description"],
            "bussinessid" => $this->client_service_dets["client_id"]);
        return $insert_values;
    }

    private function insert_client_or_service_details_to_service_db()
    {
        $servicedb_query = $this->get_service_db_query();
        $this->db->insert("services", $servicedb_query);
//        echo "<br/>servicedb_query $servicedb_query";

    }

    private function get_business_db_query()
    {
//        echo "client server dets";
//        print_r($this->client_service_dets);
        $insert_values = array(
            "bussinessid" => $this->client_service_dets["client_id"],
            "bname" => $this->client_service_dets["bname"]);
        return $insert_values;
    }

    private function insert_business_details_to_business_db()
    {
        $businessdb_query = $this->get_business_db_query();
//        echo "<br/>businessdb_query $businessdb_query";
        $this->db->insert("bussiness",$businessdb_query);
//        echo "<br/>businessdb_query $businessdb_query";
    }


    public function insert_client_service_info_to_db()
    {
        $this->load->database();
        $this->get_client_or_service_details();
//        $this->validate_client_service_details();
//        print_r($this->client_service_dets);
//        echo "<br/>";
//        echo $this->client_service_dets["first_name"];
        $this->insert_client_or_service_details_to_client_db();
        $this->insert_user_details_to_user_db();
        $this->insert_role_details_to_roles_db();
//        $this->send_user_password_to_user();
        $this->insert_client_or_service_details_to_service_db();
        $this->insert_business_details_to_business_db();
//        $this->display_success_screen();

    }

    private function display_success_screen()
    {
        if ($this->client_service_dets["role_id"] == 2) {
            echo file_get_contents("../client_success.html");
        } else {
            echo file_get_contents("../service_success.html");
        }

    }


}

?>