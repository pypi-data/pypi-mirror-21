#include "Attribute.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

PyObject * MGLAttribute_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLAttribute * self = (MGLAttribute *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLAttribute_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLAttribute_tp_dealloc(MGLAttribute * self) {

	#ifdef MGL_VERBOSE
	printf("MGLAttribute_tp_dealloc %p\n", self);
	#endif

	MGLAttribute_Type.tp_free((PyObject *)self);
}

int MGLAttribute_tp_init(MGLAttribute * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_New(TRACE, "Cannot create ModernGL.Attribute manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLAttribute_tp_str(MGLAttribute * self) {
	return PyUnicode_FromFormat("<ModernGL.Attribute>");
}

PyMethodDef MGLAttribute_tp_methods[] = {
	{0},
};

PyObject * MGLAttribute_get_name(MGLAttribute * self, void * closure) {
	Py_INCREF(self->name);
	return self->name;
}

char MGLAttribute_name_doc[] = R"(
	name

	The attribute name.
	The name will be filtered to have no array syntax on it's end.
	Attribute name without ``'[0]'`` ending if any.
)";

PyObject * MGLAttribute_get_location(MGLAttribute * self, void * closure) {
	return PyLong_FromLong(self->location);
}

char MGLAttribute_location_doc[] = R"(
	location

	The attribute location.
	The result of the glGetAttribLocation.
)";

PyObject * MGLAttribute_get_array_length(MGLAttribute * self, void * closure) {
	return PyLong_FromLong(self->array_length);
}

char MGLAttribute_array_length_doc[] = R"(
	array_length

	If the attribute is an array the array_length is the length of the array otherwise it is ``1``.
)";

PyObject * MGLAttribute_get_dimension(MGLAttribute * self, void * closure) {
	return PyLong_FromLong(self->dimension);
}

char MGLAttribute_dimension_doc[] = R"(
	dimension

	The attribute dimension.

	+-----------+-----------+
	| GLSL type | dimension |
	+===========+===========+
	| int       | 1         |
	+-----------+-----------+
	| ivec2     | 2         |
	+-----------+-----------+
	| ivec3     | 3         |
	+-----------+-----------+
	| ivec4     | 4         |
	+-----------+-----------+
	| uint      | 1         |
	+-----------+-----------+
	| uvec2     | 2         |
	+-----------+-----------+
	| uvec3     | 3         |
	+-----------+-----------+
	| uvec4     | 4         |
	+-----------+-----------+
	| float     | 1         |
	+-----------+-----------+
	| vec2      | 2         |
	+-----------+-----------+
	| vec3      | 3         |
	+-----------+-----------+
	| vec4      | 4         |
	+-----------+-----------+
	| double    | 1         |
	+-----------+-----------+
	| dvec2     | 2         |
	+-----------+-----------+
	| dvec3     | 3         |
	+-----------+-----------+
	| dvec4     | 4         |
	+-----------+-----------+
	| mat2      | 4         |
	+-----------+-----------+
	| mat2x3    | 6         |
	+-----------+-----------+
	| mat2x4    | 8         |
	+-----------+-----------+
	| mat3x2    | 6         |
	+-----------+-----------+
	| mat3      | 9         |
	+-----------+-----------+
	| mat3x4    | 12        |
	+-----------+-----------+
	| mat4x2    | 8         |
	+-----------+-----------+
	| mat4x3    | 12        |
	+-----------+-----------+
	| mat4      | 16        |
	+-----------+-----------+
	| dmat2     | 4         |
	+-----------+-----------+
	| dmat2x3   | 6         |
	+-----------+-----------+
	| dmat2x4   | 8         |
	+-----------+-----------+
	| dmat3x2   | 6         |
	+-----------+-----------+
	| dmat3     | 9         |
	+-----------+-----------+
	| dmat3x4   | 12        |
	+-----------+-----------+
	| dmat4x2   | 8         |
	+-----------+-----------+
	| dmat4x3   | 12        |
	+-----------+-----------+
	| dmat4     | 16        |
	+-----------+-----------+
)";

PyObject * MGLAttribute_get_shape(MGLAttribute * self, void * closure) {
	return PyUnicode_FromFormat("%c", self->shape);
}

