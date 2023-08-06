launchpad.py
============

A [Novation Launchpad][1] control suite for [Python][2].

If you ever dreamed of using your Launchpad for completely other stuff than music: Welcome !-)

Compatible with most [tm] single board computers.

Watch a 6s video [here][7].  
Or take a look at [that one][8].  
What about the brand new Launchpad Pro support? [Right][9]!

Hey - and the Mac? Yep, that finally works too. [Look][12] \o/  

Older Launchpads might be documented [here][10].


---
## STATUS 2017/04/09:

What's hot, what's not?  

### Devices

    Launchpad Mk1   - class "Launchpad()"     all features, LEDs and buttons
    Launchpad/S     - class "Launchpad()"     all features, LEDs and buttons
    Launchpad Mini  - class "Launchpad()"     all features, LEDs and buttons

    Launchpad Mk2   - class "LaunchpadMk2()"  all features, LEDs and buttons

    Launchpad Pro   - class "LaunchpadPro()"  all features, LEDs and buttons

### OS

+++ BREAKING +++  
+++ FIXED THOSE SYSEX "OS ISSUES" (which was actually - well, me :-)

Now full functionality with Windows 10 and macOS.

---
## NEWS

### CHANGES 2017/04/09:

    - Windows 10 and macOS SysEx issues are fixed \o\ \o/ /o/

### CHANGES 2017/01/XX:

    - launchpad.py is now available as an [optionally] installable package;
    - fixed unintentional installs under Python 3 dist-packages
    - added ButtonFlush() method to empty the button buffer
    - added Pro LedAllOn() and Mk2 Reset()
    - added macOS notes
    - some minor tweaks for the Mk2

### CHANGES 2016/12/XX:

    - added "fireworks demo" note (device not recognized)
    - reworked string scrolling for Mk1 and Mk2 Launchpads:
      - characters now adjacent
      - no artifacts left on screen (right to left scrolling)
      - scrolling from left to right still has some issues ("quick hack drawback" :)
    - implemented same scrolling behaviour for the Pro Launchpad
    - Mk2 LedCtrlXY() now does nothing if x/y are out of range (were clamped to 0 or 8 before)
    - Mk2 LedCtrlXYByCode() now also exits if x/y values are out of range
    - added LedCtrlXYByRGB() for Mk2/Pro; pass color arguments as list [r,g,b]
    - tried to clarify "Mk1" color and x/y origin mode for Pro pads in the doc
    - added ButtonStateXY() for Mk2 and Pro
    - device name search patterns now are case insensitive

### CHANGES 2016/11/XX:

    - added notes about how to use it on macOS

### CHANGES 2016/01/XX:

    - Support for Launchpad Pro now built in (only a few functions, so far).
      Please notice the new class for the Pro:
        lp_pro = LaunchpadPro()
      Except for a few, low level functions (e.g. "LedCtrlRaw()"), this and
      probably all future classes will remain compatible to the good, old
      "Classic" Launchpad (Mk1).
    - added method Check(); Checks whether a device is attached.
    - added demo code for Pro (including automatic device recognition)
    - added Pro RGB LED control
    - added Pro X/Y LED control for RGB and color code mode
    - added Pro character display incl. left/right shift
    - added Pro string scrolling
    - Support for Launchpad Mk2 now built in
      Please notice the new class for the Mk2:
        lp_pro = LaunchpadMk2()
    - classes for "Pro" and "Mk2" now with default names for Open() and Check();
    - "Pro" now automatically put in "Ableton Live mode" after opening it.
      No need to push "Setup - Live" button anymore.
    - added Mk2 LedCtrlRawByCode() and LedCtrlXYByCode()
    - added Pro ButtonStateRaw(); first *damn fast* button reads \o/


### CHANGES 2016/01/10:

    - The current version does not work with Mac OS X.
      Regarding that, as well as the fact that PyGame somehow reached its
      end of life, I am currently looking for other Midi libraries or implementations.
    - I bought a Launchpad Pro. Time to implement this, although I am not sure
      what will come first, building a new Midi system or implementing the Pro.

### CHANGES 2015/02/21:

    - Support for multiple Launchpads now finally built in. Use 'em all:
        lp1 = launchpad.Launchpad()
        lp2 = launchpad.Launchpad()
        lp1.Open(0)
        lp2.Open(1)

### CHANGES 2015/02/18:
  
    - Added option to select a Launchpad if more than one is attached.
      Also supports search for a device string, e.g. "Mini".
    - Added optional parameters <number> and <name> to Open()


---
## Upcoming attractions, notes and thoughts

  More and more reported issues are directly related to PyGame.  
  As nice as it was, it has reached its end, so I am looking for a
  more (platform) compatible lib (that actually works), but only after
  the rest got built in...

  - "Pro": remove the "Mk1" compatibility from the "Pro" functions (blue LEDs and intensity values)
  - "Pro": flash LEDs
  - "Pro": pulse LEDs
  - "All": [r,g,b] lists for colors, instead of single args (might affect compatibility)
  - "Pro": implement native text scrolling
  - "Pro": support full analog reads (button already pressed, but intensity changes)
  - "All": build in the new (*censored yet*) MIDI lib
  - "Doc": split installation and usage (and condense that a little)
  - "Doc": add git clone instructions
  - "All": fix manual text scrolling
  - "All": replace MIDI cmd numbers with sth human readable (144->Note On; 176->Control Change, etc...)
  - "All": custom bitmaps and graphics
  - "All": event system
  - "All": better custom font support
  - "All": [r,g,b] lists for colors, instead of single args (might affect compatibility)
  - "All": upload to PyPI
  - ...


