 <!-- UPLOADING THE FILE-->

 <?php
        if(isset($_POST['submit'])) {
            $file = $_FILES['file'];
            
            //print_r($file);

            $file_name = $_FILES['file']['name'];
            $file_tempname = $_FILES['file']['tmp_name'];
            $file_size = $_FILES['file']['size'];
            $file_error = $_FILES['file']['error'];
            $file_type = $_FILES['file']['type'];

            $file_ext = explode('.', $file_name);
            $file_actual_ext = strtolower(end($file_ext));

            $allowed = array('ifc', 'xkt');
            if(in_array($file_actual_ext, $allowed)) {
                if ($file_error === 0) {
                    if ($file_size < 50000000) {
                        $file_name_new = uniqid('',true);  //Creates new unique name of file
                        $file_name_new_ext = $file_name_new.'.'. $file_actual_ext;
                        $file_dest = 'uploads/'.$file_name_new_ext;

                        //Create directory with images
                        $foldername =  'uploads/'.$file_name_new;
                        mkdir($foldername);
                        foreach($_FILES['files']['name'] as $i => $name){
  		                if(strlen($_FILES['files']['name'][$i]) > 1){  
                        move_uploaded_file($_FILES['files']['tmp_name'][$i],$foldername."/".$name);
  		                }}





                        move_uploaded_file($file_tempname, $file_dest);
                        //header('Location: index.php?uploadsuccess');
                        echo "Your file reference is: ".$file_name_new;
                        echo '<script type="text/javascript">alert("You have uploaded the file. Please, write down your reference number: '.$file_name_new.'");</script>';
                        
                    } else {
                        echo "The size is too big";
                    }

                }   else {
                    echo "There was an error uploading your file";
                }
            } else {
                echo "Please, choose IFC file";
            }
            
        }
        ?>