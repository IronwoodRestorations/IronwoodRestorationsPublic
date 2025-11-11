import json
import os
import sys
import time
import datetime
import re

PDFEnabled = True

# Try to import Reportlab
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
except Exception as e:
    PDFEnabled = False
    print(f"Failed to import Report Lab due to: {e}")
    print("Print to PDF will be disabled, if you wish to use print to PDF please run install.py")

# JSON storage
JSON_FILE = "custom_dtcs.json"

authorOS = os.getlogin()

# Repo Information
repo_link = "https://github.com/IronwoodRestorations/IronwoodRestorationsPublic/tree/main/CustomDTCGenerator"
youtube_link = "https://www.youtube.com/@IronwoodRestorations"

HEADERS = {
    "P": "Powertrain",
    "B": "Body",
    "C": "Chassis",
    "U": "Network"
}

# Categories (editable)
CATEGORIES = {
    "x40xx": "Communication Systems",
    "x41xx": "Sensor Networks",
    "x42xx": "Body Control Modules",
    "x43xx": "Power Distribution",
    "x44xx": "Hybrid/EV Systems",
    "x45xx": "Safety & Chassis Systems",
    "x46xx": "Custom Computer Nodes",
    "x47xx": "Miscellaneous Custom Functions"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_dtcs():
    #Load DTC data from JSON file.
    print("Loading DTC(s) from custom_dtcs.json")
    time.sleep(1)
    if not os.path.exists(JSON_FILE):
        print("Loaded DTC(s) sucessfully")
        time.sleep(1)
        return []
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def save_dtcs(data):
    #Save DTC data to JSON file.
    print("Saving DTC(s) to custom_dtcs.json")
    time.sleep(1)
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def create_dtc():
    # Interactive DTC creation
    clear_screen()
    print("=== Create New DTC ===\n")

    # --- Step 1: Select the header ---
    print("Select a header type:")
    for i, (header, desc) in enumerate(HEADERS.items(), 1):
        print(f"{i}. {header} – {desc}")

    while True:
        try:
            header_choice = int(input("\nEnter header number: "))
            if 1 <= header_choice <= len(HEADERS):
                header = list(HEADERS.keys())[header_choice - 1]
                header_desc = HEADERS[header]
                break
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    # --- Step 2: Select category ---
    clear_screen()
    print(f"=== {header} - {header_desc} ===\nSelect a category:")
    for i, (prefix, desc) in enumerate(CATEGORIES.items(), 1):
        print(f"{i}. {prefix} – {desc}")

    while True:
        try:
            category_choice = int(input("\nEnter category number: "))
            if 1 <= category_choice <= len(CATEGORIES):
                prefix = list(CATEGORIES.keys())[category_choice - 1]
                category_desc = CATEGORIES[prefix]
                break
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    # --- Step 3: Build the code ---
    # Header + 4 (custom) + prefix digits
    code_number = input(f"Enter 2-digit code for {prefix} (e.g., 01 for {prefix[:3]}01): ").zfill(2)
    full_code = f"{header}4{prefix[:2]}{code_number}"  # Example: U4A01

    # --- Step 4: Collect details ---
    clear_screen()
    print(f"Creating DTC {full_code} ({category_desc})\n")

    title = input("Enter DTC title: ")
    description = input("Enter DTC description: ")

    print("\nEnter possible fixes (blank line to finish):")
    fixes = []
    while True:
        fix = input(" - ")
        if not fix.strip():
            break
        fixes.append(fix)

    pinpoint = input("\nEnter pinpoint test code (e.g., PP-001): ")

    # --- Step 5: Save ---
    new_dtc = {
        "code": full_code,
        "header": header_desc,
        "category": category_desc,
        "title": title,
        "description": description,
        "possible_fixes": fixes,
        "pinpoint_test": pinpoint
    }

    dtcs = load_dtcs()
    dtcs.append(new_dtc)
    save_dtcs(dtcs)

    print(f"\n✅ DTC {full_code} saved successfully!\n")
    input("Press Enter to return to the menu...")

def select_dtc_paginated(dtcs, page_size=25):
    page = 0
    total_pages = (len(dtcs) - 1) // page_size + 1

    while True:
        clear_screen()
        start = page * page_size
        end = min(start + page_size, len(dtcs))
        print(f"=== Edit Existing DTC (Page {page + 1}/{total_pages}) ===\n")

        for i, dtc in enumerate(dtcs[start:end], start=1):
            print(f"{i}. {dtc.get('code')} - {dtc.get('title', 'Untitled')}")

        nav_options = []
        if page > 0:
            nav_options.append("P = Previous page")
        if page < total_pages - 1:
            nav_options.append("N = Next page")
        nav_options.append("C = Cancel")
        print("\n" + "   ".join(nav_options))

        choice = input("\nSelect DTC by number: ").strip().upper()
        if choice == "C":
            return None
        elif choice == "N" and page < total_pages - 1:
            page += 1
        elif choice == "P" and page > 0:
            page -= 1
        else:
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= (end - start):
                    return dtcs[start + choice_num - 1]
                else:
                    print("Invalid selection. Try again.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Try again.")
                input("Press Enter to continue...")


def edit_dtc(page_size=25):
    dtcs = load_dtcs()
    if not dtcs:
        clear_screen()
        print("No DTCs found. Load or create some first.\n")
        input("Press Enter to return...")
        return

    # --- Paginated DTC Selection ---
    page = 0
    total_pages = (len(dtcs) - 1) // page_size + 1

    while True:
        clear_screen()
        start = page * page_size
        end = min(start + page_size, len(dtcs))
        print(f"=== Edit Existing DTC (Page {page + 1}/{total_pages}) ===\n")

        for i, dtc in enumerate(dtcs[start:end], start=1):
            print(f"{i}. {dtc.get('code')} - {dtc.get('title', 'Untitled')}")

        # Navigation options
        nav_options = []
        if page > 0:
            nav_options.append("P = Previous page")
        if page < total_pages - 1:
            nav_options.append("N = Next page")
        nav_options.append("C = Cancel")
        print("\n" + "   ".join(nav_options))

        choice = input("\nSelect DTC by number: ").strip().upper()
        if choice == "C":
            print("Edit cancelled.\n")
            return
        elif choice == "N" and page < total_pages - 1:
            page += 1
            continue
        elif choice == "P" and page > 0:
            page -= 1
            continue
        else:
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= (end - start):
                    dtc = dtcs[start + choice_num - 1]
                    break  # Selected DTC found, exit loop
                else:
                    print("Invalid selection. Try again.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Try again.")
                input("Press Enter to continue...")

    # --- Start editing selected DTC ---
    clear_screen()
    print(f"Editing {dtc['code']} - {dtc['title']}\n")

    # --- Edit header ---
    print("Select new header (leave blank to keep current, 'C' to cancel):")
    for i, (header, desc) in enumerate(HEADERS.items(), 1):
        print(f"{i}. {header} – {desc}")
    header_input = input(f"Current: {dtc.get('header', '')} > ").strip()
    if header_input.upper() == "C":
        print("Edit cancelled.\n")
        return
    if header_input.isdigit() and 1 <= int(header_input) <= len(HEADERS):
        dtc['header'] = list(HEADERS.values())[int(header_input) - 1]
        header_key = list(HEADERS.keys())[int(header_input) - 1]
    else:
        header_key = next((k for k, v in HEADERS.items() if v == dtc.get('header')), "U")

    # --- Edit category ---
    print("\nSelect new category (leave blank to keep current, 'C' to cancel):")
    for i, (code, desc) in enumerate(CATEGORIES.items(), 1):
        print(f"{i}. {code} – {desc}")
    category_input = input(f"Current: {dtc.get('category', '')} > ").strip()
    if category_input.upper() == "C":
        print("Edit cancelled.\n")
        return
    if category_input.isdigit() and 1 <= int(category_input) <= len(CATEGORIES):
        cat_key = list(CATEGORIES.keys())[int(category_input) - 1]
        dtc['category'] = CATEGORIES[cat_key]
    else:
        cat_key = next((k for k, v in CATEGORIES.items() if v == dtc.get('category')), "x40xx")

    # --- Edit code ---
    code_number = input(f"\nEnter 2-digit code for this DTC (Current: {dtc.get('code', '')[-2:]}, 'C' to cancel) > ").strip()
    if code_number.upper() == "C":
        print("Edit cancelled.\n")
        return
    code_number = code_number.zfill(2) if code_number else dtc.get('code', '')[-2:]
    full_code = f"{header_key}4{cat_key[2]}{code_number}"
    dtc['code'] = full_code

    # --- Edit other fields ---
    title = input(f"\nTitle [{dtc['title']}] (C to cancel): ").strip()
    if title.upper() == "C":
        print("Edit cancelled.\n")
        return
    if title:
        dtc['title'] = title

    description = input(f"Description [{dtc['description']}] (C to cancel): ").strip()
    if description.upper() == "C":
        print("Edit cancelled.\n")
        return
    if description:
        dtc['description'] = description

    pinpoint = input(f"Pinpoint Test [{dtc.get('pinpoint_test', '')}] (C to cancel): ").strip()
    if pinpoint.upper() == "C":
        print("Edit cancelled.\n")
        return
    if pinpoint:
        dtc['pinpoint_test'] = pinpoint

    # --- Edit possible fixes ---
    print("\nPossible Fixes:")
    for i, fix in enumerate(dtc['possible_fixes'], 1):
        print(f" {i}. {fix}")

    print("\n[A] Add Fix   [R] Remove Fix   [Enter] Skip   [C] Cancel")
    fix_action = input("Select action: ").strip().upper()
    if fix_action == "C":
        print("Edit cancelled.\n")
        return

    if fix_action == "A":
        while True:
            new_fix = input(" - New fix (blank to stop, 'C' to cancel): ").strip()
            if new_fix.upper() == "C":
                print("Edit cancelled.\n")
                return
            if not new_fix:
                break
            dtc['possible_fixes'].append(new_fix)

    elif fix_action == "R":
        while True:
            remove_index = input("Enter fix number to remove (blank to stop, 'C' to cancel): ").strip()
            if remove_index.upper() == "C":
                print("Edit cancelled.\n")
                return
            if not remove_index:
                break
            try:
                remove_index = int(remove_index)
                if 1 <= remove_index <= len(dtc['possible_fixes']):
                    removed = dtc['possible_fixes'].pop(remove_index - 1)
                    print(f"Removed: {removed}")
                else:
                    print("Invalid fix number.")
            except ValueError:
                print("Invalid input.")

    # --- Save changes ---
    save_dtcs(dtcs)
    print(f"\nDTC {full_code} updated successfully!\n")
    input("Press Enter to return...")

def print_to_pdf():
    clear_screen()
    
    if not PDFEnabled:
        print("Error 0x001A: PDF functionality is not enabled.")
        quit()

    dtcs = load_dtcs()
    if not dtcs:
        print("No DTCs found. Please create or load DTCs first.")
        input("Press Enter to return...")
        return

    # --- Project/Application Name ---
    project_name = input("Enter Project/Application Name: ").strip() or "Unnamed Project"
    project_name_file = re.sub(r'[^a-zA-Z0-9_-]', '_', project_name)
    project_name_display = project_name  # readable

    # --- Sort DTCs by header then numeric code ---
    header_order = ["B", "C", "P", "U"]
    dtcs.sort(key=lambda d: (
        header_order.index(d["code"][0]) if d["code"][0] in header_order else 99,
        int(d["code"][1:]) if d["code"][1:].isdigit() else 99999
    ))

    # --- Ask user for color mode ---
    print("\nSelect PDF color mode:")
    print("1. Black & White (default)")
    print("2. Colorless (only borders)")
    print("3. Color version (green highlights)")
    color_choice = input("Choice [1]: ").strip() or "1"

    pdf_file = f"custom_dtcs_{project_name_file}.pdf"

    # --- Links ---
    repo_full = repo_link
    youtube_full = youtube_link
    youtube_display = youtube_full.replace("https://www.", "").replace("https://", "").replace("youtube.com/", "")

    # --- Footer ---
    def footer(canvas, doc):
        canvas.saveState()
        text_color = colors.green if color_choice=="3" else colors.black
        style = ParagraphStyle("footer_style", fontSize=8, textColor=text_color)
        footer_text = (
            f"<b>{project_name_display}</b> | "
            f"Created with Custom DTC Builder from Ironwood Restorations<br/>"
            f"Page {canvas.getPageNumber()} | "
            f"<a href='{repo_full}'>Github: @IronwoodRestorations</a> | "
            f"<a href='{youtube_full}'>Youtube/TikTok: {youtube_display}</a>"
        )
        p = Paragraph(footer_text, style)
        w, h = p.wrap(doc.width, doc.bottomMargin)
        p.drawOn(canvas, doc.leftMargin, 20)
        canvas.restoreState()

    # --- Document Setup ---
    creation_date = datetime.datetime.now()
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
        title=f"Custom DTC's: {project_name_display}",
        author=authorOS,
        creator="Custom DTC Builder Script",
        creationDate=creation_date,
        modDate=creation_date,
        subject=f"Custom DTC list for {project_name_display}",
        keywords=f"DTC, Custom, IronwoodRestorations, Repo: {repo_full}, YouTube: {youtube_full}"
    )

    styles = getSampleStyleSheet()
    elements = []

    # --- Main Title ---
    elements.append(Paragraph(f"<b>Custom DTC's: {project_name_display}</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # --- DTC Headers | Trouble Code Categories in two columns ---
    headers_para = "<br/>".join([f"{k} – {v}" for k,v in HEADERS.items()])
    categories_para = "<br/>".join([f"{k} – {v}" for k,v in CATEGORIES.items()])

    table_data = [
        [
            Paragraph("<b>Custom DTC Headers</b><br/>" + headers_para, styles["Normal"]),
            Paragraph("<b>Trouble Code Categories</b><br/>" + categories_para, styles["Normal"])
        ]
    ]
    table = Table(table_data, colWidths=[doc.width/2.0]*2)
    table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 18))

    # --- Combined DTC Table ---
    elements.append(Paragraph("<b>Custom DTC's</b>", styles["Heading2"]))
    table_data = [["Code", "Category", "Title", "Description", "Possible Fixes", "Pinpoint Test"]]
    for dtc in dtcs:
        fixes_str = "<br/>• " + "<br/>• ".join(dtc["possible_fixes"]) if dtc["possible_fixes"] else "-"
        table_data.append([
            Paragraph(dtc["code"], styles["Normal"]),
            Paragraph(dtc["category"], styles["Normal"]),
            Paragraph(dtc["title"], styles["Normal"]),
            Paragraph(dtc["description"], styles["Normal"]),
            Paragraph(fixes_str, styles["Normal"]),
            Paragraph(dtc["pinpoint_test"], styles["Normal"]),
        ])

    col_widths = [55, 95, 95, 130, 130, 65]
    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    # --- Table Styling ---
    if color_choice=="1":  # B&W
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
        ]))
    elif color_choice=="2":  # Borders only
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
    elif color_choice=="3":  # Green highlights
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.green),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.darkgreen),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
        ]))

    elements.append(table)

    # --- Build PDF ---
    doc.build(elements, onFirstPage=footer, onLaterPages=footer)

    print(f"\nPDF generated successfully: {pdf_file}\n")
    print("Exiting after PDF generation.\n")
    sys.exit(0)

def dtcMenu():
    while True:
        clear_screen()
        print("\n=== DTC Menu ===")
        print("1. Create new DTC")
        print("2. Edit DTCs")
        print("3. Reload DTCs")
        print("4. Return to Main Menu")
        
        choice = input("Select option: ").strip()
        if choice == "1":
            create_dtc()
        elif choice == "2":
            edit_dtc()
        elif choice == "3":
            print("Reloading DTC's")
            time.sleep(1)
            load_dtcs()
        elif choice == "4":
            break  # return to main menu
        else:
            print("Invalid choice. Try again.\n")

    
def main():
    while True:
        clear_screen()
        print("=== Custom DTC Builder ===")
        print("1. DTC Menu")
        if PDFEnabled:
            print("2. Print to PDF")
            print("3. Exit")
        else:
            print("2. Exit")

        choice = input("Select option: ").strip()
        if choice == "1":
            dtcMenu()
        elif choice == "2":
            if PDFEnabled:
                print_to_pdf()
            else:
                break
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
