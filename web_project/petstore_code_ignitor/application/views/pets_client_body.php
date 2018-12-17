<div class="content">
    <img src="<?php echo base_url();?>images/petstore_index_banner.png" alt="index banner">
    <h2>Client</h2>
    <p>Required information is marked withan asterik(*)</p>
    <form name="cs_form" method="post" action="<?php echo base_url();?>">
        <input type="hidden" name="role_id" value="2">
        <input type="hidden" name="description" value="client">
        <div class=forms>
            <?php echo validation_errors('<div class="warning_msgs">','</div>')?>
            <input type="hidden" name="form_name" value="client_insert">
            <div class=labels>
                <label>*First Name:</label>
            </div>
            <div class=inputs>
                <input type="text" name="first_name"/><br/>
            </div>
            <div class=labels>
                <label>*Last Name:</label>
            </div>
            <div class=inputs>
                <input type="text" name="last_name"/><br/>
            </div>
            <div class=labels>
                <label>*E-mail:</label>
            </div>
            <div class=inputs>
                <input type="text" name="email"/><br/>
            </div>
            <div class=labels>
                <label>Phone:</label>
            </div>
            <div class=inputs>
                <input type="text" name="phone"/><br/>
            </div>
            <div class=labels>
                <label>Bussiness Name:</label>
            </div>
            <div class=inputs>
                <input type="text" name="bname"/><br/>
            </div>
            <div class=labels>
                <input type="submit" onclick="return validate_client_service_form();"/>
            </div>
        </div>
    </form>
    </br></br>
