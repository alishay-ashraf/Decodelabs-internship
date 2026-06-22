import ezdxf
from ezdxf.enums import TextEntityAlignment

def create_professional_plan(filename="modern_floor_plan.dxf"):
    # 1. Initialize Document & Set Standard Units to Millimeters
    doc = ezdxf.new("R2010", setup=True)
    doc.header['$INSUNITS'] = 4 # 4 = Millimeters
    msp = doc.modelspace()
    
    # 2. Strict Layer Management
    layers = [
        {"name": "WALLS", "color": 7, "lineweight": 35},       # Black/White
        {"name": "DOORS", "color": 1, "lineweight": 18},       # Red
        {"name": "WINDOWS", "color": 4, "lineweight": 18},     # Cyan
        {"name": "FIXTURES", "color": 3, "lineweight": 15},    # Green
        {"name": "DIMENSIONS", "color": 5, "lineweight": 13},  # Magenta
        {"name": "TEXT", "color": 7, "lineweight": 18}
    ]
    for layer in layers:
        if layer["name"] not in doc.layers:
            doc.layers.new(name=layer["name"], dxfattribs={"color": layer["color"], "lineweight": layer["lineweight"]})

    # Safe Dimension Style Setup
    try:
        dimstyle = doc.dimstyles.get("EZ_METRIC")
    except ezdxf.lldxf.const.DXFTableEntryError:
        dimstyle = doc.dimstyles.new("EZ_METRIC")

    dimstyle.dxf.dimtxt = 200      # Text height
    dimstyle.dxf.dimasz = 150      # Arrow/Tick size
    dimstyle.dxf.dimexe = 100      # Extension line beyond dimension line
    dimstyle.dxf.dimexo = 50       # Extension line offset from origin

    # 3. Block Management (Furniture)
    chair_block = doc.blocks.new(name="CHAIR")
    chair_block.add_lwpolyline([(0, 0), (1000, 0), (1000, 1000), (0, 1000)], close=True, dxfattribs={"layer": "FIXTURES"})
    chair_block.add_lwpolyline([(150, 150), (850, 150), (850, 850), (150, 850)], close=True, dxfattribs={"layer": "FIXTURES"})

    # 4. Drafting the Exterior Walls WITH Openings
    # Bottom Wall segments (Leaving a gap from X=2000 to X=3000 for the door)
    msp.add_lwpolyline([(0, 0), (2000, 0), (2000, 300), (300, 300), (300, 7700), (0, 8000)], close=True, dxfattribs={"layer": "WALLS"})
    msp.add_lwpolyline([(3000, 0), (10000, 0), (10000, 3000), (9700, 3000), (9700, 300), (3000, 300)], close=True, dxfattribs={"layer": "WALLS"})
    
    # Left Wall Windows & Upper Left Envelope (Leaving a gap from Y=3000 to Y=5000)
    msp.add_lwpolyline([(0, 5000), (0, 8000), (5000, 8000), (5000, 7700), (300, 7700), (300, 5000)], close=True, dxfattribs={"layer": "WALLS"})
    
    # Right Wall Windows & Upper Right Envelope (Leaving a gap from Y=3000 to Y=5000)
    msp.add_lwpolyline([(10000, 5000), (10000, 8000), (5200, 8000), (5200, 7700), (9700, 7700), (9700, 5000)], close=True, dxfattribs={"layer": "WALLS"})
    msp.add_lwpolyline([(9700, 3000), (10000, 3000), (10000, 0), (9700, 0)], close=False, dxfattribs={"layer": "WALLS"})

    # Interior Partition Wall
    msp.add_lwpolyline([(5000, 300), (5200, 300), (5200, 7700), (5000, 7700)], close=True, dxfattribs={"layer": "WALLS"})

    # 5. Placing Windows and Doors into Openings
    # Left Window Frame
    msp.add_lwpolyline([(0, 3000), (300, 3000), (300, 5000), (0, 5000)], close=True, dxfattribs={"layer": "WINDOWS"})
    msp.add_line((150, 3000), (150, 5000), dxfattribs={"layer": "WINDOWS"})
    
    # Right Window Frame
    msp.add_lwpolyline([(9700, 3000), (10000, 3000), (10000, 5000), (9700, 5000)], close=True, dxfattribs={"layer": "WINDOWS"})
    msp.add_line((9850, 3000), (9850, 5000), dxfattribs={"layer": "WINDOWS"})

    # Front Door Frame and Swing
    msp.add_line((2000, 0), (2000, 1000), dxfattribs={"layer": "DOORS"})
    msp.add_arc(center=(2000, 0), radius=1000, start_angle=0, end_angle=90, dxfattribs={"layer": "DOORS"})

    # 6. Block Placements
    msp.add_blockref("CHAIR", insert=(1200, 2000), dxfattribs={"layer": "FIXTURES"})
    msp.add_blockref("CHAIR", insert=(1200, 4200), dxfattribs={"layer": "FIXTURES"})
    

    # 7. Labels
    msp.add_text("LIVING ROOM", dxfattribs={"layer": "TEXT", "height": 300}).set_placement(
        (2500, 6000), align=TextEntityAlignment.CENTER
    )
    msp.add_text("BEDROOM", dxfattribs={"layer": "TEXT", "height": 300}).set_placement(
        (7500, 6000), align=TextEntityAlignment.CENTER
    )

    # 8. Standardized Dimensioning with Active Dimstyle
    # Top Dimension
    dim1 = msp.add_linear_dim(base=(5000, 8800), p1=(0, 8000), p2=(10000, 8000), dimstyle="EZ_METRIC", dxfattribs={"layer": "DIMENSIONS"})
    dim1.render()

    # Left Dimension
    dim2 = msp.add_linear_dim(base=(-1000, 4000), p1=(0, 0), p2=(0, 8000), angle=90, dimstyle="EZ_METRIC", dxfattribs={"layer": "DIMENSIONS"})
    dim2.render()

    doc.saveas(filename)
    print(f"Updated professional blueprint saved to '{filename}' successfully!")

if __name__ == "__main__":
    create_professional_plan()