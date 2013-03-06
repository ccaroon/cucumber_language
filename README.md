cucumber_language
=================

Cucumber Language support for Komodo (UDL-based). Should work with Komodo 7-8.

Syntax Highlighting
-------------------
Listed below are the various types of Cucumber Syntax and the Komodo Element Type
that defines it's color:

* Comments     --> comments   --> `# this is a comment`
* Tags         --> identifier --> `@tag1 @tag2 @example_tags`
* Strings      --> strings    --> `'Single', "Double" or """Doc Strings"""`
* Numbers      --> numbers    --> `1.0, 123`
* Placeholders --> variables  --> `<input>, <output>`
* Data Tables  --> variables  --> `| value1 | value2 |`
* Keywords     --> keywords   --> `Feature, Background, Given, When, Then, etc...`

Code Intelligence
-----------------

### Auto Complete ###
* Tags         --> Triggered when you type an At Sign (@)
* Placeholders --> Triggered when you type a left Angle Bracket (<)
* Keywords     --> Triggered when you start typing something that looks like a
                   Cucumber keyword.

Manual completion also supported for the above.

### Call Tips ###
None supported.

Building from Source
--------------------
Assuming you have Komodo installed, you can use the `koext` tool to build the
extention:

1. cd to the source code directory
2. `koext build`
3. `cucumber_language-X.Y.Z-ko.xpi` should have been created.

Installing
----------
Drag the .XPI file onto Komodo. You should then see the extension in the Add-Ons
list and be prompted to restart.
