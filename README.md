# FileyFace
[fileyface.co](fileyface.co) -- HackGT 11

File Manager that automatically sorts file downloads. One click away from organisation. 

**Set-Up**
1. Clone the repository
2. Download all requirements ``` pip install <requirements> ```
3. Set API key for OpenAI and TextRazor (if needed)
4. Run in background
5. Download .pdf, .docx, .pptx, and .txt files as needed!
   
   --> files will be automatically sorted

# How FileyFace Works
**File Analysis**
1. Immediately upon file download, file name and extension are read
2. Web address of download (e.g. "canvas.com" for an assignment download) are read from Chrome history
3. File is parsed and summarised depending on doc type

   --> OpenAI API assists in general file summarisation

   --> RazorText API assists in keyword location based on weights (entity, phrase, word, topic)
5. User is able to change file name within GUI; if name is changed, then file name is re-read

**Decision Making**
1. Data is collected and compiled from file analysis

   --> including summary, key words, file name, file extension, web address
3. Directory tree is loaded and saved from computer
4. Based on folder names and file analysis data, prompt OpenAI API
5. Inputs are weighted and "best folder destination" is outputted to user

   --> new folder is created with os functionality if necessary
7. If user is unsatisfied, "Regenerate" button can be used to re-evaluate inputs for a potentially more accurate folder destination output

   --> if user changes the name of a file within the GUI, a "Regenerate" button press is recommended

   --> "Regenerate" can be pressed as frequently as necessary

**File Placement**
1. Saved directory tree is parsed
2. File is unzipped from package (if necessary)
3. Python os package is used to move file from src to destination
4. If file already exists at that location, copy with "(1)" appended is made

# Demo
--video here--
