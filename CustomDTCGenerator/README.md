# Custom DTC Generator

>This is a work in progess. The features will include planned features and this message will be deleted when complete

The Custom DTC Generator is a tool designed to help you create, organize, and export your own Diagnostic Trouble Codes (DTCs) for vehicles or custom ECUs.  
With this tool, you can design custom DTCs, assign them to specific conditions and generate a table that can be printed to PDF for reference or integration with diagnostic software.

This project is part of the [Ironwood Restorations](https://youtube.com/@IronwoodRestorations) open-source repository of automotive projects and tools.

## Features

- Create custom DTCs with unique codes and descriptions  (Currently only U4xxx)
- Organize DTCs into categories for easy reference  (U40-7xxx)
- Export tables to PDF for sharing or documentation  
- Open-source and editable, modify the code to suit your own ECU or data system  
- Lightweight & standalone, no heavy dependencies required 
- Edit Custom DTC's (Planned)

## Usage
1. Download customdtc.zip and extract, then navigate to the main folder
2. Run the install script:
    ```bash
    python install.py
    ```
3. Run the main script:
    ```bash
    python custom_dtc_generator.py
    ```
4. Follow the prompts to:
    - Add new DTCs
    - Edit existing DTCs
    - Assign categories or conditions
    - Export your table to PDF when finished.

## Contributing
- Suggest new features or improvements via pull requests
- Report bugs or issues in GitHub Issues
- Share your own custom DTC tables

## Support
If you find this tool useful, consider starring the repo or sharing your custom DTC builds, your support helps me keep making new open-source automotive projects!
