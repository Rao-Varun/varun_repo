<?php

class PetsController extends CI_Controller
{

    public function index()
    {
        $this->load->library('email');
        $this->load->library("form_validation");
        $this->load->helper('url');
        $this->load->view("pets_header");
        $this->display_required_page_body();
        $this->display_end_template();

    }

    private function display_basic_template()
    {
        $this->load->view("pets_basic_body");
    }

    private function display_end_template()
    {
        $this->load->view("pets_footer");
    }

    private function about_us()
    {
        $this->load->view("pets_about_us_body");
    }

    private function index_page()
    {
        $this->load->view("pets_index_body");
    }

    private function contact_us()
    {
        $this->load->view("pets_contactus_body");
    }

    private function client()
    {
        $this->load->view("pets_client_body");
    }

    private function service()
    {
        $this->load->view("pets_service_body");
    }

    private function login()
    {
        $this->load->view("pets_login_body");
    }

    private function get_navigation_page()
    {
        switch ($_GET["page"]) {
            case "aboutus":
                $this->about_us();
                break;

            case "contactus":
                $this->contact_us();
                break;

            case "client":
                $this->client();
                break;

            case "service":
                $this->service();
                break;

            case "login":
                $this->login();
                break;

            case "login_verify":
                break;
        }

    }

    private function perform_login_form_validation()
    {
        $this->form_validation->set_rules("email", "E-mail", "required|regex_match[/[\w]+[._]*[\w\d]+\@[a-z]+\.[a-z]+/]");
        $this->form_validation->set_rules("password", "Password", "required");
        return $this->form_validation->run();

    }

    private function perform_login_operation()
    {

        if (!$this->perform_login_form_validation()) {
            $this->login();
            return;
        }
        $this->load->model("PetsLoginModel");
        $roleid = $this->PetsLoginModel->get_role_id();
        switch ($roleid) {
            case 1:
                $this->load->view("pets_login_basic_body");
                $this->load->view("pets_login_service_body");
                break;
            case 2:

                $this->load->view("pets_login_basic_body");
                $this->load->view("pets_login_client_body");
                break;
            default:
                $this->display_basic_template();
                $this->load->view("pets_login_failure_body");
                break;
        }


    }

    private function display_contact_us_success()
    {
        $this->load->view("pets_contactus_success_body");
    }

    public function perform_contactus_form_validation()
    {
        $this->form_validation->set_rules("fist_name", "First Name", "required", "regex_match[/^[a-zA-Z][a-zA-Z]$+/]");
        $this->form_validation->set_rules("last_name", "Last Name", "required", "regex_match[/[a-zA-Z]+/]");
        $this->form_validation->set_rules("email", "E-mail", "required|regex_match[/[\w]+[._]*[\w\d]+\@[a-z]+\.[a-z]+/]");
        return $this->form_validation->run();
    }

    private function perform_contact_insert_operation()
    {
        if (!$this->perform_contactus_form_validation()) {
            $this->contact_us();
            return;
        }
        $this->load->model("PetModel");
        $this->PetModel->insert_contact_us_details();
        $this->display_contact_us_success();
    }

    private function display_client_success()
    {
        $this->load->view("pets_client_success_body");
    }

    private function display_service_success()
    {
        $this->load->view("pets_service_success_body");
    }

    private function is_client_service_form_valid()
    {
        $this->form_validation->set_rules("first_name", "First Name", "required|regex_match[/[a-zA-Z]+/]");
        $this->form_validation->set_rules("last_name", "Last Name", "required|regex_match[/[a-zA-Z]+/]");
        $this->form_validation->set_rules("email", "E-mail", "required|regex_match[/[\w]+[._]*[\w\d]+\@[a-z]+\.[a-z]+/]");
        return $this->form_validation->run();
    }

    private function send_user_password_to_user()
    {
        $subject = "Your Password";
        $to = $_POST["email"];
        $first = $_POST["first_name"];
        $last = $_POST["last_name"];
        $password = $first . "_" . $last;
        $message = "Your password is $password";
        $this->email->from('admin@petstore', 'admin');
        $this->email->to($to);
        $this->email->subject($subject);
        $this->email->message($message);
        $this->email->send();
    }


    private function perform_client_insert_operation()
    {
        if (!$this->is_client_service_form_valid()) {
            $this->client();
            return;
        }
        $this->load->model("PetsClientModel");
        $this->PetsClientModel->insert_client_service_info_to_db();
//        $this->send_user_password_to_user();
        $this->display_client_success();
    }

    private function perform_service_insert_operation()
    {
        if (!$this->is_client_service_form_valid()) {
            $this->service();
            return;
        }
        $this->load->model("PetsClientModel");
        $this->PetsClientModel->insert_client_service_info_to_db();
        $this->display_service_success();
    }

    private function is_login_client_form_valid()
    {
        $this->form_validation->set_rules("my_pet", "My Pet", "required|regex_match[/[a-zA-Z]+/]");
        return $this->form_validation->run();
    }


    private function perform_login_client_insertion()
    {
        if (!$this->is_login_client_form_valid()) {
            $this->load->view("pets_login_client_body");
            return;
        }
        $this->load->model("PetsLoginInsertModel");
        $this->PetsLoginInsertModel->insert_login_client_details();
        $this->load->view("pets_login_client_success_body");
    }

    private function is_login_business_form_valid()
    {
        $this->form_validation->set_rules("service", "Service", "required|regex_match[/[a-zA-Z]+/]");
        return $this->form_validation->run();
    }


    private function perform_login_business_insertion()
    {
        if (!$this->is_login_business_form_valid()) {
            $this->load->view("pets_login_service_body");
            return;
        }
        $this->load->model("PetsLoginInsertModel");
        $this->PetsLoginInsertModel->insert_login_business_details();
        $this->load->view("pets_login_service_success_body");
    }

    private function display_internal_pages()
    {

        $this->load->helper(array('form'));
        $this->load->library('form_validation');
        switch ($_POST["form_name"]) {
            case "login":
                $this->perform_login_operation();
                break;

            case "client_insert":
                $this->display_basic_template();
                $this->perform_client_insert_operation();

                break;

            case "contactus_insert":
                $this->display_basic_template();
                $this->perform_contact_insert_operation();
                break;

            case "service_insert":
                $this->display_basic_template();
                $this->perform_service_insert_operation();
                break;

            case "login_client_insert":
                $this->display_basic_template();
                $this->perform_login_client_insertion();
                break;

            case "login_service_insert":
                $this->display_basic_template();
                $this->perform_login_business_insertion();
                break;

            case "login_verify":
                $this->perform_login_operation();
        }
    }

    private function display_required_page_body()
    {
        if (isset($_GET["page"])) {
            $this->display_basic_template();
            $this->get_navigation_page();
        } elseif (isset($_POST["form_name"])) {
            $this->display_internal_pages();
        } else {
            $this->display_basic_template();
            $this->index_page();
        }

    }


}


?>