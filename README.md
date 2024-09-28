# FileyFace
HackGT11 -- File Manager that automatically sorts file downloads. One click away from organisation.
[fileyface.co](fileyface.co)

**Set-Up**
1. Clone the repository
2. Download all requirements ``` pip install <requirements> ```
3. Set API key for OpenAI and TextRazor (if needed)
4. Run in background
5. Download .pdf, .docx, .pptx, and .txt files as needed!
   --> files will be automatically sorted

# How FileyFace Works
**File Analysis**
1. Files are extracted (if necessary)
2. File name and extension are extracted
3. Web address of download (e.g. "canvas.com" for an assignment download) is stored
4. File is parsed and summarised depending on doc type
   --> OpenAI API and RazorText API assist in file summarisation
5. OpenAI generates final prediction score for each folder, or if any should be created

**Decision Making**
1. Data is collected and compiled from file analysis
   --> including summary, key words, file name, file extension, web address
2. Directory tree is loaded and saved from computer
3. Based on folder names and file analysis data, prompt OpenAI API
4. Inputs are weighted and "best folder destination" is outputted to user

**File Placement**
1. Saved directory tree is parsed
2. Python os package is used to move file from src to destination
3. If file already exists at that location, copy with "(1)" appended is made
4. 

# Demo
--video here--