---
## Installation/Usage

### Install as Python package

#### Via pip

t.b.d...

#### From local file system

If you downloaded the Launchpad.py source package, simply execute the command

      python setup.py install

from the base directory or 

      sudo python setup.py install

if superuser access is required.

Load and use the module with

      import launchpad_py
      ...
      ...
      # Mk1 Launchpad:
      lp = launchpad_py.Launchpad()
      # Mk2 Launchpad:
      lp = launchpad_py.LaunchpadMk2()
      # Pro Launchpad:
      lp = launchpad_py.LaunchpadPro()

or if you dislike typing that much, use

      import launchpad_py as lppy
      ...
      ...
      lp = lppy.Launchpad()
      lp = lppy.LaunchpadMk2()
      lp = lppy.LaunchpadPro()

For compatibility with existing code, use

      import launchpad_py as launchpad

#### Install directly from Github

Instead of downloading the source distribution, you can directly install it from Github
by executing

      pip2 install git+https://github.com/FMMT666/launchpad.py


### Direct usage

If you don't want to or cannot install the package on your system, simply
copy the two files

      launchpad.py
      charset.py

to your working directory.  
Use those files as described above, but without the "_py":

      import launchpad
      ...
      ...
      # Mk1 Launchpad:
      lp = launchpad.Launchpad()
      ...

or

      import launchpad as LP
      ...
      ...
      lp = LP.Launchpad()
      ...

### Universal loading template code

      import sys
      
      try:
        import launchpad_py as launchpad
      except ImportError:
        try:
          import launchpad
        except ImportError:
          sys.exit("error loading lauchpad.py")

Also see example folder for more code...

---
## License

[CC BY 4.0, Attribution 4.0 International][11]

You are free to:

Share — copy and redistribute the material in any medium or format  
Adapt — remix, transform, and build upon the material for any purpose, even commercially.
  
The licensor cannot revoke these freedoms as long as you follow the license terms.


---
## Requirements

  - [Python][2] 2
  - [Pygame][3] v1.9.1, (v1.9.2), v1.9.3

Some Pygame versions do not work on some OSes (e.g. v1.9.2 might cause trouble
with Windows 7/10). I cannot tell you any more than just "try them!".  
The latest fixes (4/2017) were tested with v1.9.3 (via pip from Python 2.7.13)
and Windows 10 (x64). That seems to work fine again...
  
It does not work with Python 3.  

Launchpad.py was tested under

  - Linux, 32 bit, 64 bit
  - Windows XP, 32 bit
  - Windows 7, 32 bit, 64 bit
  - Windows 10, 64 bit
  - macOS Sierra
  - [Raspberry-Pi 1/2][4] (Look out for my [Minecraft][5] controller here: [www.askrprojects.net][6])
  - Beagle Bone (Black)
  - Banana Pi (Pro/M2/R1)
  - pcDuino V3
  - ...

Supported and tested red/green LED Launchpad devices, here referred  to as "Classic" or "Mk1":

  - Launchpad (the original, old "Mk1")
  - Launchpad S
  - Launchpad Mini (Mk1)

Supported and tested full RGB Launchpad devices:
  
  - Launchpad Pro
  - Launchpad Mk2

Notice that Novation now (1/2016) sells an RGB Launchpad under the same
name it once shipped the first red/green LED with!


---
## Notes (from the source)

### For Launchpad Mk1 users (the original "Classic" Launchpad):

      USE CLASS "Launchpad":
      
        lp = launchpad.Launchpad()

### For Launchpad Pro users

      USE CLASS "LaunchpadPro":
      
        lp = launchpad.LaunchpadPro()
        
      As of 2016/01/24, the "Pro" is now automatically set to "Ableton Live mode",
      which is required for launchpad.py to work.

### For Launchpad Mk2 users

      USE CLASS "LaunchpadMk2":
      
        lp = launchpad.LaunchpadMk2()

### For Mac users

#### Mac Python and Pygame

Good news, everybody. It now works with macOS Sierra \o/  
Best part: It even works with the stock "Apple Python".
      
Pygame can be installed via "pip". Just enter "pip" on the console
to see whether it is installed:
      
        pip
      
If it isn't, you can install it with:
      
        sudo easy_install pip
        
If pip is working, search for Pygame via pip (console command):
      
        sudo pip search pygame
      
Somewhere in the list, you should see something like
      
        Pygame (1.9.2b8)   - Python Game Development
        
Install that with:
      
        sudo pip install pygame

#### Hardware

Notice that the original Launchpad Mk1 requires an USB driver. Thanks, [Stewart!][13].  
Get it from [here][14] (Novation USB Driver-2.7.dmg).

