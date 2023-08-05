#include "Uniform.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

PyObject * MGLUniform_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLUniform * self = (MGLUniform *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLUniform_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLUniform_tp_dealloc(MGLUniform * self) {

	#ifdef MGL_VERBOSE
	printf("MGLUniform_tp_dealloc %p\n", self);
	#endif

	MGLUniform_Type.tp_free((PyObject *)self);
}

int MGLUniform_tp_init(MGLUniform * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Uniform manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLUniform_tp_str(MGLUniform * self) {
	return PyUnicode_FromFormat("<ModernGL.Uniform>");
}

PyObject * MGLUniform_read(MGLUniform * self) {
	PyObject * result = PyBytes_FromStringAndSize(0, self->element_size);

	// TODO: remove
	if (!self->gl_value_reader_proc) {
		MGLError * error = MGLError_New(TRACE, "gl_value_reader_proc is null in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, PyBytes_AS_STRING(result));
	return result;
}

const char * MGLUniform_read_doc = R"(
	read()

	Read the uniform value as binary data.

	Returns:
		``bytes``
)";

PyObject * MGLUniform_write(MGLUniform * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"data", 0};

	const char * buffer;
	int size;

	int args_ok = PyArg_ParseTupleAndKeywords(
		args,
		kwargs,
		"y#",
		(char **)kwlist,
		&buffer,
		&size
	);

	if (!args_ok) {
		return 0;
	}

	// TODO: remove
	if (!self->gl_value_writer_proc) {
		MGLError * error = MGLError_New(TRACE, "gl_value_writer_proc is null in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	if (size != self->array_length * self->element_size) {
		MGLError * error = MGLError_New(TRACE, "data size mismatch %d != %d", size, self->array_length * self->element_size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	if (self->matrix) {
		((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, self->array_length, false, buffer);
	} else {
		((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, self->array_length, buffer);
	}

	Py_RETURN_NONE;
}

const char * MGLUniform_write_doc = R"(
	write()

	Write the uniform value as binary data.

	Args:
		data: Data to write.

	Returns:
		``None``
)";

PyMethodDef MGLUniform_tp_methods[] = {
	{"read", (PyCFunction)MGLUniform_read, METH_NOARGS, MGLUniform_read_doc},
	{"write", (PyCFunction)MGLUniform_write, METH_VARARGS | METH_KEYWORDS, MGLUniform_write_doc},
	{0},
};

PyObject * MGLUniform_get_name(MGLUniform * self, void * closure) {
	Py_INCREF(self->name);
	return self->name;
}

char MGLUniform_name_doc[] = R"(
	name
)";

PyObject * MGLUniform_get_location(MGLUniform * self, void * closure) {
	return PyLong_FromLong(self->location);
}

char MGLUniform_location_doc[] = R"(
	location
)";

PyObject * MGLUniform_get_dimension(MGLUniform * self, void * closure) {
	return PyLong_FromLong(self->dimension);
}

char MGLUniform_dimension_doc[] = R"(
	dimension

	The uniform dimension.

	+-----------------+-----------+
	| GLSL type       | dimension |
	+=================+===========+
	| sampler2D       | 1         |
	+-----------------+-----------+
	| sampler2DCube   | 1         |
	+-----------------+-----------+
	| sampler2DShadow | 1         |
	+-----------------+-----------+
	| bool            | 1         |
	+-----------------+-----------+
	| bvec2           | 2         |
	+-----------------+-----------+
	| bvec3           | 3         |
	+-----------------+-----------+
	| bvec4           | 4         |
	+-----------------+-----------+
	| int             | 1         |
	+-----------------+-----------+
	| ivec2           | 2         |
	+-----------------+-----------+
	| ivec3           | 3         |
	+-----------------+-----------+
	| ivec4           | 4         |
	+-----------------+-----------+
	| uint            | 1         |
	+-----------------+-----------+
	| uvec2           | 2         |
	+-----------------+-----------+
	| uvec3           | 3         |
	+-----------------+-----------+
	| uvec4           | 4         |
	+-----------------+-----------+
	| float           | 1         |
	+-----------------+-----------+
	| vec2            | 2         |
	+-----------------+-----------+
	| vec3            | 3         |
	+-----------------+-----------+
	| vec4            | 4         |
	+-----------------+-----------+
	| double          | 1         |
	+-----------------+-----------+
	| dvec2           | 2         |
	+-----------------+-----------+
	| dvec3           | 3         |
	+-----------------+-----------+
	| dvec4           | 4         |
	+-----------------+-----------+
	| mat2            | 4         |
	+-----------------+-----------+
	| mat2x3          | 6         |
	+-----------------+-----------+
	| mat2x4          | 8         |
	+-----------------+-----------+
	| mat3x2          | 6         |
	+-----------------+-----------+
	| mat3            | 9         |
	+-----------------+-----------+
	| mat3x4          | 12        |
	+-----------------+-----------+
	| mat4x2          | 8         |
	+-----------------+-----------+
	| mat4x3          | 12        |
	+-----------------+-----------+
	| mat4            | 16        |
	+-----------------+-----------+
	| dmat2           | 4         |
	+-----------------+-----------+
	| dmat2x3         | 6         |
	+-----------------+-----------+
	| dmat2x4         | 8         |
	+-----------------+-----------+
	| dmat3x2         | 6         |
	+-----------------+-----------+
	| dmat3           | 9         |
	+-----------------+-----------+
	| dmat3x4         | 12        |
	+-----------------+-----------+
	| dmat4x2         | 8         |
	+-----------------+-----------+
	| dmat4x3         | 12        |
	+-----------------+-----------+
	| dmat4           | 16        |
	+-----------------+-----------+
)";

PyObject * MGLUniform_get_value(MGLUniform * self, void * closure) {

	// TODO: remove
	if (!self->value_getter) {
		MGLError * error = MGLError_New(TRACE, "value_getter is null in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	return ((MGLUniform_Getter)self->value_getter)(self);
}

int MGLUniform_set_value(MGLUniform * self, PyObject * value, void * closure) {

	// TODO: remove
	if (!self->value_setter) {
		MGLError * error = MGLError_New(TRACE, "value_setter is null in %s (%s:%d)", __FUNCTION__, __FILE__, __LINE__);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	return ((MGLUniform_Setter)self->value_setter)(self, value);
}

char MGLUniform_value_doc[] = R"(
	value
)";

PyObject * MGLUniform_get_array_length(MGLUniform * self, void * closure) {
	return PyLong_FromLong(self->array_length);
}

char MGLUniform_array_length_doc[] = R"(
	array_length

	If the uniform is an array the array_length is the length of the array otherwise it is ``1``.
)";

PyGetSetDef MGLUniform_tp_getseters[] = {
	{(char *)"name", (getter)MGLUniform_get_name, 0, MGLUniform_name_doc, 0},
	{(char *)"location", (getter)MGLUniform_get_location, 0, MGLUniform_location_doc, 0},
	{(char *)"dimension", (getter)MGLUniform_get_dimension, 0, MGLUniform_dimension_doc, 0},
	{(char *)"value", (getter)MGLUniform_get_value, (setter)MGLUniform_set_value, MGLUniform_value_doc, 0},
	{(char *)"array_length", (getter)MGLUniform_get_array_length, 0, MGLUniform_array_length_doc, 0},
	{0},
};

const char * MGLUniform_tp_doc = R"(
	Uniform
)";

PyTypeObject MGLUniform_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Uniform",                                     // tp_name
	sizeof(MGLUniform),                                     // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLUniform_tp_dealloc,                      // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLUniform_tp_str,                            // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLUniform_tp_str,                            // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLUniform_tp_doc,                                      // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLUniform_tp_methods,                                  // tp_methods
	0,                                                      // tp_members
	MGLUniform_tp_getseters,                                // tp_getset
	&MGLProgramMember_Type,                                 // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLUniform_tp_init,                           // tp_init
	0,                                                      // tp_alloc
	MGLUniform_tp_new,                                      // tp_new
};

MGLUniform * MGLUniform_New() {
	MGLUniform * self = (MGLUniform *)MGLUniform_tp_new(&MGLUniform_Type, 0, 0);
	return self;
}

void MGLUniform_Invalidate(MGLUniform * uniform) {

	#ifdef MGL_VERBOSE
	printf("MGLUniform_Invalidate %p\n", uniform);
	#endif

	Py_DECREF(uniform->name);

	Py_TYPE(uniform) = &MGLInvalidObject_Type;

	Py_DECREF(uniform);
}

void MGLUniform_Complete(MGLUniform * self, const GLMethods & gl) {
	switch (self->type) {
		case GL_BOOL:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_bool_array_value_getter;
				self->value_setter = (void *)MGLUniform_bool_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_bool_value_getter;
				self->value_setter = (void *)MGLUniform_bool_value_setter;
			}
			break;

		case GL_BOOL_VEC2:
			self->matrix = false;
			self->dimension = 2;
			self->element_size = 8;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform2iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_bvec2_array_value_getter;
				self->value_setter = (void *)MGLUniform_bvec2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_bvec2_value_getter;
				self->value_setter = (void *)MGLUniform_bvec2_value_setter;
			}
			break;

		case GL_BOOL_VEC3:
			self->matrix = false;
			self->dimension = 3;
			self->element_size = 12;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform3iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_bvec3_array_value_getter;
				self->value_setter = (void *)MGLUniform_bvec3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_bvec3_value_getter;
				self->value_setter = (void *)MGLUniform_bvec3_value_setter;
			}
			break;

		case GL_BOOL_VEC4:
			self->matrix = false;
			self->dimension = 4;
			self->element_size = 16;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform4iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_bvec4_array_value_getter;
				self->value_setter = (void *)MGLUniform_bvec4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_bvec4_value_getter;
				self->value_setter = (void *)MGLUniform_bvec4_value_setter;
			}
			break;

		case GL_INT:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_int_array_value_getter;
				self->value_setter = (void *)MGLUniform_int_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_int_value_getter;
				self->value_setter = (void *)MGLUniform_int_value_setter;
			}
			break;

		case GL_INT_VEC2:
			self->matrix = false;
			self->dimension = 2;
			self->element_size = 8;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform2iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_ivec2_array_value_getter;
				self->value_setter = (void *)MGLUniform_ivec2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_ivec2_value_getter;
				self->value_setter = (void *)MGLUniform_ivec2_value_setter;
			}
			break;

		case GL_INT_VEC3:
			self->matrix = false;
			self->dimension = 3;
			self->element_size = 12;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform3iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_ivec3_array_value_getter;
				self->value_setter = (void *)MGLUniform_ivec3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_ivec3_value_getter;
				self->value_setter = (void *)MGLUniform_ivec3_value_setter;
			}
			break;

		case GL_INT_VEC4:
			self->matrix = false;
			self->dimension = 4;
			self->element_size = 16;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform4iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_ivec4_array_value_getter;
				self->value_setter = (void *)MGLUniform_ivec4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_ivec4_value_getter;
				self->value_setter = (void *)MGLUniform_ivec4_value_setter;
			}
			break;

		case GL_UNSIGNED_INT:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformuiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1uiv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_uint_array_value_getter;
				self->value_setter = (void *)MGLUniform_uint_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_uint_value_getter;
				self->value_setter = (void *)MGLUniform_uint_value_setter;
			}
			break;

		case GL_UNSIGNED_INT_VEC2:
			self->matrix = false;
			self->dimension = 2;
			self->element_size = 8;
			self->gl_value_reader_proc = (void *)gl.GetUniformuiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform2uiv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_uvec2_array_value_getter;
				self->value_setter = (void *)MGLUniform_uvec2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_uvec2_value_getter;
				self->value_setter = (void *)MGLUniform_uvec2_value_setter;
			}
			break;

		case GL_UNSIGNED_INT_VEC3:
			self->matrix = false;
			self->dimension = 3;
			self->element_size = 12;
			self->gl_value_reader_proc = (void *)gl.GetUniformuiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform3uiv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_uvec3_array_value_getter;
				self->value_setter = (void *)MGLUniform_uvec3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_uvec3_value_getter;
				self->value_setter = (void *)MGLUniform_uvec3_value_setter;
			}
			break;

		case GL_UNSIGNED_INT_VEC4:
			self->matrix = false;
			self->dimension = 4;
			self->element_size = 16;
			self->gl_value_reader_proc = (void *)gl.GetUniformuiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform4uiv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_uvec4_array_value_getter;
				self->value_setter = (void *)MGLUniform_uvec4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_uvec4_value_getter;
				self->value_setter = (void *)MGLUniform_uvec4_value_setter;
			}
			break;

		case GL_FLOAT:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_value_getter;
				self->value_setter = (void *)MGLUniform_float_value_setter;
			}
			break;

		case GL_FLOAT_VEC2:
			self->matrix = false;
			self->dimension = 2;
			self->element_size = 8;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform2fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_vec2_array_value_getter;
				self->value_setter = (void *)MGLUniform_vec2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_vec2_value_getter;
				self->value_setter = (void *)MGLUniform_vec2_value_setter;
			}
			break;

		case GL_FLOAT_VEC3:
			self->matrix = false;
			self->dimension = 3;
			self->element_size = 12;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform3fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_vec3_array_value_getter;
				self->value_setter = (void *)MGLUniform_vec3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_vec3_value_getter;
				self->value_setter = (void *)MGLUniform_vec3_value_setter;
			}
			break;

		case GL_FLOAT_VEC4:
			self->matrix = false;
			self->dimension = 4;
			self->element_size = 16;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform4fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_vec4_array_value_getter;
				self->value_setter = (void *)MGLUniform_vec4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_vec4_value_getter;
				self->value_setter = (void *)MGLUniform_vec4_value_setter;
			}
			break;

		case GL_DOUBLE:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 8;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_value_getter;
				self->value_setter = (void *)MGLUniform_double_value_setter;
			}
			break;

		case GL_DOUBLE_VEC2:
			self->matrix = false;
			self->dimension = 2;
			self->element_size = 16;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform2dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_dvec2_array_value_getter;
				self->value_setter = (void *)MGLUniform_dvec2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_dvec2_value_getter;
				self->value_setter = (void *)MGLUniform_dvec2_value_setter;
			}
			break;

		case GL_DOUBLE_VEC3:
			self->matrix = false;
			self->dimension = 3;
			self->element_size = 24;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform3dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_dvec3_array_value_getter;
				self->value_setter = (void *)MGLUniform_dvec3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_dvec3_value_getter;
				self->value_setter = (void *)MGLUniform_dvec3_value_setter;
			}
			break;

		case GL_DOUBLE_VEC4:
			self->matrix = false;
			self->dimension = 4;
			self->element_size = 32;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform4dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_dvec4_array_value_getter;
				self->value_setter = (void *)MGLUniform_dvec4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_dvec4_value_getter;
				self->value_setter = (void *)MGLUniform_dvec4_value_setter;
			}
			break;

		case GL_SAMPLER_2D:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_sampler_array_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_sampler_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_value_setter;
			}
			break;

		case GL_SAMPLER_2D_SHADOW:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_sampler_array_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_sampler_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_value_setter;
			}
			break;

		case GL_SAMPLER_2D_MULTISAMPLE:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_sampler_array_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_sampler_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_value_setter;
			}
			break;

		case GL_SAMPLER_CUBE:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = (void *)gl.GetUniformiv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniform1iv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_sampler_array_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_sampler_value_getter;
				self->value_setter = (void *)MGLUniform_sampler_value_setter;
			}
			break;

		case GL_FLOAT_MAT2:
			self->matrix = true;
			self->dimension = 4;
			self->element_size = 16;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix2fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_2x2_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_2x2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_2x2_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_2x2_value_setter;
			}
			break;

		case GL_FLOAT_MAT2x3:
			self->matrix = true;
			self->dimension = 6;
			self->element_size = 24;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix2x3fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_2x3_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_2x3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_2x3_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_2x3_value_setter;
			}
			break;

		case GL_FLOAT_MAT2x4:
			self->matrix = true;
			self->dimension = 8;
			self->element_size = 32;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix2x4fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_2x4_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_2x4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_2x4_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_2x4_value_setter;
			}
			break;

		case GL_FLOAT_MAT3x2:
			self->matrix = true;
			self->dimension = 6;
			self->element_size = 24;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix3x2fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_3x2_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_3x2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_3x2_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_3x2_value_setter;
			}
			break;

		case GL_FLOAT_MAT3:
			self->matrix = true;
			self->dimension = 9;
			self->element_size = 36;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix3fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_3x3_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_3x3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_3x3_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_3x3_value_setter;
			}
			break;

		case GL_FLOAT_MAT3x4:
			self->matrix = true;
			self->dimension = 12;
			self->element_size = 48;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix3x4fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_3x4_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_3x4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_3x4_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_3x4_value_setter;
			}
			break;

		case GL_FLOAT_MAT4x2:
			self->matrix = true;
			self->dimension = 8;
			self->element_size = 32;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix4x2fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_4x2_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_4x2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_4x2_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_4x2_value_setter;
			}
			break;

		case GL_FLOAT_MAT4x3:
			self->matrix = true;
			self->dimension = 12;
			self->element_size = 48;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix4x3fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_4x3_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_4x3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_4x3_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_4x3_value_setter;
			}
			break;

		case GL_FLOAT_MAT4:
			self->matrix = true;
			self->dimension = 16;
			self->element_size = 64;
			self->gl_value_reader_proc = (void *)gl.GetUniformfv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix4fv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_float_matrix_4x4_array_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_4x4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_float_matrix_4x4_value_getter;
				self->value_setter = (void *)MGLUniform_float_matrix_4x4_value_setter;
			}
			break;

		case GL_DOUBLE_MAT2:
			self->matrix = true;
			self->dimension = 4;
			self->element_size = 32;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix2dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_2x2_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_2x2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_2x2_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_2x2_value_setter;
			}
			break;

		case GL_DOUBLE_MAT2x3:
			self->matrix = true;
			self->dimension = 6;
			self->element_size = 48;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix2x3dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_2x3_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_2x3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_2x3_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_2x3_value_setter;
			}
			break;

		case GL_DOUBLE_MAT2x4:
			self->matrix = true;
			self->dimension = 8;
			self->element_size = 64;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix2x4dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_2x4_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_2x4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_2x4_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_2x4_value_setter;
			}
			break;

		case GL_DOUBLE_MAT3x2:
			self->matrix = true;
			self->dimension = 6;
			self->element_size = 48;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix3x2dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_3x2_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_3x2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_3x2_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_3x2_value_setter;
			}
			break;

		case GL_DOUBLE_MAT3:
			self->matrix = true;
			self->dimension = 9;
			self->element_size = 72;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix3dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_3x3_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_3x3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_3x3_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_3x3_value_setter;
			}
			break;

		case GL_DOUBLE_MAT3x4:
			self->matrix = true;
			self->dimension = 12;
			self->element_size = 96;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix3x4dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_3x4_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_3x4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_3x4_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_3x4_value_setter;
			}
			break;

		case GL_DOUBLE_MAT4x2:
			self->matrix = true;
			self->dimension = 8;
			self->element_size = 64;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix4x2dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_4x2_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_4x2_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_4x2_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_4x2_value_setter;
			}
			break;

		case GL_DOUBLE_MAT4x3:
			self->matrix = true;
			self->dimension = 12;
			self->element_size = 96;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix4x3dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_4x3_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_4x3_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_4x3_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_4x3_value_setter;
			}
			break;

		case GL_DOUBLE_MAT4:
			self->matrix = true;
			self->dimension = 16;
			self->element_size = 128;
			self->gl_value_reader_proc = (void *)gl.GetUniformdv;
			self->gl_value_writer_proc = (void *)gl.ProgramUniformMatrix4dv;
			if (self->array_length > 1) {
				self->value_getter = (void *)MGLUniform_double_matrix_4x4_array_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_4x4_array_value_setter;
			} else {
				self->value_getter = (void *)MGLUniform_double_matrix_4x4_value_getter;
				self->value_setter = (void *)MGLUniform_double_matrix_4x4_value_setter;
			}
			break;

		default:
			self->matrix = false;
			self->dimension = 1;
			self->element_size = 4;
			self->gl_value_reader_proc = 0;
			self->gl_value_writer_proc = 0;
			self->value_getter = (void *)MGLUniform_invalid_getter;
			self->value_setter = (void *)MGLUniform_invalid_setter;
			break;
	}
}
