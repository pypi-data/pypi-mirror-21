#pragma once

#include "Python.hpp"

#include "Object.hpp"

struct MGLVersion : public MGLObject {
	const char * name;

	int major;
	int minor;
};

extern PyTypeObject MGLVersion_Type;

MGLVersion * MGLVersion_New();

extern MGLVersion * CORE_330;
extern MGLVersion * CORE_400;
extern MGLVersion * CORE_410;
extern MGLVersion * CORE_420;
extern MGLVersion * CORE_430;
extern MGLVersion * CORE_440;
extern MGLVersion * CORE_450;
