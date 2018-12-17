<div class="content">
    <img src="<?php echo base_url()?>images/petstore_index_banner.png" alt="index banner">
    <h2>My Pet</h2>
    <p>Required information is marked withan asterik(*)</p>
    <form method="post" action="<?php echo base_url()?>">
        <div class=forms>
            <?php echo validation_errors('<div class="warning_msgs">','</div>')?>
            <input type="hidden" name="form_name" value="login_client_insert">
            <div class=labels>
                <label>Client Name:</label>
            </div>
            <div class=inputs>
                <input type="text" name="client_name"/><br/>
            </div>
            <div class=labels>
                <label>*My Pet:</label>
            </div>
            <div class=inputs>
                <input type="text" name="my_pet"/><br/>
            </div>
            <div class=labels>
                <input type="submit" value="Add New One"/>
            </div>
        </div>
    </form>
    </br></br>