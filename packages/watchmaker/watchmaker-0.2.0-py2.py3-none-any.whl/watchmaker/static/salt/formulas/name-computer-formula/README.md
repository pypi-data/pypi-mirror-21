[![license](https://img.shields.io/github/license/plus3it/name-computer-formula.svg)](./LICENSE)
[![Travis Build Status](https://travis-ci.org/plus3it/name-computer-formula.svg?branch=master)](https://travis-ci.org/plus3it/name-computer-formula)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/plus3it/name-computer-formula?branch=master&svg=true)](https://ci.appveyor.com/project/plus3it/name-computer-formula)

# name-computer-formula
Cross-platform salt formula to set the computer name of a system.

## Available States

### name-computer

Set the computer name on Windows, or the hostname on Linux.

## Configuration

The only configuration option is a salt grain, `name-computer:computername`.
The formula will read the grain, and will set the computer name to the value
of the grain. If the grain is unset or set to a value that evaluates as
`False`, then the formula will do nothing.
