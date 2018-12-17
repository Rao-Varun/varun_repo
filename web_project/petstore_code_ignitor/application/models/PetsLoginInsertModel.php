<?php

class PetsLoginInsertModel extends CI_Model
{

    private function get_query_for_login_client()
    {
        $details = array(
            'client_name' => $_POST["client_name"],
            'my_pet' => $_POST["my_pet"]
        );
        return $details;
    }

    public function insert_login_client_details()
    {
        $this->load->database();
        $query = $this->get_query_for_login_client();
        $this->db->insert('login_client', $query);
    }

    private function get_query_for_login_business()
    {
        $details = array(
            'business_name' => $_POST["business_name"],
            'service' => $_POST["service"]
        );
        return $details;
    }

    public function insert_login_business_details()
    {
        $this->load->database();
        $query = $this->get_query_for_login_business();
        $this->db->insert('login_business', $query);
    }




}


?>
