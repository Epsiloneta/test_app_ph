import sys
import ctypes


def call_main(args):
    lib = ctypes.CDLL('build/lib.linux-x86_64-2.7/ripser_lib.so')    
    LP_c_char = ctypes.POINTER(ctypes.c_char)
    LP_LP_c_char = ctypes.POINTER(LP_c_char)

    lib.main.argtypes = (ctypes.c_int, # argc
                            LP_LP_c_char) # argv

    argc = len(args)
    argv = (LP_c_char * (argc + 1))()
    for i, arg in enumerate(args):
        enc_arg = arg.encode('utf-8')
        argv[i] = ctypes.create_string_buffer(enc_arg)

    lib.main(argc, argv)

def call_main_save_stdout(args,stdout_file):
    from os import open, close, dup, O_WRONLY, O_CREAT
    old = dup(1)
    close(1)
    open(stdout_file, O_WRONLY|O_CREAT) # should open on 1
    call_main(args)
    close(1)
    dup(old) # should dup to 1
    close(old) # get rid of left overs

call_main_save_stdout(['ripser','ripser/examples/sphere_3_192.lower_distance_matrix'],'output_file')