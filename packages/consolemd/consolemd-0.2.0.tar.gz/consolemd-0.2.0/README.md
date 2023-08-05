# ConsoleMD

ConsoleMD renders markdown to the console.

## Installation

It's highly recommended to install ConsoleMD inside a virtual environment.

```bash
pip install consolemd

# you probably want to make consolemd more accessible so...
cd ~/bin
ln -s ~/path/to/venv/bin/consolemd consolemd
```

## Usage

You can treat `consolemd` pretty much like you would `less` or `pygmentize`.

```bash
consolemd --help
consolemd README.md
cat README.md | consolemd
```

You can change the colors `consolemd` uses via `-s` or the environment
variable `CONSOLEMD_STYLE=name`.

If your terminal doesn't support true color (16 million colors) then
run `consolemd` with `--no-true-color` or set environment variable
`CONSOLEMD_TRUECOL=0`.

If you like really long paragraphs that wrap at terminal edge then
use `--no-soft-wrap` or set `CONSOLEMD_WRAP=0`.

A current at-time-of-writing list of pygment styles is the following:

```text
abap algol algol_nu arduino autumn borland bw colorful default emacs
friendly fruity igor lovelace manni monokai murphy native paraiso_dark
paraiso_light pastie perldoc rainbow_dash rrt sas stata tango trac
vim vs xcode
```

`consolemd` uses `native` by default but `monokai` is also very nice.

## Your terminal

iTerm2 under OSX is great and nicely supports true color. Urxvt under
Linux only pretends to be true color and doesn't do it very well.

If you have strange color issues then running with `--no-true-color`
should be the first thing you try. If that fixes your problem then
make sure to add `CONSOLEMD_TRUECOL=0` to your `.bashrc`.

See this [gist](https://gist.github.com/XVilka/8346728) for more info.

## Why not just use pygments?

Because pygments highlights the markdown but doesn't strip out
the control characters. Also, ConsoleMD uses CommonMark to parse
the markdown instead of the lousy one in pygments _(I'm allowed to
say that since I'm the guy that wrote it)_.

Also, ConsoleMD uses some parts of pygments internally, and uses
pygments to highlight code blocks.

## CommonMark

Over the last few years there's been work on standardizing
markdown with an official spec, that work happens at
[CommonMark.org](http://commonmark.org/).

The python implementation of the specification that I used is
called [CommonMark-py](https://github.com/rtfd/CommonMark-py).

Github has recently (March 2017) converted all internal markdown
to use a CommonMark parser, an interesting article can be found
[here](https://githubengineering.com/a-formal-spec-for-github-markdown/).

## Bugs?

Probably. There are lots of corner cases and it's not always clear what
the proper output should even be. For example, url links and embedded
images. Vertical whitespace is also very tricky and subjective.

Unfortunately `commonmark-py` isn't very easy to use as a library so if
any node types got missed then chaos may ensue. Please open a bug (or even
better a pull request) so that `consolemd` can get patched up.

## Example

![](http://i.imgur.com/bR3AllY.png)
