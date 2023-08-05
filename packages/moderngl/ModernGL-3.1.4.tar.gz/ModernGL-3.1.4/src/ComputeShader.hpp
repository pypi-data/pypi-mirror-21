#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"

struct MGLComputeShader : public MGLContextMember {
	PyObject * source;

	int program_obj;
	int shader_obj;
};

extern PyTypeObject MGLComputeShader_Type;

MGLComputeShader * MGLComputeShader_New();
void MGLComputeShader_Invalidate(MGLComputeShader * program);
