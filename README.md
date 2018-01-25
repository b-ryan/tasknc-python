# pytasknc

A Python ncurses application for [Taskwarrior](https://taskwarrior.org/),
originally based on [tasknc](https://github.com/lharding/tasknc).

## Background

Taskwarrior is a command-line task & todo list manager. It's a wonderful tool
with a robust ecosystem. In fact you can browse the many
[tools](https://taskwarrior.org/tools/) available - like a web UI and more.

One of those available tools is [tasknc](https://github.com/lharding/tasknc).
It is a solid little tool, but nearly immediately I wanted to customize it in a
way not supported by its configuration and I didn't really want to dig into the
plethora of C code. Python is perfect here with its built-in support for
ncurses.

There is an existing project called
[taskhud](https://github.com/usefulthings/taskhud), but for me it had these issues:

- It didn't work
- There's no pypi package

Plus, I have been wanting an excuse to get experience with ncurses for the sake
of another project: [polecat](https://www.polecat.io/).

## Dependencies

This project has one requirement: Python 3. Python 2 is not supported.

## Installation

Install using pip. Note that since you must use Python 3, you might need to use
the `pip3` command, depending on your system:

```
pip install pytasknc
```

## Usage

```
pytasknc
```

## Design

I believe this project is fairly unique in its design, at least as far as an
ncurses application goes. I was heavily inspired by the
[reagent](https://holmsand.github.io/reagent/) Clojure library.

For one, the application state is immutable. The
[models](https://github.com/b-ryan/tasknc-python/blob/master/pytasknc/models.py)
module contains the full state necessary to draw the screen and is made up of
`namedtuple` objects, which are copied and modified whenever some action is
taken on the screen.

You can see the
[actions](https://github.com/b-ryan/tasknc-python/blob/master/pytasknc/actions.py)
module contains the code to respond to any action the user may take. An action
function is one which takes the current state and returns a new state.

The
[draw](https://github.com/b-ryan/tasknc-python/blob/master/pytasknc/draw.py)
module then renders a state into what you see on the screen. In fact, it does a
basic diff (sorta like [React](https://reactjs.org/)) in order to update the
minimal amount of screen necessary. If the code were to always perform a full
draw of the screen, the screen often flickers.
