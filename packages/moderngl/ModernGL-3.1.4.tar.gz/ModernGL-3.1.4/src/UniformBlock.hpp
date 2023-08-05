#pragma once

#include "Python.hpp"

#include "ProgramMember.hpp"

struct MGLUniformBlock : public MGLProgramMember {
	PyObject * name;

	int number;
	int location;

	int array_length;
};

extern PyTypeObject MGLUniformBlock_Type;

MGLUniformBlock * MGLUniformBlock_New();
void MGLUniformBlock_Complete(MGLUniformBlock * uniform_block, const GLMethods & gl);
