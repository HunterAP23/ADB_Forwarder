# ADB_Forwarder
Use your Android device's camera as webcam over USB instead of WiFi.

This will cover the steps to set up IP Webcam on your device and be able to
access it securely.

1. Install ADB for your system if you don't already have it.
2. Install Python 3 on your system if you don't already have it
(recommended Python 3.6 to 3.8).
3. On your device, open up Developer Options (you'll have to enable this if you
device is running stock, look up the method for your device).
4. Find the option called "USB Debugging" under Developer Options and enable it.
5. Connect your device to your PC with a USB cable.
6. A popup should appear on your device asking if you trust the connection to
your PC. Check the "Always allow from this computer" box and select "Allow".
  - If the prompt does not appear, locate the ADB executable and open a console
  or powershell window in that location, then type `adb devices`.
  This should bring up the prompt and list the devices the ADB program can see.
7. In the IP Webcam app, configure your setup and specify a port to use (or
  stick with the default 8080).
8. Set up a username and password in the IP Webcam app, under the
"Local broadcasting" section.
9. On your PC, open the adb.json file and modify it to point to the adb
executable, as well as put in the port that you specified in the IP Webcam app.
  * Example JSON:
  ```
  {
    "location": "C:\\Program Files\\something\somewhere\adb.exe",
    "port": "8080"
  }
  ```
10. Open a console or powershell window and navigate to where you keep this
repository.
11. Run the following command and you should see the program's output:
`python adb_handler.py`.
12. If you do not see any errors, then follow the next set of steps.
If you do see any errors, you didn't follow the steps above correctly.
13. On your device, IP Webcam should list a URL at the bottom of the screen for
you to access.
 - For example, if you used port `8080` then the URL might look like
 `http://192.168.1.24:8080`
14. Open up that URL in a browser on your PC. It will ask for the username and
password you set previously, and you'll be met with a page containing a lot of
options for controlling your phone's camera.
 - If you wish to preview the video, select from the different "Video renderer"
 options listed at the top of the page. "Browser" usually works for me.
15. Confirm that your camera works correctly on this webpage.
16. To use your camera with OBS, create a new Browser Source and use the URL
you got to connect to the IP Webcam browser page, use the following format to
access it:
  - For example, with the normal URL of `http://192.168.1.24:8080` the Browser
  Source URL should be `http://username:password@192.168.1.24:8080/video`.
    - Note that the username and password are used here, and they are completely
    visible when the Browser Source's properties are visible.

Voila, you're done!

ISSUES:
  * IP Webcam does not work in OBS as a Browser Source when using HTTPS URL's.
    * __SOLUTION:__ Use the regular HTTP version of the URL instead of HTTPS.
