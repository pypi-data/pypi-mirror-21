#pragma once

#include "Python.hpp"

#include "Buffer.hpp"

struct MGLBufferAccess : public MGLObject {
	MGLBuffer * buffer;

	void * ptr;

	int buffer_obj;
	int offset;
	int size;
	int access;
};

extern PyTypeObject MGLBufferAccess_Type;

MGLBufferAccess * MGLBufferAccess_New();
