#include <cpp_odbc/error.h>

#include <pybind11/pybind11.h>

namespace turbodbc { namespace bindings {


void for_error(pybind11::module & module)
{
	pybind11::register_exception<cpp_odbc::error>(module, "Error");
}

} }
