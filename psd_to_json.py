from psd_tools import PSDImage
import base64
from PIL import Image
from io import BytesIO
import json


def extract_layer_info(layer):
    # Esta función extrae la información relevante de una capa
    layer_info = {
        "id": str(layer.layer_id),
        "color": {},  # Puedes llenar esto según sea necesario
        "bounds": {
            "left": layer.bbox[0],  # Accede a la coordenada izquierda de la tupla
            "top": layer.bbox[1],   # Accede a la coordenada superior de la tupla
            "right": layer.bbox[2], # Accede a la coordenada derecha de la tupla
            "bottom": layer.bbox[3]  # Accede a la coordenada inferior de la tupla
        },
        "layername": layer.name,
        "name": layer.name,
        "opacity": layer.opacity,
        "size": {
            "height": layer.bbox[3] - layer.bbox[1],  # Calcula la altura usando las coordenadas superior e inferior
            "width": layer.bbox[2] - layer.bbox[0]   # Calcula el ancho usando las coordenadas izquierda y derecha
        },
        "src": "",  # Debes manejar la lógica para obtener la fuente de la capa
        "src_type": "data",  # Puedes cambiar esto según sea necesario
        "type": "normal",
        "visibility": layer.visible,
        "blendMode": str(layer.blend_mode),  # Convertir BlendMode a cadena
        "position": {
            "x": layer.bbox[0],
            "y": layer.bbox[1]
        },
        "scale": {
            "x": 1,  # Puedes ajustar esto según sea necesario
            "y": 1
        },
        "filters": {},  # Puedes llenar esto según sea necesario
        "has_mask": layer.has_mask,
        "duplicates": []  # Puedes llenar esto según sea necesario
    }

    # Obtener la fuente de la capa
    layer_image = layer.topil()
    buffered = BytesIO()
    layer_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    layer_info["src"] = f"data:image/png;base64,{img_str}"

    # Manejar información de transformación para capas de objetos inteligentes
    if layer.kind == "smartobject":
        # Verificar si la capa tiene información de transformación
        if hasattr(layer, "transform"):
            # Obtener información de transformación para capas de objetos inteligentes
            transform_info = {
                "xx": layer.transform.xx,
                "xy": layer.transform.xy,
                "yx": layer.transform.yx,
                "yy": layer.transform.yy,
                "tx": layer.transform.tx,
                "ty": layer.transform.ty
            }

            # Agregar información de transformación al diccionario layer_info
            layer_info["transform"] = transform_info

    # Resto del código...

    return layer_info


def psd_to_json(file_path):
    psd = PSDImage.open(file_path)

    # Crear una estructura básica de JSON
    psd_json = {
        "size": {
            "width": psd.width,
            "height": psd.height
        },
        "layers": []
    }

    # Recorrer cada capa del PSD y extraer información
    for layer in psd:
        layer_info = extract_layer_info(layer)
        psd_json["layers"].append(layer_info)

    return psd_json


psd_path = "./1675345981285-glass-dropper-bottle-photoshop-mockup.psd"
resultado_json = psd_to_json(psd_path)

# Imprimir el tipo de cada elemento del diccionario
for key, value in resultado_json.items():
    print(f"{key}: {type(value)}")

# Escribir el JSON en un archivo
output_file = "output.json"
with open(output_file, 'w') as json_file:
    json.dump(resultado_json, json_file, indent=2, default=str)
