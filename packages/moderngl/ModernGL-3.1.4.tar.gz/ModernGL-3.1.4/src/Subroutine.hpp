#pragma once

#include "Python.hpp"

#include "ProgramStageMember.hpp"

struct MGLSubroutine : public MGLProgramStageMember {
	PyObject * name;

	int number;
	int index;
	int location;
	int type;

	int dimension;
	int element_size;
	int array_length;

	bool matrix;
};

extern PyTypeObject MGLSubroutine_Type;

MGLSubroutine * MGLSubroutine_New();
void MGLSubroutine_Invalidate(MGLSubroutine * subroutine);
void MGLSubroutine_Complete(MGLSubroutine * subroutine);
