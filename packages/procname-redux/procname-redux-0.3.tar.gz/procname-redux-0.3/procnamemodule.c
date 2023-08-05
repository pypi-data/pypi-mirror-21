/**
 * Set process titles in Python programs
 *
 * Based on work by Eugene A. Lisitsky
 *
 * Copyright (C) 2009  Ludvig Ericson
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

/* This makes the "s#" format for PyArg_ParseTuple and such take a Py_ssize_t
 * instead of an int or whatever. */
#define PY_SSIZE_T_CLEAN

#include <Python.h>

#ifdef __linux
#include <sys/prctl.h>
#endif

/* This is actually not an exposed Python API, but it's been there since the
 * early days and won't go away. */
void Py_GetArgcArgv(int *argc, char ***argv);

#define BUFFER_SIZE 2048
char name_buffer[BUFFER_SIZE];


static PyObject *procname_getprocname(PyObject *self, PyObject *args) {
    int argc;
    char **argv;
    Py_GetArgcArgv(&argc, &argv);
    return Py_BuildValue("s", *argv);
};

#include <stdio.h>
static PyObject *procname_setprocname(PyObject *self, PyObject *args) {
    int argc;
    char **argv;
    char *name;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    Py_GetArgcArgv(&argc, &argv);

    // Figure out how much space we've got
    int environ_length = -1;
    if (environ) {
        while (environ[++environ_length]);
    }

    unsigned int available_space;
    if (environ_length > 0) {
        available_space = environ[environ_length - 1] + strlen(environ[environ_length - 1]) - argv[0];
    } else {
        available_space = argv[argc - 1] + strlen(argv[argc - 1]) - argv[0];
    }

    if (environ) {
        char **new_environ = malloc((environ_length + 1) * sizeof(char*));

        unsigned int i = -1;
        while (environ[++i]) {
           new_environ[i] = strdup(environ[i]);
        }
        new_environ[environ_length] = NULL;

        environ = new_environ;
    }

    // Shorten the name if needed
    if (available_space > BUFFER_SIZE) {
        available_space = BUFFER_SIZE;
    }
    strncpy(name_buffer, name, available_space - 1);
    name_buffer[available_space - 2] = '\0';
    printf("%s\n", name_buffer);

    // Apply the name
    memset(argv[0], '\0', available_space);
    strcpy(argv[0], name_buffer);


#ifdef __linux
    /* Use the much nicer prctl API where possible (GNU/Linux.)
       Note: Rather than overwriting argv as above, this sets task_struct.comm which is fixed at 16 bytes.
       Not quite the same!
       prctl() with PR_SET_MM and PR_SET_MM_ARG_START/PR_SET_MM_ARG_END could work, but would require
       `setcap 'CAP_SYS_RESOURCE=+ep'`. */
    if (prctl(PR_SET_NAME, name, 0, 0, 0)) {
        PyErr_SetFromErrno(PyExc_OSError);
    }
#endif

    Py_RETURN_NONE;
};

static PyMethodDef procname_methods[] = {
    {"getprocname", procname_getprocname, METH_VARARGS, "getprocname() -> current process name\n"},
    {"setprocname", procname_setprocname, METH_VARARGS, "setprocname(name) -- set process name\n"},
    {NULL, NULL, 0, NULL}
};

PyDoc_STRVAR(procname__doc__, "Module for setting/getting process name");

#if PY_VERSION_HEX >= 0x03000000
    static struct PyModuleDef procname_module_def = {
        PyModuleDef_HEAD_INIT,
        "procname",
        procname__doc__,
        -1,
        procname_methods,
        NULL, NULL, NULL, NULL
    };

    PyMODINIT_FUNC PyInit_procname(void) {
        return PyModule_Create(&procname_module_def);
    }
#else  /* Python 2.x */
    PyMODINIT_FUNC initprocname(void) {
        Py_InitModule3("procname", procname_methods, procname__doc__);
    }
#endif
