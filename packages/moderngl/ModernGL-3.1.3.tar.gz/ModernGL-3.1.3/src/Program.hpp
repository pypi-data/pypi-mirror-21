#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"
#include "Primitive.hpp"

struct MGLProgram : public MGLContextMember {
	PyObject * shaders;

	PyObject * vertex_shader;
	PyObject * fragment_shader;
	PyObject * geometry_shader;
	PyObject * tesselation_evaluation_shader;
	PyObject * tesselation_control_shader;

	PyObject * uniforms;
	PyObject * uniforms_proxy;

	PyObject * uniform_blocks;
	PyObject * uniform_blocks_proxy;

	PyObject * attributes;
	PyObject * attributes_proxy;

	PyObject * varyings;
	PyObject * varyings_proxy;

	MGLPrimitive * geometry_input;
	MGLPrimitive * geometry_output;

	int geometry_vertices;

	int program_obj;
};

extern PyTypeObject MGLProgram_Type;

MGLProgram * MGLProgram_New();
void MGLProgram_Invalidate(MGLProgram * program);
void MGLProgram_Compile(MGLProgram * program, PyObject * outputs);
