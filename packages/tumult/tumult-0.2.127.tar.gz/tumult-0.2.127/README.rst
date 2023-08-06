Tumult
======

About
-----

Tumult is an oh-my-zsh compatible plugin that adds macOS-specific
functions and scripts to your ZSH environment.

Tumult will check to see if you're running on macOS and not add aliases
or inject its bin into your PATH if you aren't. This allows you to use
the same plugin list in all your environments without polluting your
``$PATH`` with incompatible functions and scripts on your non-Mac
machines.

.. raw:: html

   <!-- START doctoc generated TOC please keep comment here to allow auto update -->

.. raw:: html

   <!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents** *generated with
`DocToc <https://github.com/thlorenz/doctoc>`__*

-  `Included scripts <#included-scripts>`__
-  `Other Useful macOS tools <#other-useful-macos-tools>`__
-  `Installation <#installation>`__
-  `Bash / not using a framework <#bash--not-using-a-framework>`__
-  `[Antigen](https://github.com/zsh-users/antigen) <#antigenhttpsgithubcomzsh-usersantigen>`__
-  `[Oh-My-Zsh](http://ohmyz.sh/) <#oh-my-zshhttpohmyzsh>`__
-  `[Zgen](https://github.com/tarjoilija/zgen) <#zgenhttpsgithubcomtarjoilijazgen>`__
-  `License <#license>`__

.. raw:: html

   <!-- END doctoc generated TOC please keep comment here to allow auto update -->

Included scripts
----------------

