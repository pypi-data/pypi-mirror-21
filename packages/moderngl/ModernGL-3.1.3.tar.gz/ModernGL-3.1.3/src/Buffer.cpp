#include "Buffer.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"
#include "BufferAccess.hpp"

#include "UniformBlock.hpp"

PyObject * MGLBuffer_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLBuffer * self = (MGLBuffer *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLBuffer_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLBuffer_tp_dealloc(MGLBuffer * self) {

	#ifdef MGL_VERBOSE
	printf("MGLBuffer_tp_dealloc %p\n", self);
	#endif

	MGLBuffer_Type.tp_free((PyObject *)self);
}

int MGLBuffer_tp_init(MGLBuffer * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Buffer manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLBuffer_tp_str(MGLBuffer * self) {
	return PyUnicode_FromFormat("<ModernGL.Buffer>");
}

MGLBufferAccess * MGLBuffer_access(MGLBuffer * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"size", "offset", "readonly", 0};

	int size = -1;
	int offset = 0;
	int readonly = false;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|$iip",
		(char **)kwlist,
		&size,
		&offset,
		&readonly
	);

	if (!args_ok) {
		return 0;
	}

	if (size == -1) {
		size = self->size - offset;
	}

	if (offset < 0 || size > self->size - offset) {
		MGLError * error = MGLError_New(TRACE, "offset = %d or size = %d out of range", offset, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	MGLBufferAccess * access = MGLBufferAccess_New();

	access->buffer = self;
	access->buffer_obj = self->buffer_obj;
	access->offset = offset;
	access->size = size;
	access->access = readonly ? GL_MAP_READ_BIT : (GL_MAP_READ_BIT | GL_MAP_WRITE_BIT);
	access->ptr = 0;

	return access;
}

const char * MGLBuffer_access_doc = R"(
	access(size, offset = 0, readonly = False)

	Keyword Args:
		size: The size.
		offset: The offset.
		readonly: The readonly.
)";

PyObject * MGLBuffer_read(MGLBuffer * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"size", "offset", 0};

	int size = -1;
	int offset = 0;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|I$I",
		(char **)kwlist,
		&size,
		&offset
	);

	if (!args_ok) {
		return 0;
	}

	if (size == -1) {
		size = self->size - offset;
	}

	if (offset < 0 || size < 0 || size + offset > self->size) {
		MGLError * error = MGLError_New(TRACE, "offset = %d or size = %d out of range", offset, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	const GLMethods & gl = self->context->gl;

	gl.BindBuffer(GL_ARRAY_BUFFER, self->buffer_obj);
	void * map = gl.MapBufferRange(GL_ARRAY_BUFFER, offset, size, GL_MAP_READ_BIT);

	if (!map) {
		MGLError * error = MGLError_New(TRACE, "Cannot map buffer");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	PyObject * data = PyBytes_FromStringAndSize((const char *)map, size);

	gl.UnmapBuffer(GL_ARRAY_BUFFER);

	return data;
}

const char * MGLBuffer_read_doc = R"(
	read(size, offset = 0)

	Read the content.

	Args:
		size: The size. Value `-1` means all.

	Keyword Args:
		offset: The offset.

	Returns:
		bytes: binary data.
)";

PyObject * MGLBuffer_write(MGLBuffer * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"data", "offset", 0};

	const char * data = 0;
	int size = 0;
	int offset = 0;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"y#|$I",
		(char **)kwlist,
		&data,
		&size,
		&offset
	);

	if (!args_ok) {
		return 0;
	}

	if (offset < 0 || size + offset > self->size) {
		MGLError * error = MGLError_New(TRACE, "offset = %d or size = %d out of range", offset, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	const GLMethods & gl = self->context->gl;
	gl.BindBuffer(GL_ARRAY_BUFFER, self->buffer_obj);
	gl.BufferSubData(GL_ARRAY_BUFFER, (GLintptr)offset, size, data);
	Py_RETURN_NONE;
}

const char * MGLBuffer_write_doc = R"(
	write(data, offset = 0)

	Write the content.

	Args:
		data: The data.

	Keyword Args:
		offset: The offset.

	Returns:
		None
)";

