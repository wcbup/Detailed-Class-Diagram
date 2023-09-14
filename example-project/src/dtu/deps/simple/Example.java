package dtu.deps.simple;

import dtu.deps.util.Utils;

// import some.other.Class;

// Known Dependencies
// -> dtu.deps.simple.Other
// -> dtu.deps.util.Utils
// -> java.lang.String

/**
 * This is an example class that contains dependencies.
 *
 * Known dependencies:
 */
public class Example {
    Other other = new Other();

    public static void main(String[] args) {
        Utils.printHello();
    }

}