+---------+--------------+
| Script  | Description  |
+=========+==============+
| 720p    | Resets an    |
|         | application' |
|         | s            |
|         | window to    |
|         | 720p         |
|         | (1280x720)   |
|         | for better   |
|         | screencastin |
|         | g.           |
|         | Doesn't work |
|         | with apps    |
|         | that don't   |
|         | support      |
|         | window       |
|         | resizing in  |
|         | their        |
|         | AppleScript  |
|         | dictionary.  |
|         | Copied from  |
|         | Derrick      |
|         | Bailey's     |
|         | `blog <http: |
|         | //lostechies |
|         | .com/derickb |
|         | ailey/2012/0 |
|         | 9/08/screenc |
|         | asting-tip-r |
|         | esize-your-a |
|         | pp-to-720p-1 |
|         | 280x720-in-o |
|         | sx/>`__      |
+---------+--------------+
| battery | Show the     |
| -percen | percentage   |
| tage    | of battery   |
|         | charge       |
+---------+--------------+
| battery | Show the     |
| -time   | estimated    |
|         | battery      |
|         | life.        |
+---------+--------------+
| change- | If you have  |
| wallpap | your desktop |
| er      | wallpaper    |
|         | set to       |
|         | rotate       |
|         | through a    |
|         | folder of    |
|         | images at    |
|         | intervals,   |
|         | this will    |
|         | force an     |
|         | immediate    |
|         | switch       |
+---------+--------------+
| clean-x | Clean up the |
| ml-clip | XML on the   |
|         | clipboard    |
+---------+--------------+
| chrome  | Force        |
|         | opening an   |
|         | URL with     |
|         | Chrome       |
+---------+--------------+
| chrome- | Outputs the  |
| tabs    | URLs for all |
|         | your open    |
|         | Chrome tabs  |
|         | so you can   |
|         | snapshot     |
|         | them         |
+---------+--------------+
| clean-c | Converts     |
| lipboar | contents of  |
| d       | clipboard to |
|         | plain text.  |
+---------+--------------+
| clear-m | Clears the   |
| acos-fo | macOS font   |
| nt-cach | cache,       |
| e       | originally   |
|         | from         |
|         | `awesome-osx |
|         | -command-lin |
|         | e <https://g |
|         | ithub.com/he |
|         | rrbischoff/a |
|         | wesome-osx-c |
|         | ommand-line/ |
|         | blob/master/ |
|         | functions.md |
|         | #app-icons>` |
|         | __           |
+---------+--------------+
| column- | Set the      |
| view    | current      |
|         | directory to |
|         | column view  |
|         | in the       |
|         | Finder       |
+---------+--------------+
| disable | Disable the  |
| -ftp-se | ftp server   |
| rver    | on a Mac     |
+---------+--------------+
| disable | Disable the  |
| -ssh-se | ssh server   |
| rver    | on a Mac     |
+---------+--------------+
| disable | Disable the  |
| -startu | boot chime   |
| p-chime |              |
+---------+--------------+
| eject-a | Eject all    |
| ll      | removable    |
|         | disks        |
+---------+--------------+
| enable- | Enable the   |
| ftp-ser | ftp server   |
| ver     | on a Mac     |
+---------+--------------+
| enable- | Enable the   |
| ssh-ser | ssh server   |
| ver     | on a Mac     |
+---------+--------------+
| enable- | Re-enable    |
| startup | the boot     |
| -chime  | chime        |
+---------+--------------+
| evernot | Create a new |
| e       | Evernote     |
|         | note from    |
|         | stdin or a   |
|         | file         |
+---------+--------------+
| finder- | Show the     |
| path    | path to the  |
|         | frontmost    |
|         | finder       |
|         | window       |
+---------+--------------+
| finder- | Show the     |
| selecti | paths to all |
| on      | items        |
|         | selected in  |
|         | the Finder,  |
|         | quoted so it |
|         | copes with   |
|         | spaces in    |
|         | your         |
|         | directory or |
|         | file names   |
+---------+--------------+
| firefox | Force        |
|         | opening an   |
|         | URL with     |
|         | Firefox      |
+---------+--------------+
| fix-air | Kick         |
| play    | ``coreaudiod |
|         | ``           |
|         | when AirPlay |
|         | stops        |
|         | responding   |
+---------+--------------+
| get-ite | Gets the     |
| rm2-buf | current      |
| fer     | iterm2       |
|         | window's     |
|         | scrollback   |
|         | contents     |
+---------+--------------+
| icon-vi | Set the      |
| ew      | current      |
|         | directory to |
|         | icon view in |
|         | the Finder   |
+---------+--------------+
| imgcat  | Display an   |
|         | image        |
|         | directly in  |
|         | your         |
|         | terminal.    |
|         | Only works   |
|         | with iTerm 2 |
+---------+--------------+
| itunesc | Play/Pause   |
| tl      | iTunes from  |
|         | terminal.    |
+---------+--------------+
| kick-af | Restart file |
| p       | sharing from |
|         | the CLI. I   |
|         | got tired of |
|         | having to    |
|         | remote       |
|         | desktop in   |
|         | to kick the  |
|         | fileserver   |
|         | via the GUI  |
|         | every time   |
|         | Apple's file |
|         | sharing got  |
|         | wedged, now  |
|         | it can be    |
|         | fixed over   |
|         | ``ssh``      |
+---------+--------------+
| kick-sc | Sometimes    |
| reensha | screen       |
| ring    | sharing just |
|         | hangs on my  |
|         | Mini running |
|         | 10.11. This  |
|         | is not new   |
|         | to 10.11, it |
|         | was          |
|         | exhibiting   |
|         | the same     |
|         | annoying     |
|         | behavior on  |
|         | 10.10 and    |
|         | 10.9. The    |
|         | mini is      |
|         | headless and |
|         | it's a pain  |
|         | in the ass   |
|         | to plug it   |
|         | into the TV  |
|         | just long    |
|         | enough to    |
|         | restart      |
|         | screen       |
|         | sharing, so  |
|         | I wrote this |
|         | so I can fix |
|         | it over ssh. |
+---------+--------------+
| kill-sc | Kill the     |
| reensav | screensaver  |
| er      | when it      |
|         | locks up     |
+---------+--------------+
| list-vi | Set the      |
| ew      | current      |
|         | directory to |
|         | column view  |
|         | in the       |
|         | Finder       |
+---------+--------------+
| lockscr | Lock the     |
| een     | screen       |
+---------+--------------+
| mac-hib | Set a Mac to |
| ernate  | use          |
|         | hibernate    |
|         | mode when    |
|         | sleeping     |
+---------+--------------+
| mac-saf | Set a Mac to |
| esleep  | use          |
|         | safesleep    |
|         | mode when    |
|         | sleeping     |
+---------+--------------+
| mac-sle | Set a Mac to |
| ep      | use the      |
|         | default      |
|         | sleep mode   |
|         | when         |
|         | sleeping     |
+---------+--------------+
| macos-f | Shows what   |
| rontmos | application  |
| t-app   | is           |
|         | Frontmost.   |
+---------+--------------+
| mkdmg   | Makes a .dmg |
|         | file from a  |
|         | directory    |
+---------+--------------+
| mkicns  | Creates an   |
|         | .icns file   |
|         | from an      |
|         | image file   |
+---------+--------------+
| naptime | Put the      |
|         | machine to   |
|         | sleep        |
+---------+--------------+
| nitenit | Make a Mac   |
| e       | go to sleep  |
+---------+--------------+
| pbcurl  | ``curl`` the |
|         | address in   |
|         | the          |
|         | clipboard.   |
|         | Originally   |
|         | from Ryan    |
|         | Tomayko's    |
|         | `dotfiles <h |
|         | ttps://githu |
|         | b.com/rtomay |
|         | ko/dotfiles> |
|         | `__          |
+---------+--------------+
| pbinden | Indent the   |
| t       | contents of  |
|         | the          |
|         | clipboard 4  |
|         | spaces. With |
|         | -o, write    |
|         | result to    |
|         | standard     |
|         | output       |
|         | instead of   |
|         | to the       |
|         | clipboard.   |
|         | Originally   |
|         | from Ryan    |
|         | Tomayko's    |
|         | `dotfiles <h |
|         | ttps://githu |
|         | b.com/rtomay |
|         | ko/dotfiles> |
|         | `__          |
+---------+--------------+
| pbsed   | Run          |
|         | ``sed``\ (1) |
|         | on the       |
|         | contents of  |
|         | the          |
|         | clipboard    |
|         | and put the  |
|         | result back  |
|         | on the       |
|         | clipboard.   |
|         | All ``sed``  |
|         | options and  |
|         | arguments    |
|         | are          |
|         | supported.   |
|         | Originally   |
|         | from Ryan    |
|         | Tomayko's    |
|         | `dotfiles <h |
|         | ttps://githu |
|         | b.com/rtomay |
|         | ko/dotfiles> |
|         | `__          |
+---------+--------------+
| pledit  | Convert a    |
|         | plist to     |
|         | XML, run     |
|         | ${EDITOR} on |
|         | it, then     |
|         | convert it   |
|         | back.        |
+---------+--------------+
| safari  | Force        |
|         | opening an   |
|         | URL with     |
|         | Safari       |
+---------+--------------+
| screen- | Display the  |
| resolut | screen       |
| ion     | resolution   |
+---------+--------------+
| set-mac | Set the      |
| os-host | macOS name   |
| name    | of your      |
|         | machine.     |
|         | macOS may be |
|         | UNIX-based,  |
|         | but the      |
|         | Apple        |
|         | eccentriciti |
|         | es           |
|         | mean that    |
|         | no,          |
|         | ``sudo hostn |
|         | ame newname` |
|         | `            |
|         | isn't enough |
|         | if you want  |
|         | the new name |
|         | to be        |
|         | visible on   |
|         | the network  |
|         | for things   |
|         | like File    |
|         | and Screen   |
|         | sharing.     |
+---------+--------------+
| speedup | Speeds up    |
| -apple- | Mail.app by  |
| mail    | vaccuuming   |
|         | the indexes  |
|         | - Originally |
|         | from         |
|         | http://www.h |
|         | awkwings.net |
|         | /2007/03/03/ |
|         | scripts-to-a |
|         | utomate-the- |
|         | mailapp-enve |
|         | lope-speed-t |
|         | rick/        |
+---------+--------------+
| toggle- | Toggle       |
| finder- | whether      |
| show-do | Finder shows |
| tfiles  | dotfiles     |
+---------+--------------+
| unquara | Unquarantine |
| ntine   | a file       |
+---------+--------------+
| volume  | Get/set the  |
|         | system       |
|         | volume       |
+---------+--------------+
| wifi-na | Returns the  |
| me      | name of the  |
|         | WIFI network |
|         | you're       |
|         | connected to |
+---------+--------------+

