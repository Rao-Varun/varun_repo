<div class="content">
    <img src="<?php echo base_url();?>images/petstore_index_banner.png" alt="index banner">
    <h2>Login</h2>
    <p>Required information is marked withan asterik(*)</p>
    <form name="cs_form" action="<?php echo base_url();?>" method="post">
        <div class=forms>
            <?php echo validation_errors('<div class="warning_msgs">','</div>')?>
            <input type="hidden" name="form_name" value="login">
            <div class=labels>
                <label>*E-mail:</label>
            </div>
            <div class=inputs>
                <input type="text" name="email"/><br/>
            </div>
            <div class=labels>
                <label>*Password:</label>
            </div>
            <div class=inputs>
                <input type="password" name="password"/><br/>
            </div>
            <div class=labels>
                <input type="submit"  value="Submit"/>
            </div>
        </div>
    </form>
    </br></br>
