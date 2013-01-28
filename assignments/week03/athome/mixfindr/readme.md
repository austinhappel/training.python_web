# installation notes

1. Get virtualenv
2. Make virtual environment

        mkdir env && virtualenv env
3. In env, install pip requirements

        pip install -r requirements.txt

4. Last.fm requires an api key for some reason. Set the following
environment variable up:

        export last_fm_api_key=<your api key>