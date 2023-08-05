#pragma once

#include "Python.hpp"

#include "Object.hpp"
#include "Program.hpp"

struct MGLProgramMember : public MGLObject {
	int program_obj;
};

extern PyTypeObject MGLProgramMember_Type;
