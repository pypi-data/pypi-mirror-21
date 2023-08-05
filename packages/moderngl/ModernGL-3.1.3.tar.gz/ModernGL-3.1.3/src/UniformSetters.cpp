#include "Uniform.hpp"

#include "Error.hpp"

int MGLUniform_invalid_setter(MGLUniform * self, PyObject * value) {
	MGLError * error = MGLError_New(TRACE, "Cannot detect uniform type");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

int MGLUniform_bool_value_setter(MGLUniform * self, PyObject * value) {
	int c_value;

	if (value == Py_True) {
		c_value = 1;
	} else if (value == Py_False) {
		c_value = 0;
	} else {
		MGLError * error = MGLError_New(TRACE, "value must be a bool not %s", Py_TYPE(value)->tp_name);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, &c_value);

	return 0;
}

int MGLUniform_bvec2_value_setter(MGLUniform * self, PyObject * value) {
	int c_values[2];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 2) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 2; ++i) {
		PyObject * v = PyTuple_GET_ITEM(value, i);

		if (v == Py_True) {
			c_values[i] = 1;
		} else if (v == Py_False) {
			c_values[i] = 0;
		} else {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a bool not %s", i, Py_TYPE(value)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return -1;
		}
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_bvec3_value_setter(MGLUniform * self, PyObject * value) {
	int c_values[3];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 3) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 3; ++i) {
		PyObject * v = PyTuple_GET_ITEM(value, i);

		if (v == Py_True) {
			c_values[i] = 1;
		} else if (v == Py_False) {
			c_values[i] = 0;
		} else {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a bool not %s", i, Py_TYPE(value)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return -1;
		}
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_bvec4_value_setter(MGLUniform * self, PyObject * value) {
	int c_values[4];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 4) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 4; ++i) {
		PyObject * v = PyTuple_GET_ITEM(value, i);

		if (v == Py_True) {
			c_values[i] = 1;
		} else if (v == Py_False) {
			c_values[i] = 0;
		} else {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a bool not %s", i, Py_TYPE(value)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return -1;
		}
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_int_value_setter(MGLUniform * self, PyObject * value) {
	int c_value = PyLong_AsLong(value);

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, &c_value);

	return 0;
}

int MGLUniform_ivec2_value_setter(MGLUniform * self, PyObject * value) {
	int c_values[2];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 2) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 2; ++i) {
		c_values[i] = PyLong_AsLong(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_ivec3_value_setter(MGLUniform * self, PyObject * value) {
	int c_values[3];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 3) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 3; ++i) {
		c_values[i] = PyLong_AsLong(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_ivec4_value_setter(MGLUniform * self, PyObject * value) {
	int c_values[4];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 4) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 4; ++i) {
		c_values[i] = PyLong_AsLong(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_uint_value_setter(MGLUniform * self, PyObject * value) {
	unsigned c_value = PyLong_AsUnsignedLong(value);

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "value must be an unsigned int not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, &c_value);

	return 0;
}

int MGLUniform_uvec2_value_setter(MGLUniform * self, PyObject * value) {
	unsigned c_values[2];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 2) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 2; ++i) {
		c_values[i] = PyLong_AsUnsignedLong(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to unsigned int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_uvec3_value_setter(MGLUniform * self, PyObject * value) {
	unsigned c_values[3];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 3) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 3; ++i) {
		c_values[i] = PyLong_AsUnsignedLong(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to unsigned int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_uvec4_value_setter(MGLUniform * self, PyObject * value) {
	unsigned c_values[4];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 4) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 4; ++i) {
		c_values[i] = PyLong_AsUnsignedLong(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to unsigned int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_float_value_setter(MGLUniform * self, PyObject * value) {
	float c_value = (float)PyFloat_AsDouble(value);

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, &c_value);

	return 0;
}

int MGLUniform_vec2_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[2];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 2) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 2; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_vec3_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[3];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 3) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 3; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_vec4_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[4];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 4) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 4; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_double_value_setter(MGLUniform * self, PyObject * value) {
	double c_value = PyFloat_AsDouble(value);

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, &c_value);

	return 0;
}

int MGLUniform_dvec2_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[2];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 2) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 2; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_dvec3_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[3];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 3) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 3; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_dvec4_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[4];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 4) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 4; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, c_values);

	return 0;
}

