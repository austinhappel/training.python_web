# Overview

I like all types music, and lately I've been enjoying using mixcloud to find new music. This little webapp searches your last.fm account to get your top artists, then searches the mixcloud.com api for mixes related to those top artists. 

You can also do an artist search, which will find mixes for that artist, and also offer up related artists using last.fm.

# installation notes

1. Get virtualenv
2. Make virtual environment

        mkdir env && virtualenv env
        
3. In env, install pip requirements

        pip install -r requirements.txt

4. Last.fm requires an api key for some reason. Set the following
environment variable up:

        export last_fm_api_key=<your api key>