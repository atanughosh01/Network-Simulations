#pragma once
#include "iostream"

using namespace std;

class Error {
    string problem;
public:
    void className(string name) {
        problem = "ClassName :: " + name + "\n";
    }

    void funcName(string name) {
        problem += "FuncName :: " + name + "\n";
    }

    void problemIs(string is) {
        problem += "Problem :: " + is + "\n";
    }

    void show() {
        cout << problem << "\n";
    }
};