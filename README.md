# SOL-Sort

This code was written to help the New York City based charity Songs of Love catalog 25K tracks to prepare those tracks to be uploaded to a major streaming music platform.

The code is designed to loop through an entire directory structure, sort them chronologically into folders of 20, and then prepares a CSV in each folder.

Most of the code is organized into functions that are supporting - opening and appending to a CSV, figuring out how many folders are needed, copying files, etc.  The meat and potatoes are the organize and catalog functions, which do the heavy lifting.

I stuffed this script into a standalone application using py2app so that my clients could use this script anytime they wanted.
