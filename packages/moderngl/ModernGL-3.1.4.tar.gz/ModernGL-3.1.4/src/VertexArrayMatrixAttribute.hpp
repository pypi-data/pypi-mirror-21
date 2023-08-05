#pragma once

#include "Python.hpp"

#include "VertexArrayMember.hpp"

struct MGLVertexArrayMatrixAttribute : public MGLVertexArrayMember {
	PyObject * content;
	int location;
};

extern PyTypeObject MGLVertexArrayMatrixAttribute_Type;

MGLVertexArrayMatrixAttribute * MGLVertexArrayMatrixAttribute_New();
