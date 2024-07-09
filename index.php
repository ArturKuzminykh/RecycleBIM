<?php
include_once 'includes/header.php'
?>

<section style="text-align: center;">
<br>
    <?php
        if (isset($_SESSION["useruid"])) {
            echo '<p>Hello, <b>'.$_SESSION["useruid"] .'</b>. Welcome to the RecycleBIM Platform! Please, check the manual before starting to use the platform. We wish you a nice experience here</p>';
            
        } 
    ?>
    <p><img src='img/hello2.jpg' style="height:600px;float:center; position:relative; top:20px; " ></p>
    <!--<h2>This is section</h2>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Laborum ad, alias amet minima aperiam dicta dignissimos id nostrum, asperiores cum eius cumque. Cupiditate obcaecati nobis aperiam eius doloribus iure amet eaque a in, magnam repellendus ea alias vel dolores eos voluptatum culpa quaerat inventore suscipit ratione at ut architecto voluptas dolorem. Eos voluptatibus tenetur magni earum. Est accusamus repudiandae quae modi distinctio nostrum quisquam, eum nihil a quam? Repudiandae sed beatae fugiat, harum temporibus amet laborum laudantium ullam asperiores eum enim tempore adipisci incidunt autem, exercitationem voluptate corrupti reprehenderit quo natus praesentium in illum obcaecati esse ad. Quam atque quos unde, perferendis rem dicta hic maxime itaque dolorum architecto, illum, obcaecati voluptatum libero dolores. Porro omnis eius nam a itaque voluptate tempore ullam amet facere at suscipit dolores rem sunt error, quia unde reiciendis! Repellat ipsa sit porro quam suscipit aut adipisci ipsam modi nesciunt accusamus, voluptatem numquam reprehenderit ipsum tempora rem saepe nobis consectetur cum recusandae animi quis dolore. Saepe, veritatis libero vero qui itaque rerum voluptates fugiat in! Optio totam error eos adipisci tempora natus blanditiis repellendus. A eaque accusantium, consequuntur impedit eligendi, ullam et laborum dicta ipsa ratione cum eveniet molestiae, odio labore quis! Aspernatur, harum illo.</p>-->
</section>
</body>

</html>