char MGLAttribute_shape_doc[] = R"(
	shape

	The shape is a single character that represents the scalar type of the attriute.

	+---------+--------------------------+
	| shape   | GLSL types               |
	+=========+==========================+
	| ``'i'`` | int                      |
	|         +--------------------------+
	|         | ivec2 ivec3 ivec4        |
	+---------+--------------------------+
	| ``'I'`` | uint                     |
	|         +--------------------------+
	|         | uvec2 uvec3 uvec4        |
	+---------+--------------------------+
	| ``'f'`` | float                    |
	|         +--------------------------+
	|         | vec2 vec3 vec4           |
	|         +--------------------------+
	|         | mat2 mat3 mat4           |
	|         +--------------------------+
	|         | mat2x3 mat2x4 mat3x4     |
	|         | mat4x2 mat4x2 mat4x3     |
	+---------+--------------------------+
	| ``'d'`` | double                   |
	|         +--------------------------+
	|         | dvec2 dvec3 dvec4        |
	|         +--------------------------+
	|         | dmat2 dmat3 dmat4        |
	|         +--------------------------+
	|         | dmat2x3 dmat2x4 dmat3x4  |
	|         | dmat4x2 dmat4x2 dmat4x3  |
	+---------+--------------------------+
)";

PyGetSetDef MGLAttribute_tp_getseters[] = {
	{(char *)"name", (getter)MGLAttribute_get_name, 0, MGLAttribute_name_doc, 0},
	{(char *)"location", (getter)MGLAttribute_get_location, 0, MGLAttribute_location_doc, 0},
	{(char *)"array_length", (getter)MGLAttribute_get_array_length, 0, MGLAttribute_array_length_doc, 0},
	{(char *)"dimension", (getter)MGLAttribute_get_dimension, 0, MGLAttribute_dimension_doc, 0},
	{(char *)"shape", (getter)MGLAttribute_get_shape, 0, MGLAttribute_shape_doc, 0},
	{0},
};

const char * MGLAttribute_tp_doc = R"(
	Attribute
)";

PyTypeObject MGLAttribute_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Attribute",                                   // tp_name
	sizeof(MGLAttribute),                                   // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLAttribute_tp_dealloc,                    // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLAttribute_tp_str,                          // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLAttribute_tp_str,                          // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	MGLAttribute_tp_doc,                                    // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLAttribute_tp_methods,                                // tp_methods
	0,                                                      // tp_members
	MGLAttribute_tp_getseters,                              // tp_getset
	&MGLProgramMember_Type,                                 // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLAttribute_tp_init,                         // tp_init
	0,                                                      // tp_alloc
	MGLAttribute_tp_new,                                    // tp_new
};

MGLAttribute * MGLAttribute_New() {
	MGLAttribute * self = (MGLAttribute *)MGLAttribute_tp_new(&MGLAttribute_Type, 0, 0);
	return self;
}

void MGLAttribute_Invalidate(MGLAttribute * attribute) {

	#ifdef MGL_VERBOSE
	printf("MGLAttribute_Invalidate %p\n", attribute);
	#endif

	Py_DECREF(attribute->name);

	Py_TYPE(attribute) = &MGLInvalidObject_Type;

	Py_DECREF(attribute);
}

