package dtu.deps.tricky;
// This class is a little more tricky.
// It has many dependencies but none to Other :D.
//
// -> dtu.deps.simple.Example
// -> dtu.deps.util.Utils

import dtu.deps.simple.*;
import dtu.deps.util.*;

public class Tricky {
    Example /* System */ Other = new Example();

    Tricky dtu, deps, simple;

    private <Other> void hello(/*dtu.deps.simple.Other*/ Utils Other) {
        Tricky dtu = new Tricky();
        dtu.deps.simple.Other = new Example();
    }
    private <Other> void Other(Other Other) {
        return;
    }
}
