<?php
    include_once 'includes/header.php';

    require_once 'includes/dbh.inc.php';
    ?>

<div class = "tablesql">


    <?php

    $reference =  $_SESSION['reference'];
    $passedRatio = $_SESSION['persentageOfPassed'];

    

    $sql = "SELECT * FROM projectbuildingobjects WHERE modelReference = '$reference';";
    $result = mysqli_query($conn, $sql);
    $resultCheck = mysqli_num_rows($result);

    if ($resultCheck > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
        $img_ref = 'uploads/' . $reference . '/' . $row['documentation'];
    ?>
    <table tableborder ="1"  id="bldobjects">
            <tr>
                <td> <?php echo $row['objectClass'] ?> </td>
                <td> <?php echo $row['typeName'] ?> </td>
                <td> <?php echo $row['declaredUnit'] ?> </td>
                <td> <?php echo $row['materialCompounPerDeclareUnit'] ?> </td>
                <td> <?php echo $row['totalQuantityOfMaterials'] ?> </td>
                <td> <?php echo $row['referenceInModel'] ?> </td>
                <td> <a href="<?php echo $img_ref ?>" target="_blank"> <?php echo $row['documentation'] ?> </a></td>
            </tr>

    <?php
        }
    }
    ?>
    </table>
</div>
<script>
    alert("Your model was successfully uploaded!")
</script>
<?php
   print_r($passedRatio);
    ?>

</body>

</html>
<?php
