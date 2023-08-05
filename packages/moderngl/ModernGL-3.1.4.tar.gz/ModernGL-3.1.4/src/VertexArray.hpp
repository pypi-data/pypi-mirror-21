#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"
#include "Program.hpp"
#include "Buffer.hpp"

struct MGLVertexArray : public MGLContextMember {
	MGLProgram * program;

	PyObject * content;

	MGLBuffer * index_buffer;

	PyObject * attributes;
	PyObject * attributes_proxy;

	int vertex_array_obj;
	int num_vertices;
};

extern PyTypeObject MGLVertexArray_Type;

MGLVertexArray * MGLVertexArray_New();
void MGLVertexArray_Invalidate(MGLVertexArray * vertex_array);
void MGLVertexArray_Complete(MGLVertexArray * vertex_array);