int MGLUniform_sampler_value_setter(MGLUniform * self, PyObject * value) {
	int c_value = PyLong_AsLong(value);

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, &c_value);

	return 0;
}

int MGLUniform_float_matrix_2x2_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[4];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 4) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 4; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_2x3_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[6];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 6) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 6; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_2x4_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[8];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 8) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 8; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_3x2_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[6];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 6) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 6; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_3x3_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[9];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 9) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 9; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_3x4_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[12];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 12) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 12; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_4x2_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[8];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 8) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 8; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_4x3_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[12];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 12) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 12; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_float_matrix_4x4_value_setter(MGLUniform * self, PyObject * value) {
	float c_values[16];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 16) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 16; ++i) {
		c_values[i] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_2x2_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[4];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 4) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 4; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_2x3_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[6];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 6) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 6; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_2x4_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[8];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 8) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 8; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_3x2_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[6];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 6) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 6; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_3x3_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[9];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 9) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 9; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_3x4_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[12];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 12) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 12; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_4x2_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[8];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 8) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 8; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_4x3_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[12];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 12) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 12; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_double_matrix_4x4_value_setter(MGLUniform * self, PyObject * value) {
	double c_values[16];

	if (Py_TYPE(value) != &PyTuple_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyTuple_GET_SIZE(value);

	if (size != 16) {
		MGLError * error = MGLError_New(TRACE, "value must be a tuple of size 2 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	for (int i = 0; i < 16; ++i) {
		c_values[i] = PyFloat_AsDouble(PyTuple_GET_ITEM(value, i));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, 1, false, c_values);

	return 0;
}

int MGLUniform_bool_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int * c_values = new int[size];

	for (int k = 0; k < size; ++k) {
		PyObject * v = PyList_GET_ITEM(value, k);

		if (v == Py_True) {
			c_values[k] = 1;
		} else if (v == Py_False) {
			c_values[k] = 0;
		} else {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a bool not %s", k, Py_TYPE(value)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_bvec2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	int * c_values = new int[size * 2];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 2) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 2 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 2; ++i) {
			PyObject * v = PyTuple_GET_ITEM(tuple, i);

			if (v == Py_True) {
				c_values[cnt++] = 1;
			} else if (v == Py_False) {
				c_values[cnt++] = 0;
			} else {
				MGLError * error = MGLError_New(TRACE, "value[%d][%d] must be a bool not %s", k, i, Py_TYPE(value)->tp_name);
				PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
				delete[] c_values;
				return -1;
			}
		}
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 2, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_bvec3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	int * c_values = new int[size * 3];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 3) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 3 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 3; ++i) {
			PyObject * v = PyTuple_GET_ITEM(tuple, i);

			if (v == Py_True) {
				c_values[cnt++] = 1;
			} else if (v == Py_False) {
				c_values[cnt++] = 0;
			} else {
				MGLError * error = MGLError_New(TRACE, "value[%d][%d] must be a bool not %s", k, i, Py_TYPE(value)->tp_name);
				PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
				delete[] c_values;
				return -1;
			}
		}
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 3, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_bvec4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	int * c_values = new int[size * 4];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 4) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 4 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 4; ++i) {
			PyObject * v = PyTuple_GET_ITEM(tuple, i);

			if (v == Py_True) {
				c_values[cnt++] = 1;
			} else if (v == Py_False) {
				c_values[cnt++] = 0;
			} else {
				MGLError * error = MGLError_New(TRACE, "value[%d][%d] must be a bool not %s", k, i, Py_TYPE(value)->tp_name);
				PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
				delete[] c_values;
				return -1;
			}
		}
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 4, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_int_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int * c_values = new int[size];

	for (int k = 0; k < size; ++k) {
		c_values[k] = PyLong_AsLong(PyList_GET_ITEM(value, k));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_ivec2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	int * c_values = new int[size * 2];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 2) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 2 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 2; ++i) {
			c_values[cnt++] = PyLong_AsLong(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 2, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_ivec3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	int * c_values = new int[size * 3];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 3) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 3 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 3; ++i) {
			c_values[cnt++] = PyLong_AsLong(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 3, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_ivec4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	int * c_values = new int[size * 4];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 4) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 4 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 4; ++i) {
			c_values[cnt++] = PyLong_AsLong(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 4, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_uint_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	unsigned * c_values = new unsigned[size];

	for (int k = 0; k < size; ++k) {
		c_values[k] = PyLong_AsUnsignedLong(PyList_GET_ITEM(value, k));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to unsigned int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_uvec2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	unsigned * c_values = new unsigned[size * 2];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 2) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 2 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 2; ++i) {
			c_values[cnt++] = PyLong_AsUnsignedLong(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to unsigned int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 2, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_uvec3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	unsigned * c_values = new unsigned[size * 3];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 3) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 3 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 3; ++i) {
			c_values[cnt++] = PyLong_AsUnsignedLong(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to unsigned int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 3, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_uvec4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	unsigned * c_values = new unsigned[size * 4];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 4) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 4 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 4; ++i) {
			c_values[cnt++] = PyLong_AsUnsignedLong(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to unsigned int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 4, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	float * c_values = new float[size];

	for (int k = 0; k < size; ++k) {
		c_values[k] = (float)PyFloat_AsDouble(PyList_GET_ITEM(value, k));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_vec2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 2];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 2) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 2 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 2; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 2, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_vec3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 3];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 3) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 3 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 3; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 3, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_vec4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 4];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 4) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 4 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 4; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 4, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	double * c_values = new double[size];

	for (int k = 0; k < size; ++k) {
		c_values[k] = PyFloat_AsDouble(PyList_GET_ITEM(value, k));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_dvec2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 2];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 2) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 2 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 2; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 2, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_dvec3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 3];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 3) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 3 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 3; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 3, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_dvec4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 4];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 4) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 4 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 4; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size * 4, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_sampler_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int * c_values = new int[size];

	for (int k = 0; k < size; ++k) {
		c_values[k] = PyLong_AsLong(PyList_GET_ITEM(value, k));
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to int");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_vector_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_2x2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 4];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 4) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 4 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 4; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_2x3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 6];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 6) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 6 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 6; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_2x4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 8];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 8) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 8 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 8; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_3x2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 6];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 6) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 6 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 6; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_3x3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 9];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 9) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 9 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 9; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_3x4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 12];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 12) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 12 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 12; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_4x2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 8];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 8) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 8 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 8; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_4x3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 12];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 12) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 12 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 12; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_float_matrix_4x4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	float * c_values = new float[size * 16];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 16) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 16 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 16; ++i) {
			c_values[cnt++] = (float)PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to float");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_2x2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 4];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 4) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 4 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 4; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_2x3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 6];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 6) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 6 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 6; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_2x4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 8];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 8) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 8 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 8; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_3x2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 6];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 6) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 6 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 6; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_3x3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 9];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 9) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 9 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 9; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_3x4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 12];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 12) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 12 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 12; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_4x2_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 8];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 8) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 8 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 8; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_4x3_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 12];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 12) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 12 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 12; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}

int MGLUniform_double_matrix_4x4_array_value_setter(MGLUniform * self, PyObject * value) {

	if (Py_TYPE(value) != &PyList_Type) {
		MGLError * error = MGLError_New(TRACE, "value must be a list not %s", Py_TYPE(value));
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int size = (int)PyList_GET_SIZE(value);

	if (size != self->array_length) {
		MGLError * error = MGLError_New(TRACE, "value must be a list of size %d not %d", self->array_length, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int cnt = 0;
	double * c_values = new double[size * 16];

	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(value, k);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple not %s", k, Py_TYPE(value));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		int tuple_size = (int)PyTuple_GET_SIZE(tuple);

		if (tuple_size != 16) {
			MGLError * error = MGLError_New(TRACE, "value[%d] must be a tuple of size 16 not %d", k, tuple_size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			delete[] c_values;
			return -1;
		}

		for (int i = 0; i < 16; ++i) {
			c_values[cnt++] = PyFloat_AsDouble(PyTuple_GET_ITEM(tuple, i));
		}
	}

	if (PyErr_Occurred()) {
		MGLError * error = MGLError_New(TRACE, "Cannot convert value to double");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		delete[] c_values;
		return -1;
	}

	((gl_uniform_matrix_writer_proc)self->gl_value_writer_proc)(self->program_obj, self->location, size, false, c_values);

	delete[] c_values;
	return 0;
}