As it seems, all newer Launchpads work right out of the box, no driver required.

### For Windows users

      MIDI implementation in PyGame 1.9.2+ is broken and running this might
      bring up an 'insufficient memory' error ( pygame.midi.Input() ).

      SOLUTION: use v1.9.1 (or try v1.9.3)

### For Linux and especially Raspberry-Pi users:

      Due to some bugs in PyGame's MIDI implementation, the buttons of the Launchpad Mk1
      won't work after you restarted a program (LEDs are not affected).

      WORKAROUND #2: Simply hit one of the AUTOMAP keys (the topmost 8 buttons).
                     For whatever reason, this makes the MIDI button events
                     appearing again...

      WORKAROUND #1: Pull the Launchpad's plug out and restart... (annoying).

### Other Notes

#### Launchpad (Pro) not recognized, playing fireworks demo

Just discovered another oddity...

I attached a Launchpad Pro to my Linux box, as many times before, to finally add the
button methods, but it refused to show up as an USB device. Instead of the "note mode",
indicated by a turquoise/pink colour pattern, it played that "fireworks animation" and
did nothing...

The first time I discovered that, I blamed it on an attached FTDI UART chip, but as it
turned out, that was not the reason it didn't work.

It "simply" was a power issue.

So, if your Launchpad Pro shows that firework demo, check your USB cable!  
Seriously. That thing draws a lot of current and most USB cables simply
do not conform to the USB standard.

Mine "looked quite good" from the outside.  
With its ~5.5mm diameter, I assumed it had AWG 22 (~60mOhm/m) or better, but it in fact
has ~drumroll~ AWG 28 (~240mOhm/m) and two thick plastic strings to fill the gaps.

Well, we all know that companies try to save money wherever they can, but that's just
fraud...

Btw, the fireworks demo will play whenever the Launchpad cannot be enumerated (configured).  
[...]

---
## Common class methods overview (valid for all devices)

### Device control functions

    Open( [name], [number] )
    Close()
    Reset()
    ButtonFlush()
    

### Utility functions

    ListAll()
    
    
---
## Launchpad Mk1 "Classic" class methods overview (valid for green/red LED devices)

### LED functions

    LedGetColor( red, green )
    LedCtrlRaw( number, red, green )
    LedCtrlXY( x, y, red, green )
    LedCtrlRawRapid( allLeds )
    LedCtrlAutomap( number, red, green )
    LedAllOn()
    LedCtrlChar( char, red, green, offsx = 0, offsy = 0 )
    LedCtrlString( str, red, green, dir = 0 )

### Button functions

    ButtonChanged()
    ButtonStateRaw()
    ButtonStateXY()
    ButtonFlush()


---
## Launchpad "Mk2" and "Pro" class methods overview (valid for RGB LED devices)

### LED functions

    LedSetMode( mode )
    LedGetColorByName( name )
    LedCtrlRaw( number, red, gree, [blue] )
    LedCtrlRawByCode( number, [colorcode] )
    LedCtrlXY( x, y, red, green, [blue] )
    LedCtrlXYByCode( x, y, colorcode )
    LedCtrlXYByRGB( x, y, colorlist )
    LedCtrlChar( char, red, green, [blue], [offsx], [offsy] )
    LedCtrlString( string, red, green, [blue], [direction], [waitms] )
    LedAllOn( [colorcode] )


### Button functions

    ButtonStateRaw()
    ButtonStateXY()
    ButtonFlush()


### Color codes

All RGB Launchpads have a 128 color palette built-in.  
Controlling LEDs with colors from the palette is about three times faster than
using the, indeed much more comfortable, RGB notation.

![RGB color palette](/images/lppro_colorcodes.png)

---
## Detailed description of common Launchpad methods

