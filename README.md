# splinter
Powershell RAT, with a Python-based (CherryPy) server and sqlite backend.

Splinter has the following environment checks/controls built-in:

* Engagement end-date
* Domain environment variable
* Marker file drop

A randomised poll interval can be set in an attempt to defeat statistical traffic analysis.

Under the covers it uses Net.WebClient. This means it's proxy aware.

Persistence and post-compromise modules are an exercise for the reader. You can run arbitrary PowerShell code from any Internet location with a simple ‘iex’ command.

