---
last_modified_at: 2023-07-31 13:26:00
no_link_title:    false
no_excerpt:       false
hide_image:       false
hide_title:       false

layout:           project
cover:            false
sidebar:          false
order:            0

image:
  path:           /assets/img/projects/AuraOS/banner.png
  srcset:
    1920w:        /assets/img/projects/AuraOS/banner@1x.png
    960w:         /assets/img/projects/AuraOS/banner@0,5x.png
    480w:         /assets/img/projects/AuraOS/banner@0,25x.png
caption:          A simple OS aimed to be clean and easy to use

title:            Aura OS
date:             2021-03-29 11:37:00
description:      Information about Aura OS
hide_description: true
featured:         false

links:
  - title:        Source
    url:          https://github.com/Aurora-Softwares/Aura-OS/
---

<div align="center">


An all new OS, entirely made from the ground up.


______________________________________________________________________

<p align="center">

<a href="#features">Features</a> •
<a href="#requirements">Requirements</a> •
<a href="https://ryvor.github.io/Projects/AuraOS/wiki/">Documentation</a> •
<a href="#license">License</a>

</p>

______________________________________________________________________

</div>

## Expectation vs Reality

### Expectation

Aura OS is to be designed as a basic OS that have a simple GUI and command line, Eventually i would like to introduce my own application file and array of applications.

### Reality

In reality, building an os isnt a simple thing to do, this will be a long term goal of mine, it wont have regular updates, just when i have the time to work on it, amongst my other projects, and i will post updates to the blog [here](https://ryvor.github.io/Posts/) whenever i implement an update.

## Features

- Supports GRUB 2.06 Multiboot 2
- Supports VGA TUI

## Screenshots

Screenshots go here.

## Building the OS

### Requirements

This specification is purely based on my current situation and i am aware you could most likely do it cross-platform so long as you have the required software installed - this will be updated and confirmed as i test cross-platform.

- [Windows 10 64-bit or later](https://www.microsoft.com/en-gb/software-download/windows10)
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
  - sudo apt-get install -y gcc g++ nasm ld make
- [Visual Studio Code (latest)](https://code.visualstudio.com/)
- [F5 anything extension](https://marketplace.visualstudio.com/items?itemName=discretegames.f5anything)
- [qemu](https://qemu.weilnetz.de/w64/)

### Build

To build Aura OS, i have implemented the vscode `launch.json` file preset with a number of tasks.

- `WSL - Build`: this is used to build the kernel, is uses WSL2 to compile the sourcecode into raw binary files in `/out/raw`.
- `WSL - ISO`: This builds the OS files from `/out/raw` into an ISO file and outputs it to `/out/iso`.
- `WSL - Clean`: The Clean function removes all of the Temporary files and the output files completely
- `WSL - Clear`: Similar to clean, it clears out all of the temporary files within the `/src/` folder, but leaves all of the output files
- `Windows - Launch`: This will be executed completely in windows and it will launch the ISO file from within `/out/iso/` that matches the version within the `VERSION` file in the source root in QEMU. It gets QEMU from the C:\Program Files\qemu\ directory.

## Learn more

To learmn more about the project, please [click here!](https://ashwell-design.github.io/MultiDomainX/)!

## License

This project is licensed under the [GNU Affero General Public License v3.0](/Licenses/AGPL-3.0/)
