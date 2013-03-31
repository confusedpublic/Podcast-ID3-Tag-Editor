First scripts that edit podcast ID3 tags, specifically those of In Our Time archive podcasts.

There are four python files, one for each archive, though the only changes are variables commented out.

There are also four text files, which contain the information for the podcasts. This is copied from the source code of the In Our Time archive websites: http://www.bbc.co.uk/programmes/b006qykl/features/downloads.

Each script requires a base path to be entered where the .mp3s are stored. It requires the .mp3s to have been added to iTunes, so that they have a name with the following convention: IOT[A]: [Title], where [A] is the abbreviation of the archive (e.g. S for the science episodes), and Title is the title of the podcast. A future update will allow the original filenames to be used, those taken from the BBC website. A later update will read the podcast folder for the file names, and match them to the info from the websites automatically.

Problem: The scripts DO NOT work if there is a "é" character in the filename. I have not found an adequate way to fix this problem yet.

Once the variable has been set, run the script. Information added to the mp3s will be printed to the console, and so will warnings if the file was not found.