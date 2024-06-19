<?php
include_once 'includes/header.php'
?>
<div class="section_left">
    <form method="POST" enctype="multipart/form-data">
        <h4 style="text-align: center;">Upload your model (IFC file)</h4>
        <input type="file" name="file">
        <h4 style="text-align: center;">with images folder</h4>
        <input type="file" name="files[]" id="files" multiple directory="" webkitdirectory="" moxdirectory="" />
        <br>
        <button type="submit" name="submit" style="width: 240px;">UPLOAD</button>
    </form>
    <!-- UPLOADING THE FILE-->

    <?php include 'includes/upload.php'; ?>
    <br>
    <form method="POST">
        <h4 style="text-align: center;">Show the model</h4>
        <input type="text" name="refnum" value="<?php echo isset($_POST['refnum']) ? $_POST['refnum'] : '' ?>" placeholder="Model reference number" style="width: 240px;">
        
        <button type="submit" name="show" value="show" style="width: 240px;">
            SHOW THE MODEL
        </button>
    </form>
    <!-- VIEWING THE FILE-->

    <?php include 'includes/view.php' ?>
    <div id="treeViewContainer"></div>
</div>


<script type="module">
    //------------------------------------------------------------------------------------------------------------------
    // Import the modules we need for this example
    //------------------------------------------------------------------------------------------------------------------

    import {
        Viewer,
        XKTLoaderPlugin,
        NavCubePlugin,
        TreeViewPlugin
    } from "./dist/xeokit-sdk.min.es.js";

    //------------------------------------------------------------------------------------------------------------------
    // Create a Viewer, arrange the camera, tweak x-ray and highlight materials
    //------------------------------------------------------------------------------------------------------------------

    const viewer = new Viewer({
        canvasId: "my-Canvas",
        transparent: true
    });
    const cameraControl = viewer.cameraControl;
    const scene = viewer.scene;
    const cameraFlight = viewer.cameraFlight;

    cameraControl.followPointer = true;
    cameraControl.doublePickFlyTo = true;
    cameraFlight.duration = 1.0;
    cameraFlight.fitFOV = 25;

    viewer.camera.eye = [-2.56, 8.38, 8.27];
    viewer.camera.look = [13.44, 3.31, -14.83];
    viewer.camera.up = [0.10, 0.98, -0.14];

    viewer.scene.xrayMaterial.fillAlpha = 0.1;
    viewer.scene.xrayMaterial.fillColor = [0, 0, 0];
    viewer.scene.xrayMaterial.edgeAlpha = 0.4;
    viewer.scene.xrayMaterial.edgeColor = [0, 0, 0];

    viewer.scene.highlightMaterial.fill = false;
    viewer.scene.highlightMaterial.fillAlpha = 0.3;
    viewer.scene.highlightMaterial.edgeColor = [1, 1, 0];

    //------------------------------------------------------------------------------------------------------------------
    // Create a NavCube
    //------------------------------------------------------------------------------------------------------------------

    new NavCubePlugin(viewer, {
        canvasId: "my-CubeCanvas",
        visible: true,
        size: 250,
        alignment: "bottomRight",
        bottomMargin: 100,
        rightMargin: 10
    });

    //------------------------------------------------------------------------------------------------------------------
    // Create an IFC structure tree view
    //------------------------------------------------------------------------------------------------------------------

    const treeView = new TreeViewPlugin(viewer, {
        containerElement: document.getElementById("treeViewContainer"),
        autoExpandDepth: 1, // Initially expanding "types" makes for a lot of nodes to scroll though - let's not expand
        hierarchy: "types"
    });
    //------------------------------------------------------------------------------------------------------------------
    // Load model and metadata
    //------------------------------------------------------------------------------------------------------------------

    const xktLoader = new XKTLoaderPlugin(viewer);

    const model = xktLoader.load({
        id: "myModel",
        src: "<?= './models_xkt/' . $model ?>",
        excludeTypes: ["IfcSpace"],
        globalizeObjectIds: true, // to map GUIDs
        edges: true
    });


    //------------------------------------------------------------------------------------------------------------------
    // Click Entities to colorize them
    //------------------------------------------------------------------------------------------------------------------

    var lastEntity = null;
    var lastColorize = null;

    viewer.cameraControl.on("picked", (pickResult) => {

        if (!pickResult.entity) {
            return;
        }

        console.log(pickResult.entity.id);

        if (!lastEntity || pickResult.entity.id !== lastEntity.id) {

            if (lastEntity) {
                lastEntity.colorize = lastColorize;
            }

            lastEntity = pickResult.entity;
            lastColorize = pickResult.entity.colorize ? pickResult.entity.colorize.slice() : null;

            pickResult.entity.colorize = [0.0, 1.0, 0.0];
        }
    });

    viewer.cameraControl.on("pickedNothing", () => {
        if (lastEntity) {
            lastEntity.colorize = lastColorize;
            lastEntity = null;
        }
    });
</script>


<div class="canvas">
    <canvas id="my-Canvas"></canvas>
    <canvas id="my-CubeCanvas"></canvas>
</div>





</body>

</html>