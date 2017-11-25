#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <vector>
#include <fstream>

int main(int, char**); // prototype of Ripser entrypoint

int main_f_wrapper(std::vector<std::string> strings, std::string output_file){
    std::ofstream out(output_file);
    std::streambuf *coutbuf = std::cout.rdbuf(); //save old buf
    std::cout.rdbuf(out.rdbuf()); //redirect std::cout to out.txt!

    // code to convert from vector<string> to char**
    std::vector<char*> cstrings{};
    for(auto& string : strings)
        cstrings.push_back(&string.front());
    auto x = main(cstrings.size(),cstrings.data()); // call to ripser main function

    std::cout.rdbuf(coutbuf); //reset to standard output again

    return x;
}

namespace py = pybind11;

PYBIND11_MODULE(python_example, m) {
    m.doc() = R"pbdoc(
        Simple wrapper for Ripser C++ executable
    )pbdoc";

    m.def("ripser_call", &main_f_wrapper, "function to call ripser executable and save output to file");
}

// TO TEST it should be run in Python:
// from easy_ph.ripser_wrapper import ripser_call
// ripser_call(['ripser','/mnt/c/Users/teixi/Desktop/easy_ph/ripser/examples/sphere_3_192.lower_distance_matrix'],'output_file')