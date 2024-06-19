<!-- VIEWING THE FILE-->

<?php
        if (isset($_POST['show'])) {
            if($_POST['refnum'] == "") {
                echo "Please, specify model reference number";
            } else {
            $model = $_POST['refnum'].".ifc.xkt";
            $model_py = $_POST['refnum'].".ifc";
            //echo $model;
            
            }
        }
?>