### Open( [number], [name] )

    Opens the a Launchpad and initializes it.  
    Please notice that some devices have up to six MIDI entries!.
    A dump by ListAll(), with a "Pro", a Mk1 "Mini" and a "Mk2" might look like:
    
        ('ALSA', 'Midi Through Port-0', 0, 1, 0)
        ('ALSA', 'Midi Through Port-0', 1, 0, 0)
        ('ALSA', 'Launchpad Pro MIDI 1', 0, 1, 1)
        ('ALSA', 'Launchpad Pro MIDI 1', 1, 0, 1)
        ('ALSA', 'Launchpad Pro MIDI 2', 0, 1, 0)
        ('ALSA', 'Launchpad Pro MIDI 2', 1, 0, 0)
        ('ALSA', 'Launchpad Pro MIDI 3', 0, 1, 0)
        ('ALSA', 'Launchpad Pro MIDI 3', 1, 0, 0)
        ('ALSA', 'Launchpad Mini MIDI 1', 0, 1, 0)
        ('ALSA', 'Launchpad Mini MIDI 1', 1, 0, 0)
        ('ALSA', 'Launchpad MK2 MIDI 1', 0, 1, 0)
        ('ALSA', 'Launchpad MK2 MIDI 1', 1, 0, 0)

    You'll only need to count the entries if you have two or more identical Launchpads attached.
    
      PARAMS: <number> OPTIONAL, number of Launchpad to open.
                       1st device = 0, 2nd device = 1, ...
                       Defaults to 0, the 1st device, if not given.
              <name>   OPTIONAL, only consider devices whose names contain
                       the string <name>. The default names for the classes are:
                         Launchpad()     -> "Launchpad"
                         LaunchpadMk2()  -> "Mk2"
                         LaunchpadPro()  -> "Pro"
                       It is sufficient to search for a part of the string, e.g.
                       "chpad S" will find a device named "Launchpad S" or even
                       "Novation Launchpad S"

      RETURN: True     success
              False    error

	As of 12/2016, the name search patterns are case insensitive, hence strings like "mk2", "pRo"
	or even "lAunCHpAd MiNI" are valid too.

    Notice that the default name for the class Launchpad(), the "Mk1" or "Classic" Launchpads,
    will also react to an attached "Pro" or "Mk2" model. In that case, it's required to either
    enter the complete name (as shown by "ListAll()").


      EXAMPLES:
              # Open the first device attached:
              lp.Open()
              
              # Open the 2nd Launchpad:
              lp.Open( 1 )
              
              # Open the 3rd Launchpad Mini:
              lp.Open( 2, "Launchpad Mini")
              
              # alternative:
              lp.Open( name = "Launchpad Mini", number = 0)
              
              # open the 1st "Mk2"
              lp = launchpad.LaunchpadMk2()  # notice the "Mk2" class!
              lp.Open()                      # equals Open( 0, "Mk2" )
              
              # open the 1st "Pro"
              lp = launchpad.LaunchpadPro()  # notice the "Pro" class!
              lp.Open()                      # equals Open( 0, "Pro" )


### Check( [number], [name] )

    Checks if a device is attached.
    Uses exactly the same notation as Open(), but only returns True or False,
    without opening anything.
    
    Like Open(), this method uses different default names for the different classes:
      Launchpad()     -> "Launchpad"
      LaunchpadMk2()  -> "Mk2"
      LaunchpadPro()  -> "Pro"
      
    Notice that it's absolutely safe to query for an "Pro" or "Mk2" from all classes, e.g.:
    
      lp = lauchpad.Launchpad()        # Launchpad "Mk1" or "Classic" class
      if lp.Check( 0, "Pro" ):         # check for "Pro"
        lp = launchpad.LaunchpadPro()  # "reload" the new class for the "Pro"
        lp.Open()                      # equals lp.Open( 0, "Pro" )
    
    Search patterns are case insensitive.  
    
      PARAMS: see Open()
      
      RETURN: True     device exists
              False    device does not exist


### Close()

    Bug in PyGame. Don't call it (yet)...

      PARAMS:
      RETURN:


### ButtonFlush()

    Flushes the Launchpads button buffer.
    If you do not poll the buttons frequently or even if your software is not running,
    the Launchpad will store each button event in its buffer.
    This function can be used to clear all button events.

      PARAMS:
      RETURN:


### ListAll()

    Debug function.
    Can be called any time and does not even require Open().
    Prints a list of all detected MIDI devices and addresses.

      PARAMS:
      RETURN:


---
## Detailed description of Launchpad Mk1 "Classic" only methods


### Reset()

    Resets the Launchpad and (quickly) turns off all LEDs.
    Notice that only the Mk1 performs a 

      PARAMS:
      RETURN:


### LedGetColor( red, green )

    Returns a the special Launchpad color coding format, calculated
    from a red and green intensity value.

      PARAMS: <red>    red   LED intensity 0..3
              <green>  green LED intensity 0..3
      RETURN: number   Launchpad color code


### LedCtrlRaw( number, red, green )

    Controls an LED via its number (see table somewhere below)

      PARAMS: <number> number of the LED to control
              <red>    red   LED intensity 0..3
              <green>  green LED intensity 0..3
      RETURN:


### LedCtrlXY( x, y, red, green )

    Controls an LED via its coordinates.

      PARAMS: <x>      x coordinate of the LED to control
              <y>      y coordinate of the LED to control
              <red>    red   LED intensity 0..3
              <green>  green LED intensity 0..3
      RETURN:


### LedCtrlRawRapid( allLeds )

    Sends a list of consecutive, special color values to the Launchpad.
    Requires (less than) half of the commands to update all buttons:
    [ LED1, LED2, LED3, ... LED80 ]
    First, the 8x8 matrix is updated, left to right, top to bottom.
    Afterwards, the algorithm continues with the rightmost buttons and
    the top "automap" buttons.

    LEDn color format: 00gg00rr <- 2 bits green, 2 bits red (0..3)
    Function LedGetColor() will do the coding for you...

    Notice that the amount of LEDs needs to be even.
    If an odd number of values is sent, the next, following LED is
    turned off!

      PARAMS: <allLeds> A list of up to 80 Launchpad color codes.
      RETURN:


### LedCtrlAutomap( number, red, green )

    Control one of the "automap" buttons (top row).
    Legacy function, provided for compatibility.

      PARAMS: <number> number of the LED to control
              <red>    red   LED intensity 0..3
              <green>  green LED intensity 0..3

