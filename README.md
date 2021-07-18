# fileComparer
Toolset to determine duplicate files.
## listFilesAccordingToHashes
The main aim is to determine the duplicate files in the directory that the program runs. First of all, both the files '_myGui.py' (strictly necessary) and 'img.png' (optional,  only needed for the icon) are base files for both programs 'listFilesGroupedByHashes.py' and 'listOnlySameFiles'. The slight difference between them is:
- 'listFilesGroupedByHashes.py' prints all the files grouped concerning their hashes.
- 'listOnlySameFiles' prints only the duplicated files grouped with respect to their hashes.
