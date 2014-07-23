blenderconwayslife
==================

AddOn which generates geometry and keyframes for a Conway's Game of Life simulation in Blender. Used to create the documentary "Life": https://vimeo.com/87312053


INSTALLATION
============
- Copy the "conway_life_0_9_1" directory to your Blender addons directory.


CONFIGURATION
=============
- To run from the command line, copy golconfig.cfg.console to golconfig.cfg.
Running from the commandline gives you a way to very quickly play with random
seeds and sizes in order to determine what settings will produce an interesting
simulation to photograph.

- The default configuration is a blender configuration, which generates geometry
and keyframes.

Settings:
---------
[Universe]
GenerationCount - The number of generations the simulation should run for.
Size - The number of lifeforms that form one side of the square (so a setting of
  60 would produce a 60x60 grid).

[Rendering]
Renderer: - "console" to render to the command line, "blender" to render
  geometry and keyframes in blender.
PauseAfterRandomize - Number of seconds to pause the simulation after the
  initial seed (useful for console rendering).


SCENE SETUP
===========
- Make sure the cycles renderer is chosen.
- Create an object and name it "OriginalCell".
