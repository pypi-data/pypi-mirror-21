#pragma once

#include "Python.hpp"

#include "ProgramMember.hpp"
#include "Program.hpp"

struct MGLVarying : public MGLProgramMember {
	PyObject * name;

	int number;
	int type;

	// int dimension;
	// int element_size;
	int array_length;

	bool matrix;
};

extern PyTypeObject MGLVarying_Type;

MGLVarying * MGLVarying_New();
void MGLVarying_Invalidate(MGLVarying * varying);
void MGLVarying_Complete(MGLVarying * varying, const GLMethods & gl);
