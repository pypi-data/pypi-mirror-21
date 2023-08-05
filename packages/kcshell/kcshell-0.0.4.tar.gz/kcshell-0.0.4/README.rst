kcshell
=======

What is it:
~~~~~~~~~~~

Simple Python3 based interactive assembly/disassembly shell for various
architectures powered by
`Keystone <http://www.keystone-engine.org/>`__/`Capstone <http://www.capstone-engine.org/>`__.

I simply got tired of using
`metasm\_shell <https://github.com/rapid7/metasploit-framework/blob/master/tools/exploit/metasm_shell.rb>`__
and
`nasm\_shell <https://github.com/rapid7/metasploit-framework/blob/master/tools/exploit/nasm_shell.rb>`__
to assemble and disassemble code.
`Keystone <https://github.com/keystone-engine/keystone>`__ and
`Capstone <https://github.com/aquynh/capstone>`__ are awesome and... I
like Python.

How to install it:
------------------

.. code:: c

    pip3 install kcshell

OR (assuming you have Keystone and Capstone build toolchains installed)

.. code:: c

    git clone https://github.com/fdiskyou/kcshell
    cd kcshell
    python setup.py install

Usage
-----

By default 'kcshell' starts in 'assembler' mode (x86 32 bits). You can
change modes with 'setmode', and you can also change the default
architecture for both the 'assembler' and 'disassembler' with 'setarch'.

.. code:: c

    $ kcshell
    -=[ kcshell v0.0.3 ]=-
    Default Assembler architecture is x86 (32 bits)
    asm> lsmodes
    disasm, asm
    asm> setmode disasm
    Default Disassembler architecture is x86 (32 bits)
    disasm> lsarchs
    x86, mips32, arm_t, x64, arm, x16, arm64, mips64
    disasm> setarch x64
    Disassembler architecture is now x64
    disasm> 

To assemble instructions just type the instructions in the command line.

.. code:: c

    asm> jmp esp
    "\xff\xe4"
    asm> xor eax, eax
    "\x31\xc0"
    asm> setarch x64
    Assembler architecture is now x64
    asm> inc rax
    "\x48\xff\xc0"
    asm> 

To go from opcodes to instructions just type them in the command line.

.. code:: c

    disasm> \xff\xe4
    0x00400000:     jmp     esp
    disasm> \x31\xc0
    0x00400000:     xor     eax, eax
    disasm> setarch x64
    Disassembler architecture is now x64
    disasm> \x48\xff\xc0
    0x00400000:     inc     rax
    disasm> 

For help just use '?' or 'help <command>'.

.. code:: c

    asm> ?

    Documented commands (type help <topic>):
    ========================================
    EOF  exit  help  lsarchs  lsmodes  quit  setarch  setmode

    asm> setmode disasm
    Default Disassembler architecture is x86 (32 bits)
    disasm> ?

    Documented commands (type help <topic>):
    ========================================
    EOF  exit  help  lsarchs  lsmodes  quit  setarch  setmode

    disasm>

To list all the supported architectures just go to the desired mode and
use 'lsarchs'.

.. code:: c

    asm> lsarchs
    mips64, sparc64, sparc, arm_t, x64, x16, arm64, hexagon, systemz, mips32, ppc64, x86, arm, ppc32
    asm> lsmodes
    asm, disasm
    asm> setmode disasm
    Default Disassembler architecture is x86 (32 bits)
    disasm> lsarchs
    mips64, x16, arm64, mips32, arm_t, x86, arm, x64
    disasm> 

TODO
~~~~

-  [STRIKEOUT:Create Python package]
-  Read input from files
-  Set a proper base address for 64 bits architectures

Python Package Index
^^^^^^^^^^^^^^^^^^^^

-  https://pypi.python.org/pypi/kcshell
