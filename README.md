# Intro

Linkstats allows you to investigates hardlinked files. It comes in handy if you
do have a backup scheme composed of hardlinked, then rsynched folders...

Here is a quick idea of what each command does. You should have a look at each
command's help (-h) for more info.

- linkstat: get basic info about harlink files between folders
- listonce: receives a list of files in stdin, and spits out the first unique link on stdout
- linkonlyfolders: get a list of folders as arguments, and spit out those that consist only of hardlinks (compared to previous folders, in argument order)

# Todo

- Testing !
- Probably a lot of error handling
