
# Blender Addon for GLTF
![ezgif com-gif-maker](https://user-images.githubusercontent.com/15867665/120999352-fc471880-c7c3-11eb-9bfb-16e4de6d5263.gif)

### Installation
download this repo, then install it through to Blender Preferences > Add-ons -> Install

### Bake Camera
It's recommend to have only 1 camera as the script will pick the first available camera. It will then export a glb file containing only the camera and its action baked

### KHR Unlit and EXT_mesh_gpu_instancing

These features requires the module [@gltf-transform/cli](https://gltf-transform.donmccurdy.com/cli.html) on your system:

The logs are available in the info tab of blender

`npm install --global @gltf-transform/cli`

--- 
### Todo
- Bake camera: Handle multiple camera
- Bake camera: Handle error if no camera are in the scene
- Bake camera: Handle error if the camera has no animations or frame_end