PyObject * MGLBuffer_orphan(MGLBuffer * self) {
	const GLMethods & gl = self->context->gl;
	gl.BindBuffer(GL_ARRAY_BUFFER, self->buffer_obj);
	gl.BufferData(GL_ARRAY_BUFFER, self->size, 0, self->dynamic ? GL_DYNAMIC_DRAW : GL_STATIC_DRAW);
	Py_RETURN_NONE;
}

const char * MGLBuffer_orphan_doc = R"(
	orphan()

	Orphan the buffer.
)";

PyObject * MGLBuffer_bind_to_uniform_block(MGLBuffer * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"location", 0};

	PyObject * location = 0;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|O",
		(char **)kwlist,
		&location
	);

	if (!args_ok) {
		return 0;
	}

	int block = 0;

	if (location) {
		if (Py_TYPE(location) == &MGLUniformBlock_Type) {
			block = ((MGLUniformBlock *)location)->location;
		}
	} else {
		block = PyLong_AsLong(location);

		if (PyErr_Occurred()) {
			MGLError * error = MGLError_New(TRACE, "location must be either UniformBlock or int not %s", Py_TYPE(location));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}
	}

	const GLMethods & gl = self->context->gl;
	gl.BindBufferBase(GL_UNIFORM_BUFFER, block, self->buffer_obj);
	Py_RETURN_NONE;
}

const char * MGLBuffer_bind_to_uniform_block_doc = R"(
	bind_to_uniform_block(location = 0)
)";

PyObject * MGLBuffer_bind_to_storage_buffer(MGLBuffer * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"location", 0};

	int location = 0;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"|i",
		(char **)kwlist,
		&location
	);

	if (!args_ok) {
		return 0;
	}

	const GLMethods & gl = self->context->gl;
	gl.BindBufferBase(GL_SHADER_STORAGE_BUFFER, location, self->buffer_obj);
	Py_RETURN_NONE;
}

const char * MGLBuffer_bind_to_storage_buffer_doc = R"(
	bind_to_storage_buffer(location = 0)
)";

PyObject * MGLBuffer_release(MGLBuffer * self) {
	MGLBuffer_Invalidate(self);
	Py_RETURN_NONE;
}

const char * MGLBuffer_release_doc = R"(
	release()

	Release the buffer.
)";

PyMethodDef MGLBuffer_tp_methods[] = {
	{"access", (PyCFunction)MGLBuffer_access, METH_VARARGS | METH_KEYWORDS, MGLBuffer_access_doc},
	{"read", (PyCFunction)MGLBuffer_read, METH_VARARGS | METH_KEYWORDS, MGLBuffer_read_doc},
	{"write", (PyCFunction)MGLBuffer_write, METH_VARARGS | METH_KEYWORDS, MGLBuffer_write_doc},
	{"orphan", (PyCFunction)MGLBuffer_orphan, METH_NOARGS, MGLBuffer_orphan_doc},
	{"bind_to_uniform_block", (PyCFunction)MGLBuffer_bind_to_uniform_block, METH_VARARGS | METH_KEYWORDS, MGLBuffer_bind_to_uniform_block_doc},
	{"bind_to_storage_buffer", (PyCFunction)MGLBuffer_bind_to_storage_buffer, METH_VARARGS | METH_KEYWORDS, MGLBuffer_bind_to_storage_buffer_doc},
	{"release", (PyCFunction)MGLBuffer_release, METH_NOARGS, MGLBuffer_release_doc},
	{0},
};

PyObject * MGLBuffer_get_size(MGLBuffer * self, void * closure) {
	return PyLong_FromLong(self->size);
}

