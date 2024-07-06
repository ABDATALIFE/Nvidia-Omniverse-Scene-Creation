import omni
from pxr import Usd, UsdGeom, Gf, Sdf
import json

# Initialize Omniverse Kit
omni.kit.start()

# Create a function to add objects
def create_object(stage, object_name, object_type, position):
    # Create a new USD prim (USD is the file format used by Omniverse)
    path = f"/World/{object_name}"
    prim = stage.DefinePrim(path, object_type)
    
    # Set the transform (position) of the prim
    xform = UsdGeom.Xformable(prim)
    xform.AddTranslateOp().Set(Gf.Vec3f(*position))
    
    return prim

# Create a new stage (scene)
stage = Usd.Stage.CreateNew("omniverse://localhost/NVIDIA/synthetic_dataset.usd")

# Create the root Xform
root = UsdGeom.Xform.Define(stage, Sdf.Path("/World"))

# Add objects
objects = {
    "bicycle": ("Sphere", [0, 0, 0]),  # Placeholder using a sphere
    "car": ("Cube", [2, 0, 0]),        # Placeholder using a cube
    "dog": ("Cylinder", [4, 0, 0]),    # Placeholder using a cylinder
    "bottle": ("Cone", [6, 0, 0])      # Placeholder using a cone
}

for name, (object_type, position) in objects.items():
    create_object(stage, name, object_type, position)

# Save the stage
stage.GetRootLayer().Save()

# Function to export transformation data
def export_transformations(stage, output_file):
    transformations = []

    for prim in stage.Traverse():
        if prim.IsA(UsdGeom.Xform):
            xform = UsdGeom.Xformable(prim)
            transform = xform.GetLocalTransformation()
            transformations.append({
                "name": prim.GetName(),
                "transform": transform.GetMatrix().GetArray().tolist()
            })

    with open(output_file, 'w') as f:
        json.dump(transformations, f, indent=4)

# Export transformations to a JSON file
export_transformations(stage, "transforms.json")

# Shutdown Omniverse Kit
omni.kit.shutdown()
