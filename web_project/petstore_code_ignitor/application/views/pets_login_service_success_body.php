<div class="content">
    <img src="<?php echo base_url()?>images/petstore_index_banner.png" alt="index banner">
    <h2>My Business</h2>
    <p>Details received succesfully.</p>
    <p>Required information is marked withan asterik(*)</p>
    <form method="post" action="<?php echo base_url()?>">
        <div class=forms>
            <input type="hidden" name="form_name" value="login_service_insert">
            <div class=labels>
                <label>Business Name:</label>
            </div>
            <div class=inputs>
                <input type="text" name="business_name"/><br/>
            </div>
            <div class=labels>
                <label>*Service:</label>
            </div>
            <div class=inputs>
                <input type="text" name="service"/><br/>
            </div>
            <div class=labels>
                <input type="submit" value="Add New One"/>
            </div>
        </div>
    </form>
    </br></br>