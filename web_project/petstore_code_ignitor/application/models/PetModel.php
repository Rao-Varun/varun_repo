<?php

class PetModel extends CI_Model
{

    private function get_query_for_contactus()
    {
        $contactus = array(
            'first_name' => $_POST["first_name"],
            'last_name' => $_POST["last_name"],
            'email' => $_POST["email"],
            'phone' => $_POST["phone"],
            'comments' => $_POST["comments"],
        );
        return $contactus;
    }

    public function insert_contact_us_details()
    {
        $this->load->database();
        $query = $this->get_query_for_contactus();
        $this->db->insert('contactUs', $query);
    }




}


?>
