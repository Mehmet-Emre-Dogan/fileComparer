# fileComparer
Toolset to determine duplicate files.
## listFilesAccordingToHashes
The main aim is to determine the duplicate files in the directory that the program runs. First of all, both the files '_myGui.py' (strictly necessary) and 'img.png' (optional,  only needed for the icon) are base files for both programs 'listFilesGroupedByHashes.py' and 'listOnlySameFiles'. The slight difference between them is:
- 'listFilesGroupedByHashes.py' prints all the files grouped concerning their hashes.
- 'listOnlySameFiles' prints only the duplicated files grouped with respect to their hashes.
The file 'img.ico' can be used while compiling the codes.
## Executables
Find the executable versions of these codes.
### Clarification about .exe files

Microsoft Defender may say that file is malicious. You may read this topic explaining why that happens: https://stackoverflow.com/questions/65554464/why-is-my-pyinstaller-exe-file-marked-as-a-virus Moreover, you do not have to use the .exe file. Always you can compile your executable file from the source code (.py file) or run the .py file directly (if you have installed python interpreter and necessary libraries).
