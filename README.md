# splinter
Powershell RAT, with a PoC (single threaded) Python-based server.
NB: the RAT should really be used with a custom server with a backend database - the included server is for demonstration purposes only. 

Splinter has the following environment checks/controls built-in:

* Engagement end-date
* Domain environment variable
* Marker file drop

A randomised poll interval can be set in an attempt to defeat statistical traffic analysis.

Under the covers it uses Net.WebClient. This means it's proxy aware.

Persistence and post-compromise modules are an exercise for the reader. You can run arbitrary PowerShell code from any Internet location with a simple ‘iex’ command.

