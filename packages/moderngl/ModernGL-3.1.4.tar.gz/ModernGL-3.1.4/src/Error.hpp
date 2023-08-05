#pragma once

#include "Python.hpp"

#define TRACE __FILE__, __LINE__

struct MGLError {
	PyException_HEAD

	PyObject * github;
};

extern PyTypeObject MGLError_Type;

MGLError * MGLError_New(const char * filename, int line, const char * format, ...);
