# Blender Addon for GLTF
![screenshot](https://user-images.githubusercontent.com/15867665/120985367-825c6280-c7b6-11eb-8046-b248fa8c1653.png)

### Installation
download this repo, then install it through to Blender Preferences > Add-ons -> Install

### Bake Camera
It's recommend to have only 1 camera as the script will pick the first available camera. It will then export a glb file containing only the camera and its action baked

### KHR Unlit and EXT_mesh_gpu_instancing

These features requires the module [@gltf-transform/cli](https://gltf-transform.donmccurdy.com/cli.html) on your system:
`npm install --global @gltf-transform/cli`
