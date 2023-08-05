#include "Uniform.hpp"

#include "Error.hpp"

PyObject * MGLUniform_invalid_getter(MGLUniform * self) {
	MGLError * error = MGLError_New(TRACE, "Cannot detect uniform type");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return 0;
}

PyObject * MGLUniform_bool_value_getter(MGLUniform * self) {
	int value = 0;
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, &value);
	return PyBool_FromLong(value);
}

PyObject * MGLUniform_bvec2_value_getter(MGLUniform * self) {
	int values[2] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		2,
		PyBool_FromLong(values[0]),
		PyBool_FromLong(values[1])
	);
}

PyObject * MGLUniform_bvec3_value_getter(MGLUniform * self) {
	int values[3] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		3,
		PyBool_FromLong(values[0]),
		PyBool_FromLong(values[1]),
		PyBool_FromLong(values[2])
	);
}

PyObject * MGLUniform_bvec4_value_getter(MGLUniform * self) {
	int values[4] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		4,
		PyBool_FromLong(values[0]),
		PyBool_FromLong(values[1]),
		PyBool_FromLong(values[2]),
		PyBool_FromLong(values[3])
	);
}

PyObject * MGLUniform_int_value_getter(MGLUniform * self) {
	int value = 0;
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, &value);
	return PyLong_FromLong(value);
}

PyObject * MGLUniform_ivec2_value_getter(MGLUniform * self) {
	int values[2] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		2,
		PyLong_FromLong(values[0]),
		PyLong_FromLong(values[1])
	);
}

PyObject * MGLUniform_ivec3_value_getter(MGLUniform * self) {
	int values[3] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		3,
		PyLong_FromLong(values[0]),
		PyLong_FromLong(values[1]),
		PyLong_FromLong(values[2])
	);
}

PyObject * MGLUniform_ivec4_value_getter(MGLUniform * self) {
	int values[4] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		4,
		PyLong_FromLong(values[0]),
		PyLong_FromLong(values[1]),
		PyLong_FromLong(values[2]),
		PyLong_FromLong(values[3])
	);
}

PyObject * MGLUniform_uint_value_getter(MGLUniform * self) {
	unsigned value = 0;
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, &value);
	return PyLong_FromUnsignedLong(value);
}

PyObject * MGLUniform_uvec2_value_getter(MGLUniform * self) {
	unsigned values[2] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		2,
		PyLong_FromUnsignedLong(values[0]),
		PyLong_FromUnsignedLong(values[1])
	);
}

PyObject * MGLUniform_uvec3_value_getter(MGLUniform * self) {
	unsigned values[3] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		3,
		PyLong_FromUnsignedLong(values[0]),
		PyLong_FromUnsignedLong(values[1]),
		PyLong_FromUnsignedLong(values[2])
	);
}

PyObject * MGLUniform_uvec4_value_getter(MGLUniform * self) {
	unsigned values[4] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		4,
		PyLong_FromUnsignedLong(values[0]),
		PyLong_FromUnsignedLong(values[1]),
		PyLong_FromUnsignedLong(values[2]),
		PyLong_FromUnsignedLong(values[3])
	);
}

PyObject * MGLUniform_float_value_getter(MGLUniform * self) {
	float value = 0;
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, &value);
	return PyFloat_FromDouble(value);
}

PyObject * MGLUniform_vec2_value_getter(MGLUniform * self) {
	float values[2] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		2,
		PyFloat_FromDouble(values[0]),
		PyFloat_FromDouble(values[1])
	);
}

PyObject * MGLUniform_vec3_value_getter(MGLUniform * self) {
	float values[3] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		3,
		PyFloat_FromDouble(values[0]),
		PyFloat_FromDouble(values[1]),
		PyFloat_FromDouble(values[2])
	);
}

PyObject * MGLUniform_vec4_value_getter(MGLUniform * self) {
	float values[4] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		4,
		PyFloat_FromDouble(values[0]),
		PyFloat_FromDouble(values[1]),
		PyFloat_FromDouble(values[2]),
		PyFloat_FromDouble(values[3])
	);
}

PyObject * MGLUniform_double_value_getter(MGLUniform * self) {
	double value = 0;
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, &value);
	return PyFloat_FromDouble(value);
}

PyObject * MGLUniform_dvec2_value_getter(MGLUniform * self) {
	double values[2] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		2,
		PyFloat_FromDouble(values[0]),
		PyFloat_FromDouble(values[1])
	);
}

