#pragma once

#include "Python.hpp"

#include "FramebufferAttachment.hpp"

struct MGLMultisampleRenderbuffer : public MGLFramebufferAttachment {
};

extern PyTypeObject MGLMultisampleRenderbuffer_Type;

MGLMultisampleRenderbuffer * MGLMultisampleRenderbuffer_New();
void MGLMultisampleRenderbuffer_Invalidate(MGLMultisampleRenderbuffer * renderbuffer);
