<div class="content">
    <img src="<?php echo base_url();?>images/petstore_contactus_banner.png" alt="index banner">
    <h2>Contact Us</h2>
    <p>Required information is marked withan asterik(*)</p>
    <form name="cs_form" action="<?php echo base_url();?>" method="post">
        <div class=forms>
            <?php echo validation_errors('<div class="warning_msgs">','</div>')?>
            <input type="hidden" name="form_name" value="contactus_insert">
            <div class=contactus_labels>
                <label>*First Name:</label>
            </div>
            <div class=contactus_inputs>
                <input type="text" name="first_name"/><br/>
            </div>
            <div class=contactus_labels>
                <label>*Last Name:</label>
            </div>
            <div class=contactus_inputs>
                <input type="text" name="last_name"/><br/>
            </div>
            <div class=contactus_labels>
                <label>*E-mail:</label>
            </div>
            <div class=contactus_inputs>
                <input type="text" name="email"/><br/>
            </div>
            <div class=contactus_labels>
                <label>Phone:</label>
            </div>
            <div class=contactus_inputs>
                <input type="text" name="phone"/><br/>
            </div>
            <div class=contactus_labels>
                <label>Comments:</label>
            </div>
            <div class=contactus_inputs>
                <textarea name="comments" rows="4"/></textarea><br/>
            </div>
            <div class=contactus_labels>
                <input type="submit" value="Submit" onclick="return validate_contactus_form();"/>
            </div>
        </div>
    </form>
    </br></br>