### LedAllOn()

    Turns on all LEDs.

      PARAMS: 
      RETURN:

		
### LedCtrlChar( char, red, green, offsx = 0, offsy = 0 )

    Sends character <char> in colors <red/green> (0..3 each) and
    lateral offset <offsx> (-8..8) to the Launchpad.
    <offsy> does not have yet any function.
    
    It is highly recommended to use <offsx> and <offsy> as
    named parameters, for compatible code with the RGB Launchpads, e.g.:
    
      lp.LedCtrlChar( 'a', 3, 2, offsx = xvar )

      PARAMS: <char>   one field string to display; e.g.: 'A'
              <red>    red   LED intensity 0..3
              <green>  green LED intensity 0..3
              <offsx>  x offset of the character on the main, 8x8 matrix (-8..8)
                       Negative is left and positive right.
              <offsy>  no function
      RETURN:

      EXAMPLES:
              # scroll a red 'A' from left to right
              for x in range( -8, 9 ):
                lp.LedCtrlChar( 'A', 3, 0, offsx = x )
                time.wait( 100 )
		

### LedCtrlString( string, red, green, direction = 0, waitms = 150 )

    Scrolls <string> across the Launchpad's main, 8x8 matrix.
    <red/green> specify the color and intensity (0..3 each).
    <direction> determines the direction of scrolling.
    Dirty hack: <waitms>, by default 150, delays the scrolling speed.
    
    WARNING:
    Too short times will overflow the Launchpad's buffer and mess up
    the screen.
    
    For future compatibility, it is highly recommended to use
    <direction> and <waitms> as a named arguments, e.g.:
    
      lp.LedCtrlString( "Hello", 3,1, direction = -1, waitms = 100 )


      PARAMS: <string>     a string to display; e.g.: 'Hello'
              <red>        red   LED intensity 0..3
              <green>      green LED intensity 0..3
              <direction> -1 -> scroll right to left
                           0 -> do not scroll, just show the character
                           1 -> scroll left to right
              <waitms>     OPTIONAL: delay for scrolling speed, default 150
      RETURN:


### ButtonChanged()

    Returns True if a button event occured. False otherwise.

      PARAMS:
      RETURN: True/False
		

### ButtonStateRaw()

    Returns the state of the buttons in RAW mode.

      PARAMS:
      RETURN: [ ]                        An empty list if no event occured, otherwise...
              [ <button>, <True/False> ] ... a list with two fields:
              <button> is the RAW button number, the second field determines
              if the button was pressed <True> or released <False>.


### ButtonStateXY()

    Returns the state of buttons in X/Y mode.

      PARAMS:
      RETURN: [ ]                        An empty list if no event occured, otherwise...
              [ <x>, <y>, <True/False> ] ... a list with three fields:
              <x> is the x coordinate of the button, <y>, guess what, the
              y coordinate. The third field reveals if the button was pressed
              <True> or released <False>.


---
## Detailed description of Launchpad "Pro" or "Mk2" only methods

### LedSetMode( mode ) *>>> PRO ONLY <<<*

    Sets the Launchpad's mode.
    For proper operation with launchpad.py, the "Pro" must be set to "Ableton Live" mode.
    There is no need to call this method as it is automatically executed within Open().

      PARAMS: <mode>   0 selects "Ableton Live mode" (what we need)
                       1 selects "Standalone mode"   (power-up default)
      RETURN:


### LedGetColorByName( name )

    WORK IN PROGRESS! ONLY A FEW COLORS, SO FAR!

    Returns a color in the special Launchpad Pro color code format, derived
    from a color name, in the string <name>.
    [...]

      PARAMS: <name>   a name of a color in lower caps, "red", "green"...
      RETURN: number   Launchpad Pro color code

      EXAMPLES:
              colorRed = LP.LedGetColorByName( "red" )
    
    Supported, so far:
      off, black, white, red, green


### LedCtrlRaw( number, red, green, [blue] )

    +++ NOTICE:
    +++   It is recommended to always call this with a "blue" parameter.
    +++   The compatibility mode will be removed soon. 
    
    Controls an LED via its number and red, green and blue intensity values.
    
    This method uses system-exclusive MIDI messages, which require 10 bytes to
    be sent for each message. For a faster version, hence less comfortable version,
    see LedCtrlRawByCode() below (though even sending 10 bytes is pretty fast on the Pro).
    
    If <blue> is omitted, this method runs in "Mk1" compatibility mode, which only
    had red/green LEDs and intensities ranging from 0..3. In that mode, the input
    arguments are multiplied by 21, to map 0..3 to 0..63.
    
    Notice that the "Pro" and "Mk2" have different LED number layouts.
    Please see tables, somewhere below.

      PARAMS: <number>    number of the LED to control
              <red>       a number from 0..63
              <green>     a number from 0..63
              <blue>      OPTIONAL, a number from 0..63
      RETURN:


### LedCtrlRawByCode( number, [colorcode] )

    Controls an LED via its number and colorcode.
    If <colorcode> is omitted, 'white' is used.
    This is about three times faster than the comfortable RGB method LedCtrlRaw().

      PARAMS: <number>     number of the LED to control
              <colorcode>  OPTIONAL, a number from 0..127
      RETURN:


