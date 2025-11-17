import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime


class CVATWriter:
    """
    Basic CVAT writer for frame-by-frame annotations.
    Produces:
    - <annotations>
        - <image id="0" name="frame_0000">
            - <box ... />
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = ET.Element("annotations")

    def add_frame(self, frame_id, boxes):
        img = ET.SubElement(self.root, "image")
        img.set("id", str(frame_id))
        img.set("name", f"frame_{frame_id:05d}.jpg")
        img.set("width", str(self.width))
        img.set("height", str(self.height))

        for b in boxes:
            box = ET.SubElement(img, "box")
            box.set("label", b["label"])
            box.set("occluded", "0")
            box.set("xtl", str(b["xtl"]))
            box.set("ytl", str(b["ytl"]))
            box.set("xbr", str(b["xbr"]))
            box.set("ybr", str(b["ybr"]))
            box.set("confidence", str(b["confidence"]))

    def save(self, path):
        xml_bytes = ET.tostring(self.root)
        pretty = minidom.parseString(xml_bytes).toprettyxml(indent="  ")
        with open(path, "w", encoding="utf-8") as f:
            f.write(pretty)