char MGLBuffer_size_doc[] = R"(
	size

	The size of the buffer.
)";

PyObject * MGLBuffer_get_dynamic(MGLBuffer * self, void * closure) {
	return PyBool_FromLong(self->dynamic);
}

char MGLBuffer_dynamic_doc[] = R"(
	dynamic
)";

PyGetSetDef MGLBuffer_tp_getseters[] = {
	{(char *)"size", (getter)MGLBuffer_get_size, 0, MGLBuffer_size_doc, 0},
	{(char *)"dynamic", (getter)MGLBuffer_get_dynamic, 0, MGLBuffer_dynamic_doc, 0},
	{0},
};

int MGLBuffer_tp_as_buffer_get_view(MGLBuffer * self, Py_buffer * view, int flags) {
	int access = (flags == PyBUF_SIMPLE) ? GL_MAP_READ_BIT : (GL_MAP_READ_BIT | GL_MAP_WRITE_BIT);

	const GLMethods & gl = self->context->gl;
	gl.BindBuffer(GL_ARRAY_BUFFER, self->buffer_obj);
	void * map = gl.MapBufferRange(GL_ARRAY_BUFFER, 0, self->size, access);

	if (!map) {
		PyErr_Format(PyExc_BufferError, "Cannot map buffer");
		view->obj = 0;
		return -1;
	}

	view->buf = map;
	view->len = self->size;
	view->itemsize = 1;

	view->format = 0;
	view->ndim = 0;
	view->shape = 0;
	view->strides = 0;
	view->suboffsets = 0;

	Py_INCREF(self);
	view->obj = (PyObject *)self;
	return 0;
}

void MGLBuffer_tp_as_buffer_release_view(MGLBuffer * self, Py_buffer * view) {
	const GLMethods & gl = self->context->gl;
	gl.BindBuffer(GL_ARRAY_BUFFER, self->buffer_obj);
	gl.UnmapBuffer(GL_ARRAY_BUFFER);
}

PyBufferProcs MGLBuffer_tp_as_buffer = {
	PyBufferProcs_PADDING
	(getbufferproc)MGLBuffer_tp_as_buffer_get_view,                  // getbufferproc bf_getbuffer
	(releasebufferproc)MGLBuffer_tp_as_buffer_release_view,          // releasebufferproc bf_releasebuffer
};

const char * MGLBuffer_tp_doc = R"(
	Buffer

	Create a :py:class:`~ModernGL.Buffer` using :py:meth:`~ModernGL.Context.Buffer`.
)";

PyTypeObject MGLBuffer_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Buffer",                                      // tp_name
	sizeof(MGLBuffer),                                      // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLBuffer_tp_dealloc,                       // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLBuffer_tp_str,                             // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLBuffer_tp_str,                             // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	&MGLBuffer_tp_as_buffer,                                // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLBuffer_tp_doc,                                       // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLBuffer_tp_methods,                                   // tp_methods
	0,                                                      // tp_members
	MGLBuffer_tp_getseters,                                 // tp_getset
	&MGLContextMember_Type,                                 // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLBuffer_tp_init,                            // tp_init
	0,                                                      // tp_alloc
	MGLBuffer_tp_new,                                       // tp_new
};

MGLBuffer * MGLBuffer_New() {
	MGLBuffer * self = (MGLBuffer *)MGLBuffer_tp_new(&MGLBuffer_Type, 0, 0);
	return self;
}

void MGLBuffer_Invalidate(MGLBuffer * buffer) {
	if (Py_TYPE(buffer) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLBuffer_Invalidate %p already released\n", buffer);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLBuffer_Invalidate %p\n", buffer);
	#endif

	const GLMethods & gl = buffer->context->gl;
	gl.DeleteBuffers(1, (GLuint *)&buffer->buffer_obj);

	Py_DECREF(buffer->context);

	Py_TYPE(buffer) = &MGLInvalidObject_Type;

	Py_DECREF(buffer);
}