PyObject * MGLUniform_dvec3_value_getter(MGLUniform * self) {
	double values[3] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		3,
		PyFloat_FromDouble(values[0]),
		PyFloat_FromDouble(values[1]),
		PyFloat_FromDouble(values[2])
	);
}

PyObject * MGLUniform_dvec4_value_getter(MGLUniform * self) {
	double values[4] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	return PyTuple_Pack(
		4,
		PyFloat_FromDouble(values[0]),
		PyFloat_FromDouble(values[1]),
		PyFloat_FromDouble(values[2]),
		PyFloat_FromDouble(values[3])
	);
}

PyObject * MGLUniform_sampler_value_getter(MGLUniform * self) {
	int value = 0;
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, &value);
	return PyLong_FromLong(value);
}

PyObject * MGLUniform_float_matrix_2x2_value_getter(MGLUniform * self) {
	float values[4] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(4);
	for (int i = 0; i < 4; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_2x3_value_getter(MGLUniform * self) {
	float values[6] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(6);
	for (int i = 0; i < 6; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_2x4_value_getter(MGLUniform * self) {
	float values[8] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(8);
	for (int i = 0; i < 8; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_3x2_value_getter(MGLUniform * self) {
	float values[6] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(6);
	for (int i = 0; i < 6; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_3x3_value_getter(MGLUniform * self) {
	float values[9] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(9);
	for (int i = 0; i < 9; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_3x4_value_getter(MGLUniform * self) {
	float values[12] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(12);
	for (int i = 0; i < 12; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_4x2_value_getter(MGLUniform * self) {
	float values[8] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(8);
	for (int i = 0; i < 8; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_4x3_value_getter(MGLUniform * self) {
	float values[12] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(12);
	for (int i = 0; i < 12; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_float_matrix_4x4_value_getter(MGLUniform * self) {
	float values[16] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(16);
	for (int i = 0; i < 16; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_2x2_value_getter(MGLUniform * self) {
	double values[4] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(4);
	for (int i = 0; i < 4; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_2x3_value_getter(MGLUniform * self) {
	double values[6] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(6);
	for (int i = 0; i < 6; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_2x4_value_getter(MGLUniform * self) {
	double values[8] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(8);
	for (int i = 0; i < 8; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_3x2_value_getter(MGLUniform * self) {
	double values[6] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(6);
	for (int i = 0; i < 6; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_3x3_value_getter(MGLUniform * self) {
	double values[9] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(9);
	for (int i = 0; i < 9; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_3x4_value_getter(MGLUniform * self) {
	double values[12] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(12);
	for (int i = 0; i < 12; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_4x2_value_getter(MGLUniform * self) {
	double values[8] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(8);
	for (int i = 0; i < 8; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_4x3_value_getter(MGLUniform * self) {
	double values[12] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(12);
	for (int i = 0; i < 12; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_double_matrix_4x4_value_getter(MGLUniform * self) {
	double values[16] = {};
	((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location, values);
	PyObject * tuple = PyTuple_New(16);
	for (int i = 0; i < 16; ++i) {
		PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
	}
	return tuple;
}

PyObject * MGLUniform_bool_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		int value = 0;
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, &value);
		PyList_SET_ITEM(lst, i, PyBool_FromLong(value));
	}

	return lst;
}

PyObject * MGLUniform_bvec2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		int values[2] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_Pack(
			2,
			PyBool_FromLong(values[0]),
			PyBool_FromLong(values[1])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_bvec3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		int values[3] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			3,
			PyBool_FromLong(values[0]),
			PyBool_FromLong(values[1]),
			PyBool_FromLong(values[2])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_bvec4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		int values[4] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			4,
			PyBool_FromLong(values[0]),
			PyBool_FromLong(values[1]),
			PyBool_FromLong(values[2]),
			PyBool_FromLong(values[3])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_int_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		int value = 0;
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, &value);
		PyList_SET_ITEM(lst, i, PyLong_FromLong(value));
	}

	return lst;
}

PyObject * MGLUniform_ivec2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		int values[2] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			2,
			PyLong_FromLong(values[0]),
			PyLong_FromLong(values[1])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_ivec3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		int values[3] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			3,
			PyLong_FromLong(values[0]),
			PyLong_FromLong(values[1]),
			PyLong_FromLong(values[2])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_ivec4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		int values[4] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			4,
			PyLong_FromLong(values[0]),
			PyLong_FromLong(values[1]),
			PyLong_FromLong(values[2]),
			PyLong_FromLong(values[3])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_uint_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		unsigned value = 0;
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, &value);
		PyList_SET_ITEM(lst, i, PyLong_FromUnsignedLong(value));
	}

	return lst;
}

PyObject * MGLUniform_uvec2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		unsigned values[2] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			2,
			PyLong_FromUnsignedLong(values[0]),
			PyLong_FromUnsignedLong(values[1])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_uvec3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		unsigned values[3] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			3,
			PyLong_FromUnsignedLong(values[0]),
			PyLong_FromUnsignedLong(values[1]),
			PyLong_FromUnsignedLong(values[2])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_uvec4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		unsigned values[4] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			4,
			PyLong_FromUnsignedLong(values[0]),
			PyLong_FromUnsignedLong(values[1]),
			PyLong_FromUnsignedLong(values[2]),
			PyLong_FromUnsignedLong(values[3])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float value = 0;
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, &value);
		PyList_SET_ITEM(lst, i, PyFloat_FromDouble(value));
	}

	return lst;
}

PyObject * MGLUniform_vec2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		float values[2] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			2,
			PyFloat_FromDouble(values[0]),
			PyFloat_FromDouble(values[1])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_vec3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		float values[3] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			3,
			PyFloat_FromDouble(values[0]),
			PyFloat_FromDouble(values[1]),
			PyFloat_FromDouble(values[2])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_vec4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		float values[4] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			4,
			PyFloat_FromDouble(values[0]),
			PyFloat_FromDouble(values[1]),
			PyFloat_FromDouble(values[2]),
			PyFloat_FromDouble(values[3])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double value = 0;
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, &value);
		PyList_SET_ITEM(lst, i, PyFloat_FromDouble(value));
	}

	return lst;
}

PyObject * MGLUniform_dvec2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		double values[2] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			2,
			PyFloat_FromDouble(values[0]),
			PyFloat_FromDouble(values[1])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_dvec3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		double values[3] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			3,
			PyFloat_FromDouble(values[0]),
			PyFloat_FromDouble(values[1]),
			PyFloat_FromDouble(values[2])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_dvec4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {

		double values[4] = {};
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);
		PyObject * tuple = PyTuple_Pack(
			4,
			PyFloat_FromDouble(values[0]),
			PyFloat_FromDouble(values[1]),
			PyFloat_FromDouble(values[2]),
			PyFloat_FromDouble(values[3])
		);

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_sampler_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		int value = 0;
		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, &value);
		PyList_SET_ITEM(lst, i, PyLong_FromLong(value));
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_2x2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[4] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(4);

		for (int i = 0; i < 4; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_2x3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[6] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(6);

		for (int i = 0; i < 6; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_2x4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[8] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(8);

		for (int i = 0; i < 8; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_3x2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[6] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(6);

		for (int i = 0; i < 6; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_3x3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[9] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(9);

		for (int i = 0; i < 9; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_3x4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[12] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(12);

		for (int i = 0; i < 12; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_4x2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[8] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(8);

		for (int i = 0; i < 8; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_4x3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[12] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(12);

		for (int i = 0; i < 12; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_float_matrix_4x4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		float values[16] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(16);

		for (int i = 0; i < 16; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_2x2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[4] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(4);

		for (int i = 0; i < 4; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_2x3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[6] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(6);

		for (int i = 0; i < 6; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_2x4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[8] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(8);

		for (int i = 0; i < 8; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_3x2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[6] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(6);

		for (int i = 0; i < 6; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_3x3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[9] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(9);

		for (int i = 0; i < 9; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_3x4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[12] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(12);

		for (int i = 0; i < 12; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_4x2_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[8] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(8);

		for (int i = 0; i < 8; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_4x3_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[12] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(12);

		for (int i = 0; i < 12; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}

PyObject * MGLUniform_double_matrix_4x4_array_value_getter(MGLUniform * self) {
	int size = self->array_length;

	PyObject * lst = PyList_New(size);
	for (int i = 0; i < size; ++i) {
		double values[16] = {};

		((gl_uniform_reader_proc)self->gl_value_reader_proc)(self->program_obj, self->location + i, values);

		PyObject * tuple = PyTuple_New(16);

		for (int i = 0; i < 16; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(values[i]));
		}

		PyList_SET_ITEM(lst, i, tuple);
	}

	return lst;
}
