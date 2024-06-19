
<h4 style="text-align: center;">Project information</h4>
<form method="POST">
    <input type="text" name="reference" value="<?php echo (isset($_POST['refnum']) ? $_POST['refnum'] : '') ?>" placeholder="Model reference number" style="width: 240px;">

    <label for="pr_type">Type of building:</label>
    <br>
    <select name="pr_type" id="pr_type">
        <option value="Residential" selected>Residential</option>
        <option value="Commercial">Commercial</option>
        <option value="Industrial">Industrial</option>
        <option value="Infrastructure">Infrastructure</option>
        <option value="Agricultural">Agricultural</option>
        <option value="Public institution">Public institution</option>
    </select><br>

    <label for="pr_year">Year of construction:</label><br>
    <select name="pr_year" id="pr_year">
        <option value="Before1919" selected>Before1919</option>
        <option value="1920-1945">1920-1945</option>
        <option value="1946-1960">1946-1960</option>
        <option value="1961-1990">1961-1990</option>
        <option value="1991-2005">1991-2005</option>
        <option value="2006-2011">2006-2011</option>
        <option value="After2012">After2012</option>
    </select><br>

    <label for="pr_docs">Available documentation:</label><br>
    <input type="text" name="pr_docs" id="pr_docs" placeholder="Link to available documentation" style="width: 240px;">

    <label for="pr_start">Demolition start date:</label><br>
    <input type="date" id="pr_start" name="pr_start" value="2022-07-17" min="2022-07-17" max="2099-12-31"><br>
    <sub><input type="checkbox" id="declare" name="declare" value="declare"></sub>
    <label for="declare">I am informed and agree with: </label>

    <br>
    <sub>- The elements that did not pass validation will not be processed. <br> - The location of the project is correct. <br> - The model will be sent to the market </sub>

    <a href="index.php">
        <button type="submit" name="pr_send" value="pr_send" style="width: 240px;">
            SEND THE DATA
        </button>
        <!-- <input type="button" name="pr_send" value="SEND THE DATA" style="width: 240px;" /> -->
    </a>
</form>

<?php


if (isset($_POST['pr_send'])) {

    $data1 = $_POST['reference'];
    $data2 = $_POST['pr_type'];
    $data3 = $_POST['pr_year'];
    $data4 = $_POST['pr_docs'];
    $data5 = $_POST['pr_start'];
    $data6 = $_SESSION["useruid"];
    $model_py = $_POST['reference'] . ".ifc";
    
    $_SESSION['reference'] = $data1;

    require_once 'includes/dbh.inc.php';
    require_once 'includes/functions.inc.php';

    if (empty($data4)) {
        $data4 = "None";
    }
    if (empty($data1)) {
        header("location: validation.php?error=emptyrefnumber");
        exit();
    }
    if (!isset($_POST['declare'])) {
        header("location: validation.php?error=emptyagreement");

        exit();
    }
    if (refExists ($conn, $data1)) {
        header("location: validation.php?error=referenceexists");
        exit();
    }

    $outputscript = (shell_exec("dbinsert.py 2>&1" . $data1 . " " . $data2 . " " . $data3 . " " . $data4 . " " . $data5 . " " . $data6 . " " . $model_py));
    // print_r($outputscript);
    // echo $data1."<br>";
    // echo $data2."<br>";
    // echo $data3."<br>";
    // echo $data4."<br>";
    // echo $data5."<br>";
    $preparespecification = (shell_exec("dbelementsparse.py 2>&1" . $model_py));
    $_SESSION['persentageOfPassed'] = $preparespecification;
?>

    <script type="text/javascript">
        window.location = "datasent.php";
    </script>

<?php

}
?>