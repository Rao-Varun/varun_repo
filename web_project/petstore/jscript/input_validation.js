function validate_name() {
    var name = document.forms["cs_form"]["first_name"].value;
    var name_pattern = /[a-zA-Z]+/i;
    var n = name.search(name_pattern);
    if (n === -1) {
        alert("Invalid First name");
        return false;
    }
    return true;
}

function validate_last_name() {
    var name = document.forms["cs_form"]["last_name"].value;
    var name_pattern = /[a-zA-Z]+/i;
    var n = name.search(name_pattern);
    if (n === -1) {
        alert("Invalid Last name");
        return false;
    }
    return true;
}

function validate_phone_number() {
    var name = document.forms["cs_form"]["phone"].value;
    var name_pattern = /{^\+?\d?\d?\d\d\d\d\d\d\d\d\d\d$/i;
    var n = name.search(name_pattern);
    if (n === -1) {
        alert("Invalid phone number");
        return false;
    }
    return true;
}

function validate_email() {
    var name = document.forms["cs_form"]["email"].value;
    var name_pattern = /[\w]+[._]*[\w\d]+\@[a-z]+\.[a-z]+/i;
    var n = name.search(name_pattern);
    if (n === -1) {
        alert("Invalid email");
        return false;
    }
    return true;

}

function validate_business_name(){

    var name = document.forms["cs_form"]["bname"].value;
    var name_pattern = /\w+/i;
    var n = name.search(name_pattern);
    if (n === -1) {
        alert("Invalid business name");
        return false;
    }
    return true;

}

function validate_password(){
    var password = document.forms["cs_form"]["password"].value;

    if (password == "") {
        alert("Password is empty. Enter password");
        return false;
    }
    return true;

}

function validate_client_service_form() {
    var val1 = validate_name();
    var val2 = validate_last_name();
    var val3 = true; //validate_phone_number();
    var val4 = validate_email();
    var val5 = validate_business_name();
    if(val1 && val2 && val3 && val4 && val5)
    {
        document.forms["cs_forms"].submit();
    }
    else{
        return false;
    }

}

function validate_login_form(){
    var val1 = validate_email();
    var val2 = validate_password();
    if(val1 && val2){
        document.forms["cs_forms"].submit();
    }
    else{
        return false;
    }
}


function validate_contactus_form() {
    var val1 = validate_name();
    var val2 = validate_last_name();
    var val3 = true; //validate_phone_number();
    var val4 = validate_email();

    if(val1 && val2 && val3 && val4)
    {
        document.forms["cs_forms"].submit();
    }
    else{
        return false;
    }

}

