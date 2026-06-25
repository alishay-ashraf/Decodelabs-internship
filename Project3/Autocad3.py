import csv
import ezdxf

def extract_furniture_bom(dxf_file_path, output_csv_path):
    try:
        # Load the DXF drawing
        doc = ezdxf.readfile(dxf_file_path)
        msp = doc.modelspace()
        
        # Dictionary to store furniture counts and attributes
        # Structure: {(BlockName, Attribute_Values): Count}
        bom_data = {}
        
        print(f"Analyzing {dxf_file_path} for furniture attributes...")

        # Iterate through all block references (INSERT entities) in model space
        for entity in msp.query("INSERT"):
            block_name = entity.d.name
            
            # Initialize empty attribute tracking for this specific instance
            attributes = {
                "Item Name": "Unknown",
                "Manufacturer": "N/A",
                "Cost": "0.00"
            }
            
            # Check if the block has attached attributes (attribs)
            if entity.has_attribs:
                for attrib in entity.attribs:
                    tag = attrib.d.tag.upper()
                    text = attrib.d.text
                    
                    # Map standard corporate furniture attributes
                    if "NAME" in tag or "ITEM" in tag:
                        attributes["Item Name"] = text
                    elif "MANU" in tag or "VENDOR" in tag:
                        attributes["Manufacturer"] = text
                    elif "COST" in tag or "PRICE" in tag:
                        attributes["Cost"] = text
            
            # Create a unique key based on block name and its attributes
            item_key = (block_name, attributes["Item Name"], attributes["Manufacturer"], attributes["Cost"])
            
            # Increment the item count in our inventory database
            bom_data[item_key] = bom_data.get(item_key, 0) + 1

        # Write collected data into a structured CSV file
        with open(output_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            
            # Write Header Row
            writer.writerow(["Block Name", "Item Description", "Manufacturer", "Unit Cost", "Quantity"])
            
            # Write Data Rows
            for (b_name, item, manu, cost), qty in bom_data.items():
                writer.writerow([b_name, item, manu, cost, qty])
                
        print(f"Success! Automated BOM generated and saved to: {output_csv_path}")

    except IOError:
        print(f"Error: Cannot open or find file {dxf_file_path}")
    except ezdxf.DXFError as e:
        print(f"DXF Parsing Error: {e}")

# --- EXECUTION ---
# Ensure your AutoCAD file is saved as a AutoCAD DXF format before running
# --- EXECUTION ---
# Change this to match your exact filename!
dxf_input = "your_actual_file_name.dxf" 
csv_output = "Corporate_Office_BOM.csv"

extract_furniture_bom(dxf_input, csv_output)