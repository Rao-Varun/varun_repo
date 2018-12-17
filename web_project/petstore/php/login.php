<?php
require("db_ops.php");

class Login
{
    private $db_connect;
    private $login_dets = array();

    function __construct()
    {
        $this->db_connect = new DBOps("varunrao_client", "clientclient", "localhost");
        $this->db_connect->create_db_connection();
    }

    private function validate_form($key, $regx)
    {
        $subject = $this->login_dets[$key];
        if(!preg_match($regx, $subject)){
            die("Invalid form $key :: $subject");
        }

    }

    private function get_login_details()
    {
        foreach ($_POST as $key => $value) {
            $this->login_dets[$key] = $value;
        }
        $this->validate_form("email", "/[\w]+[._]*[\w\d]+\@[a-z]+\.[a-z]+/i");
        $password = $this->login_dets["password"];
        if($password == ""){
            die("Empty password");
        }
    }

    private function get_select_query()
    {
        $email = $this->login_dets["email"];
        $password = $this->login_dets["password"];
        $select_query = "SELECT * FROM users WHERE email = '$email' AND password = '$password'";
        return $select_query;
    }

    private function Verify_if_login_details_are_valid()
    {
        $select_query = $this->get_select_query();
        $result = $this->db_connect->execute_select_query($select_query);
//        print_r($result);
        if(count($result) != 0){
        if ($result[0]["email"] != $this->login_dets["email"] and $result[0]["password"] != $this->login_dets["password"]) {
            die("invalid user");
        }}
        else{
            die("invalid input");
        }
        return $result;
    }

    private function execute_required_html_page($result)
    {
//        print_r($result[0]["roleid"]);
        if ($result[0]["roleid"] == 1) {
            $html_file = "../loginBusiness.html";
        } elseif ($result[0]["roleid"] == 2) {
            $html_file = "../loginClient.html";
        }
        echo file_get_contents($html_file);
    }

    public function perform_login_validation()
    {
        $this->get_login_details();
        $result = $this->Verify_if_login_details_are_valid();
        $this->execute_required_html_page($result);
    }
}

$login = new Login();
$login->perform_login_validation();

?>