### LedCtrlXY( x, y, red, green, [blue], [mode] )

    +++ NOTICE:
    +++   It is recommended to always call this with a "blue" parameter.
    +++   The compatibility mode will be removed soon. 
    
    Controls an LED via its x/y coordinates and red, green or blue intensity values.
    An additional <mode> parameter determines the origin of the x-axis.
    
    If <blue> is omitted, this method operates in "Mk1" compatibility mode.
    The Mk1 Launchpad only had 2 bit intensity values (0..3). In compatibility
    mode, these values are now multiplied by 21, to extend the range to 0..63.
    That way, old, existing code, written for the classic Launchpads does not
    need to be changed.
    
    For "Pro" only:
      By default, if <mode> is omitted, the origin of the x axis is the left side
      of the 8x8 matrix, like in the "Mk1" mode (those devices had no round buttons
      on the left).
      If <mode> is set to "pro" (string), x=0 will light up the round buttons on the
      left side. Please also see the table for X/Y modes somewhere at the end of this
      document.

    This method uses system-exclusive MIDI messages, which require 10 bytes to
    be sent for each message. For a faster version, hence less comfortable version,
    see LedCtrlXYByCode() below.
    
      PARAMS: <x>      x coordinate of the LED to control
              <y>      y coordinate of the LED to control
              <red>    red   LED intensity 0..63 (or 0..3 in "Mk1" mode)
              <green>  green LED intensity 0..63 (or 0..3 in "Mk1" mode)
              <blue>   blue  LED intensity 0..63 (omit  for  "Mk1" mode)
              <mode>   OPTIONAL: "pro" selects new x/y origin >>> PRO ONLY <<<
      RETURN:


### LedCtrlXYByCode( x, y, colorcode, [mode] )

    Controls an LED via its x/y coordinates and a color from the color palette.
    
    Except for the color code, this function does the same as LedCtrlXY() does,
    but about 3 times faster.
    
      PARAMS: <x>          x coordinate of the LED to control
              <y>          y coordinate of the LED to control
              <colorcode>  a number from 0..127
              <mode>       OPTIONAL: "pro" selects new x/y origin >>> PRO ONLY <<<
      RETURN:


### LedCtrlXYByRGB( x, y, colorlist, [mode] )

    Controls an LED via its x/y coordinates and a list of colors in RGB format.
    
    This function does the same as LedCtrlXY() does, except that the color information
    is now passed in as list [R,G,B].
    
      PARAMS: <x>          x coordinate of the LED to control
              <y>          y coordinate of the LED to control
              <colorlist>  a list with [ R, G, B ] color codes; each from 0..63
              <mode>       OPTIONAL: "pro" selects new x/y origin >>> PRO ONLY <<<
      RETURN:
      
      EXAMPLES:
              LP.LedCtrlXYByRGB( 3, 7, [63, 42, 0] )


### LedCtrlChar( char, red, green, [blue], offsx = 0, offsy = 0 )

    +++ NOTICE:
    +++   It is recommended to always call this with a "blue" parameter.
    +++   The compatibility mode will be removed soon.
    
    Sends character <char> in colors <red/green/blue> (0..63 each) and
    lateral offset <offsx> (-8..8) to the Launchpad.
    <offsy> does not have yet any function.
    
    It is highly recommended to use <offsx> and <offsy> as
    named parameters, for compatible code with the RGB Launchpads, e.g.:
    
      lp.LedCtrlChar( 'a', 3, 2, offsx = xvar )
      
    If <blue> is ommited, this methods runs in "Mk1" compatibility
    mode and multiplies the <red> and <green> intensity values with 21, to
    adapt the old 0..3 range to the new 0..63 one of the "Pro" mode.
    That way, it is compatible to old, existing "Mk1" code.

      PARAMS: <char>   one field string to display; e.g.: 'A'
              <red>    red   LED intensity 0..63 (or 0..3 in "Mk1" mode)
              <green>  green LED intensity 0..63 (or 0..3 in "Mk1" mode)
              <blue>   blue  LED intensity 0..63 (omit  for  "Mk1" mode)
              <offsx>  x offset of the character on the main, 8x8 matrix (-8..8)
                       Negative is left and positive right.
              <offsy>  no function
      RETURN:

      EXAMPLES:
              # scroll a purple 'A' from left to right
              for x in range( -8, 9 ):
                lp.LedCtrlChar( 'A', 63, 0, 63, offsx = x )
                time.wait( 100 )


