""" This module contains the functionality for running and compiling C functions """

import numpy
import ctypes as C
import _ctypes
import subprocess
import os
import errno

import numpy.ctypeslib
from kernel_tuner.util import get_temp_filename, delete_temp_file

import logging

class CFunctions(object):
    """Class that groups the code for running and compiling C functions"""

    def __init__(self, iterations=7, compiler_options=None):
        """instantiate CFunctions object used for interacting with C code

        :param iterations: Number of iterations used while benchmarking a kernel, 7 by default.
        :type iterations: int
        """
        self.ITERATIONS = iterations
        self.max_threads = 1024
        self.compiler_options = compiler_options
        self.lib = None

        #test if nvcc is available, otherwise use gcc
        self.compiler = "nvcc"
        try:
            subprocess.check_call([self.compiler, "--version"], stdout=open(os.devnull, 'w'))
        except OSError as e:
            self.compiler = "gcc"
            if e.errno != errno.ENOENT:
                raise e

    def ready_argument_list(self, arguments):
        """ready argument list to be passed to the C function

        :param arguments: List of arguments to be passed to the C function.
            The order should match the argument list on the C function.
            Allowed values are numpy.ndarray, and/or numpy.int32, numpy.float32, and so on.
        :type arguments: list(numpy objects)

        :returns: A list of arguments that can be passed to the C function.
        :rtype: list()
        """
        self.arg_mapping = dict()
        ctype_args = []
        for arg in arguments:
            if isinstance(arg, numpy.ndarray):
                if arg.dtype == 'float32':
                    ctype_args.append(arg.ctypes.data_as(C.POINTER(C.c_float)))
                elif arg.dtype == 'float64':
                    ctype_args.append(arg.ctypes.data_as(C.POINTER(C.c_double)))
                elif arg.dtype == 'int32':
                    ctype_args.append(arg.ctypes.data_as(C.POINTER(C.c_int)))
                else:
                    raise TypeError("unknown dtype for ndarray")
                self.arg_mapping[str(ctype_args[-1])] = arg.shape
            elif numpy.isscalar(arg):
                if hasattr(arg, 'dtype'):
                    np_to_c_type_map = { numpy.int32: C.c_int32,
                            numpy.int64: C.c_int64,
                            numpy.float32: C.c_float,
                            numpy.float64: C.c_double }
                    if type(arg) in np_to_c_type_map:
                        ctype_args.append(np_to_c_type_map[type(arg)](arg))
                    else:
                        raise TypeError("Argument is scalar with a dtype, but does not start with int or float")
                else:
                    if isinstance(arg, int):
                        ctype_args.append(C.c_int(arg))
                    elif isinstance(arg, float):
                        ctype_args.append(C.c_float(arg))
                    else:
                        raise TypeError("Argument is scalar without dtype, and is not instance of int or float")
                self.arg_mapping[str(ctype_args[-1])] = ()
            else:
                raise TypeError("Argument is not a numpy.ndarray and is not a scalar %s" % type(arg))

        return ctype_args


    def compile(self, kernel_name, kernel_string):
        """call the C compiler to compile the kernel, return the function

        :param kernel_name: The name of the kernel to be compiled, used to lookup the
            function after compilation.
        :type kernel_name: string

        :param kernel_string: The C code that contains the function `kernel_name`
        :type kernel_string: string

        :returns: An ctypes function that can be called directly.
        :rtype: ctypes._FuncPtr
        """
        logging.debug('compiling ' + kernel_name)

        if self.lib != None:
            self.cleanup_lib()

        filename = get_temp_filename()
        source_file = filename+".cc"
        kernel_string = "extern \"C\" {\n" + kernel_string + "\n}"

        compiler_options = ["-fPIC"]
        if "#include <omp.h>" in kernel_string:
            compiler_options.append("-fopenmp")

        if self.compiler == "nvcc":
            source_file = source_file[:-1] + "u"
            compiler_options = ["-Xcompiler=" + c for c in compiler_options]

        if self.compiler_options:
            compiler_options += self.compiler_options

        lib_args = []
        if "CL/cl.h" in kernel_string:
            lib_args = ["-lOpenCL"]

        try:
            with open(source_file, 'w') as f:
                f.write(kernel_string)

            subprocess.check_call([self.compiler, "-c", source_file] + compiler_options + ["-o", filename+".o"])
            subprocess.check_call([self.compiler, filename+".o"] + compiler_options + [ "-shared", "-o", filename+".so"] + lib_args)

            self.lib = numpy.ctypeslib.load_library(filename, '.')

            func = getattr(self.lib, kernel_name)
            func.restype = C.c_float

        finally:
            delete_temp_file(source_file)
            delete_temp_file(filename+".o")
            delete_temp_file(filename+".so")


        return func

    def benchmark(self, func, c_args, threads, grid):
        """runs the kernel repeatedly, returns averaged returned value

        The C function tuning is a little bit more flexible than direct CUDA
        or OpenCL kernel tuning. The C function needs to measure time, or some
        other quality metric you wish to tune on, on its own and should
        therefore return a single floating-point value.

        Benchmark runs the C function repeatedly and returns the average of the
        values returned by the C function. The number of iterations is set
        during the creation of the CFunctions object. For all measurements the
        lowest and highest values are discarded and the rest is included in the
        average. The reason for this is to be robust against initialization
        artifacts and other exceptional cases.

        :param func: A C function compiled for this specific configuration
        :type func: ctypes._FuncPtr

        :param c_args: A list of arguments to the function, order should match the
            order in the code. The list should be prepared using
            ready_argument_list().
        :type c_args: list()

        :param threads: Ignored, but left as argument for now to have the same
            interface as CudaFunctions and OpenCLFunctions.
        :type threads: any

        :param grid: Ignored, but left as argument for now to have the same
            interface as CudaFunctions and OpenCLFunctions.
        :type grid: any

        :returns: A robust average of values returned by the C function.
        :rtype: float
        """
        results = []
        for _ in range(self.ITERATIONS):
            value = self.run_kernel(func, c_args, threads, grid)
            results.append(value)
        results = sorted(results)
        return numpy.mean(results[1:-1])


    def run_kernel(self, func, c_args, threads, grid):
        """runs the kernel once, returns whatever the kernel returns

        :param func: A C function compiled for this specific configuration
        :type func: ctypes._FuncPtr

        :param c_args: A list of arguments to the function, order should match the
            order in the code. The list should be prepared using
            ready_argument_list().
        :type c_args: list()

        :param threads: Ignored, but left as argument for now to have the same
            interface as CudaFunctions and OpenCLFunctions.
        :type threads: any

        :param grid: Ignored, but left as argument for now to have the same
            interface as CudaFunctions and OpenCLFunctions.
        :type grid: any

        :returns: A robust average of values returned by the C function.
        :rtype: float
        """
        logging.debug("run_kernel")
        logging.debug("arguments=" + str([str(arg) for arg in c_args]))

        time = func(*c_args)

        #I would like to replace the following with actually capturing
        #stderr and detecting the error directly in Python, it proved
        #however that capturing stderr for non-Python functions from Python
        #is a rather difficult thing to do
        #
        #The current, less than ideal, scheme uses the convention that a
        #negative time indicates a 'too many resources requested for launch'
        if time < 0.0:
            raise Exception("too many resources requested for launch")

        return time


    def memset(self, allocation, value, size):
        """set the memory in allocation to the value in value

        :param allocation: A memory allocation unit
        :type allocation: pycuda.driver.DeviceAllocation

        :param value: The value to set the memory to
        :type value: a single 32-bit float or int

        :param size: The size of to the allocation unit in bytes
        :type size: int
        """
        C.memset(allocation, value, size)


    def memcpy_dtoh(self, dest, src):
        """a simple memcpy expects a ctypes pointer, returns a numpy array

        :param dest: A numpy array to store the data
        :type dest: numpy.ndarray

        :param src: A ctypes pointer to some memory allocation
        :type src: ctypes.pointer
        """
        dest[:] = numpy.ctypeslib.as_array(src, shape=self.arg_mapping[str(src)])


    def cleanup_lib(self):
        """ unload the previously loaded shared library """
        _ctypes.dlclose(self.lib._handle)
