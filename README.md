# ADB_Forwarder
Use your Android device's camera as webcam over USB instead of WiFi.

1. Install ADB for your system if you don't already have it.
2. Install Python 3 on your system if you don't already have it (recommended Python 3.6 to 3.8).
3. On your device, open up Developer Options (you'll have to enable this if you device is running stock, look up the method for your device.
4. Find the option called "USB Debugging" and enable it
5. Connect your device to your PC with a USB cable.
6. A popup should appear on your device asking if you trust the connection to your PC. Check the "Always allow from this computer" box and select "Allow".
7. In the IP Webcam app, configure your setup and specify a port to use (or stick with the default 8080). Also make sure to have a username and password!
8. On your PC, open the adb.json file and modify it to point to the adb executable, as well as put in the port that you specified in the IP Webcam app.
9. Open a console or powershell window and navigate to where you keep this repository.
10. Run the following command and you should see the program's output: `python adb_handler.py`.
11. If you do not see any errors, then follow the next set of steps. If you do see any errors, you didn't follow the steps above.
12. On your device, IP Webcam should list a URL at the bottom of the screen for you to access.
  * For example, if you used port `8080` then the URL might look like `http://192.168.1.24:8080`
13. Open up that URL in a browser on your PC. You'll be met with a page containaing a lot of options for controlling your phone's camera. IF you wishto preview the video, try the different "Videor renderer" options listed at the top of the page.
14. Confirm that your camera works correctly on this webpage.
14. To use your camera with OBS, create a new Browser Source and use the URL you got to connect to the IP Webcam browser page, use the followign format to access it:
  * For example, with the normal URL of `http://192.168.1.24:8080` the Browser Source URL should be `http://username:password@192.168.1.24:8080/video`.
    * Note that the username and password are used here, and they are completely visible when the Browser Source's properties are visible.

Voila, you're done!

ISSUES:
  * IP Webcam does not work in OBS as a Browser Source when using HTTPS URL's
    Use the regular HTTP version of the URL instead of HTTPS

Example JSON:
```
{
  "location": "C:\\Program Files\\something\somewhere\adb.exe",
  "port": "8080"
}
```
