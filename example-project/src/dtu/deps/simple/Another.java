package dtu.deps.simple;
import dtu.deps.normal.Primes;

// -> dtu.deps.normal.Primes
// -> dtu.deps.simple.Other
// -> java.lang.System

public class Another extends Other{
    Primes primes = new Primes();
    void SayHi(){
        System.out.println("Hi!");
    }
}