Other Useful macOS tools
------------------------

-  `Platypus <https://github.com/sveinbjornt/Platypus>`__ - allows you
   to wrap a script inside a Mac GUI wrapper.
-  `awesome-os-command-line <https://github.com/herrbischoff/awesome-osx-command-line>`__
   has a lot of ways to manipulate macOS settings and applications from
   the command line

Installation
------------

Tumult is packaged as a zsh plugin to make it easier to use if you're
already using a zsh framework (I recommend zgen, it is wicked fast and
also supports using oh-my-zsh's internal plugins).

Bash / not using a framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're using bash, or aren't using a framework, you can either \*
Clone this repository and add its bin directory to your ``$PATH`` \* Use
``pip`` to install with ``pip install tumult``. Because I have to
explicitly publish new versions to pypi, the pip package may not alaways
be as current as the git repository.

`Antigen <https://github.com/zsh-users/antigen>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add ``antigen bundle unixorn/tumult.plugin.zsh`` to your ``.zshrc`` with
your other bundle commands.

Antigen will handle cloning the plugin for you automatically the next
time you start zsh. You can also add the plugin to a running zsh with
``antigen bundle unixorn/tumult.plugin.zsh`` for testing before adding
it to your ``.zshrc``.

`Oh-My-Zsh <http://ohmyz.sh/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``cd ~/.oh-my-zsh/custom/plugins``
2. ``git clone git@github.com:unixorn/tumult.plugin.zsh.git tumult``
3. Add tumult to your plugin list - edit ``~.zshrc`` and change
   ``plugins=(...)`` to ``plugins=(... tumult)``

`Zgen <https://github.com/tarjoilija/zgen>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add ``zgen load unixorn/tumult.plugin.zsh`` to your .zshrc file in the
same function you're doing your other ``zgen load`` calls in. Zgen will
handle automatically cloning the plugin for you the next time you do a
``zgen save``.

License
-------

Tumult is Apache 2.0 licensed, except for some scripts in bin that have
other license statements inline.
