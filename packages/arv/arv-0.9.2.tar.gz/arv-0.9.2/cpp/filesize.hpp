/*
 * dna-traitrs
 * Copyright 2014, 2016 Christian Stigen Larsen
 * Distributed under the GNU GPL v3 or later. See COPYING.
 *
 * arv
 * Copyright 2017 Christian Stigen Larsen
 * Distributed under the GNU GPL V3 or later. See COPYING.
 */

#ifndef ARV_FILESIZE_HPP
#define ARV_FILESIZE_HPP

#include <cstddef>

namespace arv {

std::size_t filesize(const int file_descriptor);

} // namespace arv

#endif // guard