### LedCtrlString( string, red, green, [blue], direction = 0, waitms = 150 )

    +++ NOTICE:
    +++   It is recommended to always call this with a "blue" parameter.
    +++   The compatibility mode will be removed soon (and the output on
    +++   Mk2 and Pro pads might be messed up).
    
    Notice that the Launchpad Pro has string scrolling capabilities built in, but
    this function provides the old, Mk1 compatible functionality. Advantages
    are custom fonts and symbols (in the future).

    Scrolls a string <str> across the Launchpad's main, 8x8 matrix.
    <red/green/blue> specify the color and intensity (0..63 each).
    <direction> determines the direction of scrolling.
    Dirty hack: <waitms>, by default 150, delays the scrolling speed.
    
    If <blue> is omitted, "Mk1" compatibility mode is turned on and the old
    0..3 <red/green> intensity values are strechted to 0..63.
    
    For future compatibility, it is highly recommended to use
    <direction> and <waitms> as a named arguments, e.g.:
    
      lp.LedCtrlString( "Hello", 3,1, direction = -1, waitms = 100 )


      PARAMS: <string>     a string to display; e.g.: 'Hello'
              <red>        red   LED intensity 0..63 (or 0..3 in "Mk1" mode)
              <green>      green LED intensity 0..63 (or 0..3 in "Mk1" mode)
              <blue>       green LED intensity 0..63 (omit  for  "Mk1" mode)
              <direction> -1 -> scroll right to left
                           0 -> do not scroll, just show the character
                           1 -> scroll left to right
              <waitms>     OPTIONAL: delay for scrolling speed, default 150
      RETURN:


### LedAllOn( [colorcode] )

    Quickly sets all LEDs to the color code given by <colorcode>.
    If <colorcode> is omitted, 'white' is used.

      PARAMS: <colorcode>   OPTIONAL, a number from 0..127
      RETURN:


### ButtonStateRaw()

    Returns the state of the buttons in RAW mode.
    
    Notice that this is not directly compatible with the "Mk1" ButtonStateRaw()
    method, which returns [ <button>, <True/False> ].

      PARAMS:
      RETURN: [ ]                    An empty list if no event occured, otherwise...
              [ <button>, <value> ]  ... a list with two fields:
              <button> is the button number, the second field, <value> determines
              the intensity (0..127) with which the button was pressed.
              0 means that the button was released.


### ButtonStateXY( [mode] )

    Returns the state of the buttons in X/Y mode.
    
    Notice that this is not directly compatible with the "Mk1" ButtonStateRaw()
    method, which returns [ <button>, <True/False> ].

      PARAMS: <mode>       OPTIONAL: "pro" selects new x/y origin >>> PRO ONLY <<<
      RETURN: [ ]                    An empty list if no event occured, otherwise...
              [ <x>, <y>, <value> ]  ... a list with three fields:
              <x> and <y> are the button's coordinates. The third field, <value> determines
              the intensity (0..127) with which the button was pressed.
              0 means that the button was released.
              Notice that "Mk2" Pads will only return either 0 or 127.
              They don't have the full analog mode like the "Pro" has.


---
## Button and LED codes, Launchpad Mk1 "Classic" (red/green LEDs)

### RAW mode

    +---+---+---+---+---+---+---+---+ 
    |200|201|202|203|204|205|206|207| < or 0..7 with LedCtrlAutomap()
    +---+---+---+---+---+---+---+---+   

    +---+---+---+---+---+---+---+---+  +---+
    |  0|...|   |   |   |   |   |  7|  |  8|
    +---+---+---+---+---+---+---+---+  +---+
    | 16|...|   |   |   |   |   | 23|  | 24|
    +---+---+---+---+---+---+---+---+  +---+
    | 32|...|   |   |   |   |   | 39|  | 40|
    +---+---+---+---+---+---+---+---+  +---+
    | 48|...|   |   |   |   |   | 55|  | 56|
    +---+---+---+---+---+---+---+---+  +---+
    | 64|...|   |   |   |   |   | 71|  | 72|
    +---+---+---+---+---+---+---+---+  +---+
    | 80|...|   |   |   |   |   | 87|  | 88|
    +---+---+---+---+---+---+---+---+  +---+
    | 96|...|   |   |   |   |   |103|  |104|
    +---+---+---+---+---+---+---+---+  +---+
    |112|...|   |   |   |   |   |119|  |120|
    +---+---+---+---+---+---+---+---+  +---+

### X/Y mode

      0   1   2   3   4   5   6   7      8   
    +---+---+---+---+---+---+---+---+ 
    |0/0|1/0|   |   |   |   |   |   |         0
    +---+---+---+---+---+---+---+---+ 

    +---+---+---+---+---+---+---+---+  +---+
    |0/1|   |   |   |   |   |   |   |  |   |  1
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  2
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |5/3|   |   |  |   |  3
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  4
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  5
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |4/6|   |   |   |  |   |  6
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  7
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |8/8|  8
    +---+---+---+---+---+---+---+---+  +---+


---
## Button and LED codes, Launchpad "Mk2" (RGB LEDs)

