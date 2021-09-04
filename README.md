
# Blender Addon for GLTF
![ezgif com-gif-maker](https://user-images.githubusercontent.com/15867665/120999352-fc471880-c7c3-11eb-9bfb-16e4de6d5263.gif)


### Export curves to es6
See [blender_curve_export](https://github.com/utsuboco/blender_curve_export)

### Installation
download this repo, then install it through to Blender Preferences > Add-ons -> Install

### Bake Camera
It's recommend to have only 1 camera as the script will pick the first available camera. It will export a glb file containing only the camera named `filename_camera.glb` and its action baked.

### KHR Unlit and EXT_mesh_gpu_instancing

First you need to [start Blender through the command line](https://docs.blender.org/manual/en/2.79/render/workflows/command_line.html). You can speed up the process by making an alias:
```Right click on the Blender icon in the Applications folder and select "Show Package contents". Make an alias of Contents/MacOS/Blender by right clicking and selecting "Make Alias". Rename it and move it somewhere you like.```


These features requires the module [@gltf-transform/cli](https://gltf-transform.donmccurdy.com/cli.html) on your system:

The logs are available in the info tab of blender

`npm install --global @gltf-transform/cli`

#### EXT_mesh_gpu_instancing
EXT_mesh_gpu_instancing will export a glb file containing only the gpu compatible collections under the name `filename_gpu.glb`.

### TLDR:
- `filename_camera.glb` for camera baked animation.
- `filename_gpu.glb` for instances.
- `filename.glb` for the typical gltf export.

--- 
### Todo
- Bake camera: Handle multiple camera
- Bake camera: Handle error if no camera are in the scene
- Bake camera: Handle error if the camera has no animations or frame_end
