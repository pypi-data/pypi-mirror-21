/*
 * dna-traits
 * Copyright 2014, 2016 Christian Stigen Larsen
 * Distributed under the GNU GPL v3 or later. See COPYING.
 *
 * arv
 * Copyright 2017 Christian Stigen Larsen
 * Distributed under the GNU GPL v3 or later. See COPYING.
 */

#include "file.hpp"

#include <unistd.h>
#include <fcntl.h>
#include <stdexcept>
#include <string>

namespace arv {

File::File(const char* filename, const int flags):
  fd(open(filename, flags, S_IRUSR))
{
  if ( fd < 0 ) {
    std::string msg = "Could not open ";
    throw std::runtime_error((msg + filename).c_str());
  }
}

File::~File() {
  close(fd);
}

} // ns arv