### RAW mode

    +---+---+---+---+---+---+---+---+ 
    |104|   |106|   |   |   |   |111|
    +---+---+---+---+---+---+---+---+ 
    
    +---+---+---+---+---+---+---+---+  +---+
    | 81|   |   |   |   |   |   |   |  | 89|
    +---+---+---+---+---+---+---+---+  +---+
    | 71|   |   |   |   |   |   |   |  | 79|
    +---+---+---+---+---+---+---+---+  +---+
    | 61|   |   |   |   |   | 67|   |  | 69|
    +---+---+---+---+---+---+---+---+  +---+
    | 51|   |   |   |   |   |   |   |  | 59|
    +---+---+---+---+---+---+---+---+  +---+
    | 41|   |   |   |   |   |   |   |  | 49|
    +---+---+---+---+---+---+---+---+  +---+
    | 31|   |   |   |   |   |   |   |  | 39|
    +---+---+---+---+---+---+---+---+  +---+
    | 21|   | 23|   |   |   |   |   |  | 29|
    +---+---+---+---+---+---+---+---+  +---+
    | 11|   |   |   |   |   |   |   |  | 19|
    +---+---+---+---+---+---+---+---+  +---+
    

### X/Y mode

      0   1   2   3   4   5   6   7      8   
    +---+---+---+---+---+---+---+---+ 
    |0/0|   |2/0|   |   |   |   |   |         0
    +---+---+---+---+---+---+---+---+ 
     
    +---+---+---+---+---+---+---+---+  +---+
    |0/1|   |   |   |   |   |   |   |  |   |  1
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  2
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |5/3|   |   |  |   |  3
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  4
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  5
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |4/6|   |   |   |  |   |  6
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |   |  7
    +---+---+---+---+---+---+---+---+  +---+
    |   |   |   |   |   |   |   |   |  |8/8|  8
    +---+---+---+---+---+---+---+---+  +---+
    

---
## Button and LED codes, Launchpad "Pro" (RGB LEDs)

### RAW mode

           +---+---+---+---+---+---+---+---+ 
           | 91|   |   |   |   |   |   | 98|
           +---+---+---+---+---+---+---+---+ 
    
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 80|  | 81|   |   |   |   |   |   |   |  | 89|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 70|  |   |   |   |   |   |   |   |   |  | 79|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 60|  |   |   |   |   |   |   | 67|   |  | 69|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 50|  |   |   |   |   |   |   |   |   |  | 59|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 40|  |   |   |   |   |   |   |   |   |  | 49|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 30|  |   |   |   |   |   |   |   |   |  | 39|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 20|  |   |   | 23|   |   |   |   |   |  | 29|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 10|  |   |   |   |   |   |   |   |   |  | 19|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    
           +---+---+---+---+---+---+---+---+ 
           |  1|  2|   |   |   |   |   |  8|
           +---+---+---+---+---+---+---+---+ 

### X/Y "Classic" mode

      9      0   1   2   3   4   5   6   7      8   
           +---+---+---+---+---+---+---+---+ 
           |0/0|   |2/0|   |   |   |   |   |         0
           +---+---+---+---+---+---+---+---+ 
            
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |0/1|   |   |   |   |   |   |   |  |   |  1
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |9/2|  |   |   |   |   |   |   |   |   |  |   |  2
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |5/3|   |   |  |   |  3
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  4
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  5
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |4/6|   |   |   |  |   |  6
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  7
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |9/8|  |   |   |   |   |   |   |   |   |  |8/8|  8
    +---+  +---+---+---+---+---+---+---+---+  +---+
          
           +---+---+---+---+---+---+---+---+ 
           |   |1/9|   |   |   |   |   |   |         9
           +---+---+---+---+---+---+---+---+ 

### X/Y "Pro" mode

      0      1   2   3   4   5   6   7   8      9
           +---+---+---+---+---+---+---+---+ 
           |1/0|   |3/0|   |   |   |   |   |         0
           +---+---+---+---+---+---+---+---+ 
            
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |1/1|   |   |   |   |   |   |   |  |   |  1
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |0/2|  |   |   |   |   |   |   |   |   |  |   |  2
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |6/3|   |   |  |   |  3
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  4
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  5
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |5/6|   |   |   |  |   |  6
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  7
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |0/8|  |   |   |   |   |   |   |   |   |  |9/8|  8
    +---+  +---+---+---+---+---+---+---+---+  +---+
          
           +---+---+---+---+---+---+---+---+ 
           |   |2/9|   |   |   |   |   |   |         9
           +---+---+---+---+---+---+---+---+ 







---
Have fun  
FMMT666(ASkr)  



[1]: https://global.novationmusic.com/launch/launchpad
[2]: http://www.python.org
[3]: http://www.pygame.org
[4]: http://www.raspberrypi.org
[5]: http://pi.minecraft.net/
[6]: http://www.askrproject.net
[7]: https://mtc.cdn.vine.co/r/videos/5B6AFA722E1181009294682988544_30ec8c83a82.1.5.18230528301682594589.mp4
[8]: https://mtc.cdn.vine.co/r/videos/B02C20F7301181005332596555776_3da8b2c29ec.1.5.3791810774169827111.mp4
[9]: https://mtc.cdn.vine.co/r/videos/EFB02602EF1300276501647966208_4cce4117438.5.1.10016548273760817556.mp4
[10]: https://novationmusic.de/launch/launchpad-mk1
[11]: https://creativecommons.org/licenses/by/4.0/
[12]: https://twitter.com/FMMT666/status/802869723910275072/video/1
[13]: https://github.com/FMMT666/launchpad.py/issues/9
[14]:https://novationmusic.de/support/product-downloads?product=Launchpad+MK1