void MGLAttribute_Complete(MGLAttribute * self, const GLMethods & gl) {
	switch (self->type) {
		case GL_INT:
			self->dimension = 1;

			self->scalar_type = GL_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 1;
			self->row_size = 4;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'i';
			break;

		case GL_INT_VEC2:
			self->dimension = 2;

			self->scalar_type = GL_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 2;
			self->row_size = 8;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'i';
			break;

		case GL_INT_VEC3:
			self->dimension = 3;

			self->scalar_type = GL_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 3;
			self->row_size = 12;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'i';
			break;

		case GL_INT_VEC4:
			self->dimension = 4;

			self->scalar_type = GL_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 4;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'i';
			break;

		case GL_UNSIGNED_INT:
			self->dimension = 1;

			self->scalar_type = GL_UNSIGNED_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 1;
			self->row_size = 4;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'I';
			break;

		case GL_UNSIGNED_INT_VEC2:
			self->dimension = 2;

			self->scalar_type = GL_UNSIGNED_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 2;
			self->row_size = 8;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'I';
			break;

		case GL_UNSIGNED_INT_VEC3:
			self->dimension = 3;

			self->scalar_type = GL_UNSIGNED_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 3;
			self->row_size = 12;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'I';
			break;

		case GL_UNSIGNED_INT_VEC4:
			self->dimension = 4;

			self->scalar_type = GL_UNSIGNED_INT;

			self->rows_length = self->array_length * 1;
			self->row_length = 4;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribIPointer;

			self->normalizable = false;
			self->shape = 'I';
			break;

		case GL_FLOAT:
			self->dimension = 1;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 1;
			self->row_length = 1;
			self->row_size = 4;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_VEC2:
			self->dimension = 2;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 1;
			self->row_length = 2;
			self->row_size = 8;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_VEC3:
			self->dimension = 3;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 1;
			self->row_length = 3;
			self->row_size = 12;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_VEC4:
			self->dimension = 4;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 1;
			self->row_length = 4;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_DOUBLE:
			self->dimension = 1;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 1;
			self->row_length = 1;
			self->row_size = 8;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_VEC2:
			self->dimension = 2;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 1;
			self->row_length = 2;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_VEC3:
			self->dimension = 3;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 1;
			self->row_length = 3;
			self->row_size = 24;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_VEC4:
			self->dimension = 4;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 1;
			self->row_length = 4;
			self->row_size = 32;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_FLOAT_MAT2:
			self->dimension = 4;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 2;
			self->row_length = 2;
			self->row_size = 8;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT2x3:
			self->dimension = 6;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 2;
			self->row_length = 3;
			self->row_size = 12;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT2x4:
			self->dimension = 8;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 2;
			self->row_length = 4;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT3x2:
			self->dimension = 6;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 3;
			self->row_length = 2;
			self->row_size = 8;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT3:
			self->dimension = 9;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 3;
			self->row_length = 3;
			self->row_size = 12;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT3x4:
			self->dimension = 12;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 3;
			self->row_length = 4;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT4x2:
			self->dimension = 8;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 4;
			self->row_length = 2;
			self->row_size = 8;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT4x3:
			self->dimension = 12;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 4;
			self->row_length = 3;
			self->row_size = 12;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_FLOAT_MAT4:
			self->dimension = 16;

			self->scalar_type = GL_FLOAT;

			self->rows_length = self->array_length * 4;
			self->row_length = 4;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribPointer;

			self->normalizable = true;
			self->shape = 'f';
			break;

		case GL_DOUBLE_MAT2:
			self->dimension = 4;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 2;
			self->row_length = 2;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT2x3:
			self->dimension = 6;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 2;
			self->row_length = 3;
			self->row_size = 24;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT2x4:
			self->dimension = 8;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 2;
			self->row_length = 4;
			self->row_size = 32;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT3x2:
			self->dimension = 6;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 3;
			self->row_length = 2;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT3:
			self->dimension = 9;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 3;
			self->row_length = 3;
			self->row_size = 24;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT3x4:
			self->dimension = 12;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 3;
			self->row_length = 4;
			self->row_size = 32;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT4x2:
			self->dimension = 8;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 4;
			self->row_length = 2;
			self->row_size = 16;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT4x3:
			self->dimension = 12;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 4;
			self->row_length = 3;
			self->row_size = 24;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		case GL_DOUBLE_MAT4:
			self->dimension = 16;

			self->scalar_type = GL_DOUBLE;

			self->rows_length = self->array_length * 4;
			self->row_length = 4;
			self->row_size = 32;

			self->gl_attrib_ptr_proc = (void *)gl.VertexAttribLPointer;

			self->normalizable = false;
			self->shape = 'd';
			break;

		default:
			self->dimension = 1;

			self->scalar_type = 0;

			self->rows_length = self->array_length * 1;
			self->row_length = 1;
			self->row_size = 4;

			self->gl_attrib_ptr_proc = 0;

			self->normalizable = false;
			self->shape = 0;
			break;
	}
}
