<?php

class PetsLoginModel extends CI_Model
{
    private $login_dets = array();
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

    }

    private function get_select_query()
    {

        $email = $this->login_dets["email"];
        $password = $this->login_dets["password"];
        $where = array(
            "email" => $email,
            "password" => $password
        );

//        "SELECT * FROM users WHERE email = '$email' AND password = '$password'";
        return $where;
    }

    private function is_login_details_valid()
    {
        $select_query = $this->get_select_query();
        $this->result =  $this->db->get_where("users", $select_query);
        if($this->result->num_rows() != 0){
            $this->row = $this->result->result();
            if ($this->row[0]->email != $this->login_dets["email"] and $this->row[0]->password != $this->login_dets["password"])
            {
                return false;
            }}
        else{
            return false;
        }
        return true;
    }

    public function get_role_id()
    {
        $this->load->database();
        $this->get_login_details();
        if($this->is_login_details_valid())
        {
            return $this->row[0]->roleid;
        }
        else{
            return 999;
        }
    }

    private function get_query_for_username()
    {


        $userid = $this->row[0]->userid;

        $where = array(
            "userid" => $userid
        );

//        "SELECT * FROM users WHERE email = '$email' AND password = '$password'";
        return $where;

    }

    public function get_user_name()
    {
        $where = $this->get_query_for_username();
        $result = $this->db->get_where("clients", $where);
        $this->client_row = $result->result();
        return $this->client_row[0]->fname;
    }
}

?>

